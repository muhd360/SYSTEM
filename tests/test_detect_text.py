import pytest
from unittest.mock import patch, MagicMock
from detect_text import TextDetector
from PIL import Image
from io import BytesIO

@pytest.fixture
def text_detector():
    return TextDetector()

@patch('requests.get')
@patch('pytesseract.image_to_string')
def test_detect_text(mock_image_to_string, mock_get, text_detector):
    mock_response = MagicMock()
    mock_response.content = b'fake image content'
    mock_get.return_value = mock_response

    mock_image_to_string.return_value = "Sample extracted text"

    result = text_detector.detect_text("http://example.com/image.jpg")

    assert result == "Sample extracted text"
    mock_get.assert_called_once_with("http://example.com/image.jpg")
    mock_image_to_string.assert_called_once()

@patch('requests.get')
def test_detect_text_invalid_url(mock_get, text_detector):
    mock_get.side_effect = Exception("Invalid URL")

    with pytest.raises(Exception):
        text_detector.detect_text("invalid_url")
