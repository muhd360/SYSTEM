import pytest
import sqlite3
from db_manager import DBManager

@pytest.fixture
def db_manager():
    return DBManager(":memory:")

def test_create_table(db_manager):
    # Table should be created in the constructor
    with db_manager.conn:
        cursor = db_manager.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
        assert cursor.fetchone() is not None

def test_insert_product_data(db_manager):
    test_data = {
        "product_name": "Test Product",
        "product_category": "Test Category",
        "expiry_date": "2023-12-31",
        "mrp": "9.99",
        "freshness_score": 85.5,
        "vlm_description": "A test product description"
    }
    db_manager.insert_product_data(test_data)

    with db_manager.conn:
        cursor = db_manager.conn.cursor()
        cursor.execute("SELECT * FROM products")
        result = cursor.fetchone()

    assert result[1] == "Test Product"
    assert result[2] == "Test Category"
    assert result[3] == "2023-12-31"
    assert result[4] == "9.99"
    assert result[5] == 85.5
    assert result[6] == "A test product description"

def test_insert_invalid_data(db_manager):
    invalid_data = {}
    with pytest.raises(sqlite3.Error):
        db_manager.insert_product_data(invalid_data)
