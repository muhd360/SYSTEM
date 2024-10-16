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
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-i", "--image-url", type=str, help="URL of the image to process for OCR."
    )
    group.add_argument(
        "-f", "--image-file", type=str, help="Path to the local image file to process for OCR."
    )
    parser.add_argument(
        "-db", "--database", type=str, default="products.db", help="Path to the SQLite database file."
    )
    args = parser.parse_args()
    
    if args.image_file and not os.path.isfile(args.image_file):
        parser.error(f"The file {args.image_file} does not exist!")
    
    return args


def load_image(image_path_or_url):
    """
    Load an image from a local file or URL.
    
    :param image_path_or_url: str, path to local file or URL of the image
    :return: PIL.Image object
    """
    if image_path_or_url.startswith(('http://', 'https://')):
        response = requests.get(image_path_or_url)
        img = Image.open(BytesIO(response.content))
    elif os.path.isfile(image_path_or_url):
        img = Image.open(image_path_or_url)
    else:
        raise ValueError(f"Invalid image path or URL: {image_path_or_url}")
    
    return img


def main():
    args = parse_arguments()
    image_input = args.image_url or args.image_file
    db_path = args.database

    ocr_extractor = OCRExtractor(api_key="YOUR_API_KEY")
    db_manager = DBManager(db_path)
    freshness_detector = FreshnessDetector()
    text_detector = TextDetector()
    feature_extractor = FeatureExtractor()
    vlm = VisionLanguageModel()

    logging.info(f"Processing image: {image_input}")
    try:
        ocr_result = ocr_extractor.process_image(image_input)
        extracted_text = text_detector.detect_text(image_input)
        features = feature_extractor.extract_features(image_input)
        freshness_score = freshness_detector.assess_freshness(features)
        vlm_description = vlm.describe_image(image_input)
        
        if not vlm_description:
            logging.warning("VLM description is empty. Proceeding with other data.")
        
        logging.info("Parsing OCR results...")
        extracted_data = ocr_extractor.parse_ocr_result(ocr_result + "\n" + extracted_text)
        extracted_data["freshness_score"] = freshness_score
        extracted_data["vlm_description"] = json.dumps(vlm_description)  # Convert dict to JSON string

        logging.info("Inserting data into the database...")
        db_manager.insert_product_data(extracted_data)

        logging.info("Process completed successfully.")
        print("OCR process completed and data inserted into the database.")
    except Exception as e:
        logging.error(f"Error during image processing: {e}")
        print("Error processing the image. Check logs for details.")

if __name__ == "__main__":
    main()
