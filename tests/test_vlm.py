import pytest
from unittest.mock import patch, MagicMock
from vlm import VisionLanguageModel

@pytest.fixture
def vision_language_model():
    return VisionLanguageModel()

@patch('fal_client.subscribe')
def test_describe_image(mock_subscribe, vision_language_model):
    mock_result = MagicMock()
    mock_result.output = "This is a description of the image."
    mock_subscribe.return_value = mock_result

    result = vision_language_model.describe_image("http://example.com/image.jpg")

    assert result == "This is a description of the image."
    mock_subscribe.assert_called_once_with(
        "fal-ai/any-llm/vision",
        arguments={
            "model": "google/gemini-flash-1.5-8b",
            "prompt": "Describe this product image in detail, including any visible text, logos, or packaging information.",
            "system_prompt": "Provide a concise but detailed description of the product image.",
            "image_url": "http://example.com/image.jpg",
        },
        with_logs=False,
    )
