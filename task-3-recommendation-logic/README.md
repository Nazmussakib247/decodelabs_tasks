# Task 3 — AI Recommendation Logic

For this task, I built **TasteMatch**, a small content-based recommendation system for learning resources. A user enters interests and, optionally, a learning level. The system compares those preferences with item tags, ranks the catalog by similarity, and displays the most relevant recommendations.

I kept the implementation intentionally transparent. It does not pretend to know a user from hidden data, and it does not use a black-box model. Every recommendation can be explained by the tags that matched.

## How the recommendation logic works

1. The user enters comma-separated interests such as `python, machine learning`.
2. The input is normalized into comparable lowercase tags.
3. Each catalog item has its own set of tags and a difficulty level.
4. The engine calculates a Jaccard-style similarity score:

   `overlap between preference tags and item tags / union of both tag sets`

5. A small bonus is added when the requested level matches the item's level.
6. Results are sorted by descending score and returned with the matched tags shown.

## Run it locally

The project uses only Python's standard library.

Interactive mode:

```bash
python recommender.py
```

Command-line mode:

```bash
python recommender.py --interests python,machine-learning --level intermediate --limit 5
```

## Run the tests

```bash
python -m unittest -v
```

The test suite covers input normalization, similarity scoring, ranked output, result limits, and catalog loading.

## Project structure

```text
data/catalog.json       Small catalog of learning resources and item tags
recommender.py           Preference input, similarity logic, ranking, and CLI
test_recommender.py      Automated tests for the recommendation engine
README.md                Project explanation and usage guide
```

## Example

With preferences `python,machine-learning` and level `intermediate`, the recommender favours resources such as **Supervised Learning Lab** because its tags overlap with both interests and its level matches the requested level.

## Reflection and next steps

This project helped me understand the idea behind content-based recommendation: a useful first recommendation does not need a huge model if the item attributes and matching rule are clear. A stronger version could collect ratings, learn user-specific weights, add a larger real catalogue, and compare Jaccard similarity with cosine similarity over vectorized item features.

The current catalogue is intentionally small and curated for learning. The result is a demonstrable recommendation prototype, not a production personalization service.
