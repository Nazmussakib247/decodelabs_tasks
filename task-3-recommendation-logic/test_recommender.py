import unittest

from recommender import DEFAULT_CATALOG, load_catalog, normalize_preferences, recommend, similarity_score


class RecommendationLogicTest(unittest.TestCase):
    def test_preferences_are_normalized(self):
        self.assertEqual(normalize_preferences("Python, Machine Learning"), {"python", "machine-learning"})

    def test_similarity_rewards_tag_overlap(self):
        item = {"tags": ["python", "data"], "level": "beginner"}
        self.assertGreater(similarity_score({"python", "data"}, item), similarity_score({"sql"}, item))

    def test_recommendations_are_ranked_and_limited(self):
        results = recommend("python,machine-learning", "intermediate", limit=3, catalog_path=DEFAULT_CATALOG)
        self.assertEqual(len(results), 3)
        self.assertGreaterEqual(results[0]["score"], results[1]["score"])
        self.assertTrue(results[0]["matched_tags"])

    def test_catalog_has_enough_items(self):
        self.assertGreaterEqual(len(load_catalog(DEFAULT_CATALOG)), 10)


if __name__ == "__main__":
    unittest.main()
