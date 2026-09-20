"""A small content-based recommendation engine for learning resources."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_CATALOG = ROOT / "data" / "catalog.json"
LEVELS = {"beginner", "intermediate", "advanced"}


def load_catalog(path: str | Path = DEFAULT_CATALOG) -> list[dict[str, Any]]:
    """Load the recommendation catalog from JSON."""
    with Path(path).open(encoding="utf-8") as file:
        catalog = json.load(file)
    if not isinstance(catalog, list) or not catalog:
        raise ValueError("The catalog must contain at least one item.")
    return catalog


def normalize_preferences(interests: str | list[str]) -> set[str]:
    """Turn comma-separated or list-based interests into normalized tags."""
    values = interests.split(",") if isinstance(interests, str) else interests
    return {value.strip().lower().replace(" ", "-") for value in values if value.strip()}


def similarity_score(preferences: set[str], item: dict[str, Any], level: str | None = None) -> float:
    """Calculate a transparent Jaccard-style score with a small level bonus."""
    item_tags = {str(tag).lower().replace(" ", "-") for tag in item.get("tags", [])}
    if not preferences or not item_tags:
        return 0.0

    overlap = len(preferences & item_tags)
    union = len(preferences | item_tags)
    score = overlap / union if union else 0.0
    if level and level.lower() == str(item.get("level", "")).lower():
        score += 0.1
    return round(score, 4)


def recommend(interests: str | list[str], level: str | None = None, limit: int = 5, catalog_path: str | Path = DEFAULT_CATALOG) -> list[dict[str, Any]]:
    """Return the highest-scoring items for a user's preferences."""
    preferences = normalize_preferences(interests)
    normalized_level = level.lower() if level else None
    scored = []
    for item in load_catalog(catalog_path):
        result = dict(item)
        result["score"] = similarity_score(preferences, item, normalized_level)
        result["matched_tags"] = sorted(preferences & {tag.lower().replace(" ", "-") for tag in item.get("tags", [])})
        scored.append(result)
    scored.sort(key=lambda item: (-item["score"], item["title"]))
    return scored[:max(1, limit)]


def print_recommendations(results: list[dict[str, Any]]) -> None:
    """Print ranked recommendations in a readable format."""
    print("\nRecommended learning resources")
    print("=" * 32)
    for index, item in enumerate(results, start=1):
        matched = ", ".join(item["matched_tags"]) or "general match"
        print(f"{index}. {item['title']} — {item['category']}")
        print(f"   Level: {item['level']} | Match score: {item['score']:.2f} | Matched: {matched}")
        print(f"   {item['description']}")


def run_cli() -> None:
    """Collect preferences and display recommendations."""
    print("TasteMatch: a simple preference-based learning recommender")
    interests = input("What are you interested in? (comma-separated): ").strip()
    level = input("What is your level? (beginner/intermediate/advanced, optional): ").strip() or None
    if level and level.lower() not in LEVELS:
        print("Unknown level; continuing without a level preference.")
        level = None
    print_recommendations(recommend(interests, level))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--interests", help="Comma-separated interests, e.g. python,data")
    parser.add_argument("--level", choices=sorted(LEVELS), default=None)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    args = parser.parse_args()
    if args.interests:
        print_recommendations(recommend(args.interests, args.level, args.limit, args.catalog))
    else:
        run_cli()


if __name__ == "__main__":
    main()
