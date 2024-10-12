import argparse
import logging
from ocr_extractor import OCRExtractor
from db_manager import DBManager
from freshness import FreshnessDetector
from detect_text import TextDetector
from extract_features import FeatureExtractor
from vlm import VisionLanguageModel

logging.basicConfig(
    level=logging.INFO,
    filename="ocr_app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="OCR Product Information Extractor using FAL Vision Models and SQL Database Integration."
    )
    parser.add_argument(
        "-i", "--image-url", type=str, required=True, help="URL of the image to process for OCR."
    )
    parser.add_argument(
        "-db", "--database", type=str, default="products.db", help="Path to the SQLite database file."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    image_url = args.image_url
    db_path = args.database

    ocr_extractor = OCRExtractor(api_key="YOUR_API_KEY")
    db_manager = DBManager(db_path)
    freshness_detector = FreshnessDetector()
    text_detector = TextDetector()
    feature_extractor = FeatureExtractor()
    vlm = VisionLanguageModel()

    logging.info(f"Processing image: {image_url}")
    try:
        ocr_result = ocr_extractor.process_image(image_url)
        extracted_text = text_detector.detect_text(image_url)
        features = feature_extractor.extract_features(image_url)
        freshness_score = freshness_detector.assess_freshness(features)
        vlm_description = vlm.describe_image(image_url)
    except Exception as e:
        logging.error(f"Error during image processing: {e}")
        print("Error processing the image. Check logs for details.")
        return

    logging.info("Parsing OCR results...")
    extracted_data = ocr_extractor.parse_ocr_result(ocr_result + "\n" + extracted_text)
    extracted_data["freshness_score"] = freshness_score
    extracted_data["vlm_description"] = vlm_description

    logging.info("Inserting data into the database...")
    db_manager.insert_product_data(extracted_data)

    logging.info("Process completed successfully.")
    print("OCR process completed and data inserted into the database.")

if __name__ == "__main__":
    main()
