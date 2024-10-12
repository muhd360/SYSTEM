import pytest
from unittest.mock import patch, MagicMock
from ocr_extractor import OCRExtractor

@pytest.fixture
def ocr_extractor():
    return OCRExtractor("dummy_api_key")

@patch('fal_client.subscribe')
def test_process_image(mock_subscribe, ocr_extractor):
    mock_result = MagicMock()
    mock_result.output = "Extracted text from image"
    mock_subscribe.return_value = mock_result

    result = ocr_extractor.process_image("http://example.com/image.jpg")

    assert result == "Extracted text from image"
    mock_subscribe.assert_called_once()

def test_parse_ocr_result(ocr_extractor):
    test_result = """
    Product: Test Product
    Category: Test Category
    Expiry: 31/12/2024
    MRP: 99.99
    """
    parsed_data = ocr_extractor.parse_ocr_result(test_result)

    assert parsed_data["product_name"] == "Test Product"
    assert parsed_data["product_category"] == "Test Category"
    assert parsed_data["expiry_date"] == "31/12/2024"
    assert parsed_data["mrp"] == "99.99"

def test_parse_ocr_result_missing_data(ocr_extractor):
    test_result = "Some text without any relevant information"
    parsed_data = ocr_extractor.parse_ocr_result(test_result)

    assert parsed_data["product_name"] == "Unknown"
    assert parsed_data["product_category"] == "Unknown"
    assert parsed_data["expiry_date"] == "Not found"
    assert parsed_data["mrp"] == "Not found"
