import json
import tempfile
import unittest
from pathlib import Path

from classify_orders import DEFAULT_DATA, build_pipeline, load_dataset, train_and_evaluate


class ClassificationProjectTest(unittest.TestCase):
    def test_dataset_loads_with_expected_target_and_features(self):
        frame = load_dataset(DEFAULT_DATA)
        self.assertEqual(len(frame), 1200)
        self.assertIn("OrderStatus", frame.columns)
        self.assertIn("OrderYear", frame.columns)

    def test_pipeline_contains_a_decision_tree(self):
        pipeline = build_pipeline()
        self.assertEqual(pipeline.named_steps["classifier"].__class__.__name__, "DecisionTreeClassifier")

    def test_evaluation_is_reproducible_and_serializable(self):
        first = train_and_evaluate(DEFAULT_DATA)
        second = train_and_evaluate(DEFAULT_DATA)
        self.assertEqual(first["accuracy"], second["accuracy"])
        self.assertEqual(first["training_rows"], 960)
        self.assertEqual(first["testing_rows"], 240)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "metrics.json"
            output.write_text(json.dumps(first), encoding="utf-8")
            self.assertTrue(json.loads(output.read_text(encoding="utf-8"))["classes"])


if __name__ == "__main__":
    unittest.main()
