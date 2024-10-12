# main.py
import argparse
import logging
from ocr_extractor import OCRExtractor
from db_manager import DBManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    filename="ocr_app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="OCR Product Information Extractor using FAL Vision Models and SQL Database Integration."
    )
    parser.add_argument(
        "-i",
        "--image-url",
        type=str,
        required=True,
        help="URL of the image to process for OCR.",
    )
    parser.add_argument(
        "-db",
        "--database",
        type=str,
        default="products.db",
        help="Path to the SQLite database file.",
    )
    return parser.parse_args()


def main():
    """
    Main function to handle the OCR processing and database insertion.
    """
    args = parse_arguments()

    image_url = args.image_url
    db_path = args.database

    # Instantiate the OCR extractor
    ocr_extractor = OCRExtractor(api_key="YOUR_API_KEY")

    # Run the OCR process on the provided image URL
    logging.info(f"Processing image: {image_url}")
    try:
        ocr_result = ocr_extractor.process_image(image_url)
    except Exception as e:
        logging.error(f"Error during OCR processing: {e}")
        print("Error processing the image. Check logs for details.")
        return

    # Instantiate the DB manager
    db_manager = DBManager(db_path)

    # Parse the OCR results
    logging.info("Parsing OCR results...")
    extracted_data = ocr_extractor.parse_ocr_result(ocr_result)

    # Insert parsed data into the database
    logging.info("Inserting data into the database...")
    db_manager.insert_product_data(extracted_data)

    logging.info("Process completed successfully.")
    print("OCR process completed and data inserted into the database.")


if __name__ == "__main__":
    main()
