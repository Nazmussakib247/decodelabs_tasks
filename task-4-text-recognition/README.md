# Task 4 — Basic Text Recognition

For this optional Project 4 task, I built a small OCR pipeline that reads text from an image and returns both the recognized content and confidence information. I used the Tesseract OCR engine through `pytesseract`, with Pillow handling image loading and preprocessing.

The project demonstrates the complete recognition flow: ingest an image, improve its contrast and scale, run a pre-trained OCR engine, collect token-level confidence scores, and display a structured result.

## Requirements covered

- Use an available recognition library: `pytesseract` with the Tesseract OCR engine
- Perform recognition on a sample image
- Display extracted text clearly
- Report average and token-level confidence
- Save machine-readable JSON output

## How it works

1. Load the image and convert it to grayscale.
2. Apply automatic contrast enhancement.
3. Upscale the image by 2x to give the OCR engine a clearer input.
4. Run Tesseract with a page-segmentation mode suitable for a small text block.
5. Keep recognized tokens with valid confidence scores.
6. Print the combined text and save `ocr_result.json`.

## Setup

Install the Python package and the system OCR engine:

```bash
sudo apt-get install tesseract-ocr
python -m pip install -r requirements.txt
```

## Run the recognition pipeline

```bash
python recognize_text.py
```

To process another image:

```bash
python recognize_text.py path/to/your-image.png --output my-result.json
```

The included sample image is a small receipt-style input at `data/sample_receipt.png`.

## Run the tests

```bash
python -m unittest -v
```

The tests check preprocessing, successful recognition, extracted tokens, and confidence scores.

## Project structure

```text
data/sample_receipt.png     Reproducible sample input
auto_result.json             Generated structured OCR output
recognize_text.py            Preprocessing, recognition, and CLI
requirements.txt             Python dependency list
test_recognize_text.py       Automated checks
README.md                    Project notes
```

## Limitations and next steps

OCR quality depends on image resolution, font, lighting, rotation, and language. This small demonstration uses the default English Tesseract model and works best with clean, high-contrast text. A stronger production version would add deskewing, multiple language models, image-quality checks, and a confidence threshold that asks for a clearer image when recognition is uncertain.
