"""Train and evaluate a simple classifier for e-commerce order status."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier


ROOT = Path(__file__).resolve().parent
DEFAULT_DATA = ROOT / "data" / "orders.csv"
DEFAULT_METRICS = ROOT / "metrics.json"
TARGET = "OrderStatus"


# IDs and free-text identifiers are deliberately excluded: they identify rows but
# do not provide a meaningful, reusable signal for a new order.
NUMERIC_FEATURES = ["Quantity", "UnitPrice", "ItemsInCart", "TotalPrice", "OrderYear", "OrderMonth", "OrderDayOfWeek"]
CATEGORICAL_FEATURES = ["Product", "PaymentMethod", "CouponCode", "ReferralSource"]


def load_dataset(path: str | Path = DEFAULT_DATA) -> pd.DataFrame:
    """Load the assigned CSV and add useful date-derived features."""
    frame = pd.read_csv(path)
    frame["Date"] = pd.to_datetime(frame["Date"], errors="coerce")
    frame["OrderYear"] = frame["Date"].dt.year
    frame["OrderMonth"] = frame["Date"].dt.month
    frame["OrderDayOfWeek"] = frame["Date"].dt.dayofweek
    return frame


def build_pipeline() -> Pipeline:
    """Build the preprocessing and classification pipeline."""
    numeric = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
    ])
    categorical = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("one_hot", OneHotEncoder(handle_unknown="ignore")),
    ])
    preprocessor = ColumnTransformer([
        ("numeric", numeric, NUMERIC_FEATURES),
        ("categorical", categorical, CATEGORICAL_FEATURES),
    ])
    return Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", DecisionTreeClassifier(max_depth=8, min_samples_leaf=4, random_state=42)),
    ])


def train_and_evaluate(data_path: str | Path = DEFAULT_DATA) -> dict:
    """Split, train, evaluate, and return serializable metrics."""
    frame = load_dataset(data_path)
    features = frame[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    target = frame[TARGET]
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42,
        stratify=target,
    )

    model = build_pipeline()
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    labels = sorted(target.unique().tolist())
    report = classification_report(y_test, predictions, labels=labels, output_dict=True, zero_division=0)

    return {
        "dataset_rows": int(len(frame)),
        "training_rows": int(len(x_train)),
        "testing_rows": int(len(x_test)),
        "target": TARGET,
        "classes": labels,
        "algorithm": "Decision Tree",
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "macro_f1": round(float(report["macro avg"]["f1-score"]), 4),
        "confusion_matrix": confusion_matrix(y_test, predictions, labels=labels).tolist(),
        "classification_report": {
            label: {
                "precision": round(float(report[label]["precision"]), 4),
                "recall": round(float(report[label]["recall"]), 4),
                "f1_score": round(float(report[label]["f1-score"]), 4),
                "support": int(report[label]["support"]),
            }
            for label in labels
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--metrics", type=Path, default=DEFAULT_METRICS)
    args = parser.parse_args()

    metrics = train_and_evaluate(args.data)
    args.metrics.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    print(f"Dataset rows: {metrics['dataset_rows']}")
    print(f"Train/test split: {metrics['training_rows']}/{metrics['testing_rows']}")
    print(f"Algorithm: {metrics['algorithm']}")
    print(f"Accuracy: {metrics['accuracy']:.2%}")
    print(f"Macro F1: {metrics['macro_f1']:.4f}")


if __name__ == "__main__":
    main()
