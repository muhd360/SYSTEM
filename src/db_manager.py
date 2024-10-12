import sqlite3
import logging


class DBManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        """
        Creates the products table if it doesn't exist.
        """
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    product_name TEXT,
                    product_category TEXT,
                    expiry_date TEXT
                )
            """)

    def insert_product_data(self, product_data):
        """
        Inserts parsed OCR data into the database.
        """
        try:
            with self.conn:
                self.conn.execute(
                    """
                    INSERT INTO products (product_name, product_category, expiry_date)
                    VALUES (?, ?, ?)
                """,
                    (
                        product_data.get("product_name", "Unknown"),
                        product_data.get("product_category", "Unknown"),
                        product_data.get("expiry_date", "Not found"),
                    ),
                )
            logging.info("Data inserted successfully into the database.")
        except sqlite3.Error as e:
            logging.error(f"Database insertion error: {e}")
            raise
