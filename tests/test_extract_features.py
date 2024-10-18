import numpy as np
import pytest
from unittest.mock import patch, MagicMock
from extract_features import FeatureExtractor

@pytest.fixture
def feature_extractor():
    return FeatureExtractor()

@patch('requests.get')
@patch('PIL.Image.open')
@patch('tensorflow.keras.applications.mobilenet_v2.preprocess_input')
def test_preprocess_image(mock_preprocess_input, mock_image_open, mock_get, feature_extractor):
    mock_response = MagicMock()
    mock_response.content = b'fake image content'
    mock_get.return_value = mock_response

    mock_image = MagicMock()
    mock_image.convert.return_value = mock_image
    mock_image.resize.return_value = mock_image
    mock_image_open.return_value = mock_image

    mock_preprocess_input.return_value = np.array([1, 2, 3])

    result = feature_extractor.preprocess_image("http://example.com/image.jpg")

    assert isinstance(result, np.ndarray)
    mock_get.assert_called_once_with("http://example.com/image.jpg")
    mock_image_open.assert_called_once()
    mock_image.convert.assert_called_once_with('RGB')
    mock_image.resize.assert_called_once_with((224, 224))
    mock_preprocess_input.assert_called_once()

@patch.object(FeatureExtractor, 'preprocess_image')
def test_extract_features(mock_preprocess_image, feature_extractor):
    mock_preprocess_image.return_value = np.array([[[1, 2, 3]]])
    
    with patch.object(feature_extractor.model, 'predict') as mock_predict:
        mock_predict.return_value = np.array([[[4, 5, 6]]])
        
        result = feature_extractor.extract_features("http://example.com/image.jpg")
        
        assert isinstance(result, np.ndarray)
        np.testing.assert_array_equal(result, np.array([[[4, 5, 6]]]))
        mock_preprocess_image.assert_called_once_with("http://example.com/image.jpg")
        mock_predict.assert_called_once()
