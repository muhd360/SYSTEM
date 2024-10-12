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
                    freshness_score REAL,
                    vlm_description TEXT
                )
            """)

    def insert_product_data(self, product_data):
        try:
            with self.conn:
                self.conn.execute(
                    """
                    INSERT INTO products (product_name, product_category, expiry_date, mrp, freshness_score, vlm_description)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        product_data.get("product_name", "Unknown"),
                        product_data.get("product_category", "Unknown"),
                        product_data.get("expiry_date", "Not found"),
                        product_data.get("mrp", "Not found"),
                        product_data.get("freshness_score", 0.0),
                        product_data.get("vlm_description", ""),
                    ),
                )
            logging.info("Data inserted successfully into the database.")
        except sqlite3.Error as e:
            logging.error(f"Database insertion error: {e}")
            raise
