import numpy as np
from PIL import Image
import requests
from io import BytesIO
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array

class FeatureExtractor:
    def __init__(self):
        self.model = MobileNetV2(weights='imagenet', include_top=False)

    def preprocess_image(self, image_url):
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        img = img.convert('RGB')
        img = img.resize((224, 224))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        return img_array

    def extract_features(self, image_url):
        preprocessed_image = self.preprocess_image(image_url)
        features = self.model.predict(preprocessed_image)
        return features
