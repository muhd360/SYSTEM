import os
import argparse
import logging
from ocr_extractor import OCRExtractor
from db_manager import DBManager
from freshness import FreshnessDetector
from detect_text import TextDetector
from extract_features import FeatureExtractor
from vlm import VisionLanguageModel
from anomaly_detector import AnomalyDetector
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

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
    if image_path_or_url.startswith(('http://', 'https://')):
        response = requests.get(image_path_or_url)
        img = Image.open(BytesIO(response.content))
    elif os.path.isfile(image_path_or_url):
        img = Image.open(image_path_or_url)
    else:
        raise ValueError(f"Invalid image path or URL: {image_path_or_url}")
    
    return img

def process_image(image_input, db_manager):
    ocr_extractor = OCRExtractor(api_key="YOUR_API_KEY")
    text_detector = TextDetector()
    feature_extractor = FeatureExtractor()
    vlm = VisionLanguageModel()
    freshness_detector = FreshnessDetector()
    anomaly_detector = AnomalyDetector()

    vlm_result = vlm.describe_image(image_input)
    ocr_result = ocr_extractor.process_image(image_input)
    extracted_text = text_detector.detect_text(image_input)
    features = feature_extractor.extract_features(image_input)

    product_category = vlm_result.get('category', 'Unknown')

    if product_category.lower() in ['fruit', 'vegetable', 'produce']:
        quality_score = freshness_detector.assess_freshness(features)
    else:
        quality_score = anomaly_detector.detect_anomalies(features)

    extracted_data = ocr_extractor.parse_ocr_result(ocr_result + "\n" + extracted_text)
    extracted_data.update(vlm_result)
    extracted_data['quality_score'] = quality_score
    extracted_data['raw_ocr'] = ocr_result
    extracted_data['raw_text'] = extracted_text

    db_manager.insert_product_data(extracted_data)

    return extracted_data

class ProductGUI:
    def __init__(self, master, db_manager):
        self.master = master
        self.db_manager = db_manager
        self.master.title("Product Information")
        self.master.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        self.image_label = ttk.Label(self.master)
        self.image_label.pack(pady=10)

        self.info_text = tk.Text(self.master, height=20, width=80)
        self.info_text.pack(pady=10)

        self.refresh_button = ttk.Button(self.master, text="Refresh", command=self.refresh_data)
        self.refresh_button.pack(pady=10)

    def refresh_data(self):
        latest_product = self.db_manager.get_latest_product()
        if latest_product:
            self.display_product_info(latest_product)

    def display_product_info(self, product):
        # Display image
        img = Image.open(product['image_path'])
        img = img.resize((300, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=photo)
        self.image_label.image = photo

        # Display text information
        self.info_text.delete('1.0', tk.END)
        info = f"Product Name: {product['product_name']}\n"
        info += f"Category: {product['product_category']}\n"
        info += f"Expiry Date: {product['expiry_date']}\n"
        info += f"MRP: {product['mrp']}\n"
        info += f"Quality Score: {product['quality_score']}\n"
        info += f"OCR Result: {product['raw_ocr']}\n"
        info += f"Extracted Text: {product['raw_text']}\n"
        self.info_text.insert(tk.END, info)

def main():
    args = parse_arguments()
    image_input = args.image_url or args.image_file
    db_path = args.database

    db_manager = DBManager(db_path)

    try:
        extracted_data = process_image(image_input, db_manager)
        logging.info("Process completed successfully.")
        print("OCR process completed and data inserted into the database.")
    except Exception as e:
        logging.error(f"Error during image processing: {e}")
        print("Error processing the image. Check logs for details.")

    root = tk.Tk()
    app = ProductGUI(root, db_manager)
    root.mainloop()

if __name__ == "__main__":
    main()
