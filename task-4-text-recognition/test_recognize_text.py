import unittest

from PIL import Image

from recognize_text import DEFAULT_IMAGE, preprocess_image, recognize_text


class TextRecognitionTest(unittest.TestCase):
    def test_preprocessing_converts_to_grayscale_and_upscales(self):
        with Image.open(DEFAULT_IMAGE) as original:
            original_size = original.size
        processed = preprocess_image(DEFAULT_IMAGE)
        self.assertEqual(processed.mode, "L")
        self.assertEqual(processed.size, (original_size[0] * 2, original_size[1] * 2))

    def test_recognition_returns_structured_output(self):
        result = recognize_text(DEFAULT_IMAGE)
        self.assertEqual(result["engine"], "Tesseract OCR via pytesseract")
        self.assertGreater(result["token_count"], 3)
        self.assertIn("LOGIC", result["text"].upper())
        self.assertGreater(result["average_confidence"], 50)

    def test_tokens_have_confidence_scores(self):
        result = recognize_text(DEFAULT_IMAGE)
        self.assertTrue(all("text" in token and "confidence" in token for token in result["tokens"]))


if __name__ == "__main__":
    unittest.main()
