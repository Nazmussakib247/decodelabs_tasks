# Task 2 — Data Classification Using AI

For this task, I built a small supervised-learning pipeline to predict an e-commerce order's `OrderStatus`. I used the order dataset assigned through the DecodeLabs portal and treated the problem as a multi-class classification task with five possible outcomes: Cancelled, Returned, Pending, Shipped, and Delivered.

The goal was not to build a production recommender or claim that a small synthetic dataset can perfectly predict real-world operations. Instead, I focused on making the complete beginner-friendly workflow visible: loading the data, understanding the target, preparing mixed feature types, splitting the data, training a model, and evaluating its predictions.

## Dataset overview

The dataset contains **1,200 order records** and 14 original columns. The target is `OrderStatus`, which is reasonably balanced across five classes:

| Status | Rows |
|---|---:|
| Cancelled | 250 |
| Returned | 247 |
| Pending | 237 |
| Shipped | 235 |
| Delivered | 231 |

I excluded identifiers such as `OrderID`, `CustomerID`, `TrackingNumber`, and `ShippingAddress` because they identify individual records rather than provide a reusable signal for a new order. I also derived year, month, and day-of-week from `Date` so the date could be used by the model in a simple numeric form.

## Approach

1. Load the CSV with pandas.
2. Parse the order date and create three date features.
3. Split the data into **80% training** and **20% testing** rows with stratification.
4. Impute missing categorical values and one-hot encode categorical columns.
5. Train a `DecisionTreeClassifier` with a controlled depth and minimum leaf size.
6. Measure accuracy, macro F1, per-class precision/recall, and the confusion matrix.

The preprocessing and model are kept together in a scikit-learn `Pipeline`, which means the same transformations are applied consistently during training and evaluation.

## Run locally

Python 3.9 or newer is recommended.

```bash
python -m pip install pandas scikit-learn joblib
python classify_orders.py
```

The command writes the evaluation summary to `metrics.json` and prints the key results to the terminal.

## Run the tests

```bash
python -m unittest -v
```

The tests check that the dataset loads correctly, the requested Decision Tree is present, the split sizes are correct, and evaluation is reproducible.

## Files

```text
data/orders.csv              Assigned dataset used for the task
classify_orders.py            Loading, preprocessing, training, and evaluation
test_classify_orders.py       Automated checks for the pipeline
metrics.json                  Generated evaluation summary
README.md                     Project explanation and setup notes
```

## Results

The model result is intentionally reported as an experiment rather than an overconfident claim. Because the available order fields do not fully explain why a real order changes status, the evaluation score should be read as a baseline for learning. A stronger next step would be to collect event history, timestamps for status changes, fulfilment signals, and a larger labelled dataset before using a model for operational decisions.

## Reflection

This project made the supervised-learning workflow much clearer to me. The most important lesson was that model training is only one part of a useful AI system: feature selection, leakage prevention, evaluation, and honest interpretation matter just as much.
