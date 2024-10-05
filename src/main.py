import os
import json
import sqlite3
import logging
from datetime import datetime
from typing import Dict, Any

import fal_client
from PIL import Image
import base64
import io

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set up SQLite database
conn = sqlite3.connect('product_database.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        brand TEXT,
        pack_size TEXT,
        expiry_date TEXT,
        mrp REAL,
        category TEXT,
        timestamp DATETIME
    )
''')
conn.commit()

def image_to_base64(image_path: str) -> str:
    """Convert an image file to a base64-encoded string."""
    with Image.open(image_path) as image:
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode('utf-8')}"

def process_image(image_path: str) -> str:
    """Process the image using the Moondream API and return the extracted text."""
    logger.info(f"Processing image: {image_path}")
    
    image_base64 = image_to_base64(image_path)
    
    handler = fal_client.submit(
        "fal-ai/moondream/batched",
        arguments={
            "inputs": [{
                # TODO prompt this properly to respond in json or using jsonformer to do it for us or use instructor
                "prompt": "Describe this product in detail, including brand name, product name, pack size, expiry date, and MRP if visible.",
                "image_url": image_base64
            }]
        },
    )

    result = handler.get()
    extracted_text = result['outputs'][0]
    
    logger.info(f"Extracted text: {extracted_text}")
    return extracted_text

def extract_product_details(text: str) -> Dict[str, Any]:
    """Extract product details from the API response."""
    details = {
        "product_name": "",
        "brand": "",
        "pack_size": "",
        "expiry_date": "",
        "mrp": 0.0,
        "category": ""
    }

    # TODO write a more elegant way to do this exact same thing
    # Simple example of information extraction (to be improved with NLP techniques)
    lines = text.split('\n')
    for line in lines:
        if "brand" in line.lower():
            details["brand"] = line.split(':')[-1].strip()
        elif "product" in line.lower():
            details["product_name"] = line.split(':')[-1].strip()
        elif "pack size" in line.lower() or "size" in line.lower():
            details["pack_size"] = line.split(':')[-1].strip()
        elif "expiry" in line.lower():
            details["expiry_date"] = line.split(':')[-1].strip()
        elif "mrp" in line.lower() or "price" in line.lower():
            try:
                price_str = line.split(':')[-1].strip()
                details["mrp"] = float(''.join(filter(str.isdigit, price_str)))
            except ValueError:
                logger.warning(f"Could not parse MRP from line: {line}")

    # Attempt to determine category based on extracted information
    if any(word in details["product_name"].lower() for word in ["shampoo", "soap", "toothpaste"]):
        details["category"] = "Personal Care"
    elif any(word in details["product_name"].lower() for word in ["oil", "pasta", "sauce"]):
        details["category"] = "Food"
    elif any(word in details["product_name"].lower() for word in ["vitamin", "supplement"]):
        details["category"] = "Health Supplements"
    else:
        details["category"] = "Other"

    logger.info(f"Extracted product details: {details}")
    return details

def store_in_database(details: Dict[str, Any]):
    """Store the extracted product details in the SQLite database."""
    logger.info("Storing product details in database")
    cursor.execute('''
        INSERT INTO products (product_name, brand, pack_size, expiry_date, mrp, category, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        details["product_name"],
        details["brand"],
        details["pack_size"],
        details["expiry_date"],
        details["mrp"],
        details["category"],
        datetime.now()
    ))
    conn.commit()
    logger.info("Product details stored successfully")

def provide_feedback(details: Dict[str, Any]) -> str:
    """Provide real-time feedback based on the extracted details."""
    feedback = []
    if not details["product_name"]:
        feedback.append("Product name not detected")
    if not details["brand"]:
        feedback.append("Brand not detected")
    if not details["expiry_date"]:
        feedback.append("Expiry date not detected")
    if details["mrp"] == 0.0:
        feedback.append("MRP not detected or invalid")

    if feedback:
        return "Warning: " + ", ".join(feedback)
    else:
        return "All required details extracted successfully"

def process_product(image_path: str):
    """Main function to process a product image."""
    try:
        extracted_text = process_image(image_path)
        product_details = extract_product_details(extracted_text)
        feedback = provide_feedback(product_details)
        logger.info(feedback)

        store_in_database(product_details)

        return json.dumps(product_details), feedback
    except Exception as e:
        logger.error(f"Error processing product: {str(e)}")
        return json.dumps({}), f"Error: {str(e)}"

def main():
    image_directory = "images"  # Replace with your image directory
    for image_file in os.listdir(image_directory):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_directory, image_file)
            logger.info(f"Processing {image_file}")
            json_result, feedback = process_product(image_path)
            print(f"Result for {image_file}:")
            print(json_result)
            print(feedback)
            print("---")

if __name__ == "__main__":
    main()

