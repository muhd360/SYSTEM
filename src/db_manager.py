import sqlite3
import logging

class DBManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    product_name TEXT,
                    product_category TEXT,
                    expiry_date TEXT,
                    mrp TEXT,
                    quality_score REAL,
                    raw_ocr TEXT,
                    raw_text TEXT,
                    image_path TEXT
                )
            """)

    def insert_product_data(self, product_data):
        try:
            with self.conn:
                self.conn.execute(
                    """
                    INSERT INTO products (product_name, product_category, expiry_date, mrp, quality_score, raw_ocr, raw_text, image_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        product_data.get("product_name", "Unknown"),
                        product_data.get("product_category", "Unknown"),
                        product_data.get("expiry_date", "Not found"),
                        product_data.get("mrp", "Not found"),
                        product_data.get("quality_score", 0.0),
                        product_data.get("raw_ocr", ""),
                        product_data.get("raw_text", ""),
                        product_data.get("image_path", ""),
                    ),
                )
            logging.info("Data inserted successfully into the database.")
        except sqlite3.Error as e:
            logging.error(f"Database insertion error: {e}")
            raise

    def get_latest_product(self):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM products ORDER BY id DESC LIMIT 1")
                row = cursor.fetchone()
                if row:
                    return {
                        "id": row[0],
                        "product_name": row[1],
                        "product_category": row[2],
                        "expiry_date": row[3],
                        "mrp": row[4],
                        "quality_score": row[5],
                        "raw_ocr": row[6],
                        "raw_text": row[7],
                        "image_path": row[8]
                    }
                else:
                    return None
        except sqlite3.Error as e:
            logging.error(f"Database query error: {e}")
            raise
