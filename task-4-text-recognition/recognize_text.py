"""Extract readable text and confidence scores from an image with Tesseract OCR."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pytesseract
from PIL import Image, ImageOps
from pytesseract import Output


ROOT = Path(__file__).resolve().parent
DEFAULT_IMAGE = ROOT / "data" / "sample_receipt.png"
DEFAULT_OUTPUT = ROOT / "ocr_result.json"


def preprocess_image(path: str | Path) -> Image.Image:
    """Prepare an image for OCR with grayscale and 2x upscaling."""
    image = Image.open(path).convert("L")
    image = ImageOps.autocontrast(image)
    return image.resize((image.width * 2, image.height * 2))


def recognize_text(path: str | Path = DEFAULT_IMAGE) -> dict[str, Any]:
    """Run OCR and return the extracted text, confidence, and token details."""
    image = preprocess_image(path)
    data = pytesseract.image_to_data(image, output_type=Output.DICT, config="--psm 6")
    tokens = []
    confidences = []
    for text, confidence in zip(data["text"], data["conf"]):
        cleaned = text.strip()
        try:
            score = float(confidence)
        except (TypeError, ValueError):
            continue
        if cleaned and score >= 0:
            tokens.append({"text": cleaned, "confidence": round(score, 2)})
            confidences.append(score)

    extracted = " ".join(token["text"] for token in tokens)
    average_confidence = sum(confidences) / len(confidences) if confidences else 0.0
    return {
        "image": str(path),
        "engine": "Tesseract OCR via pytesseract",
        "text": extracted,
        "average_confidence": round(average_confidence, 2),
        "tokens": tokens,
        "token_count": len(tokens),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", nargs="?", type=Path, default=DEFAULT_IMAGE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    result = recognize_text(args.image)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Recognized text:")
    print(result["text"])
    print(f"Average confidence: {result['average_confidence']:.2f}%")
    print(f"Saved structured output to: {args.output}")


if __name__ == "__main__":
    main()
