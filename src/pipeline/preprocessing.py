import requests
from rembg import remove
import os

class PreProcessor:
    def __init__(self, image_folder, output_folder):
        self.image_folder = image_folder
        self.output_folder = output_folder

    def get_latest_image(self):
        files = [f for f in os.listdir(self.image_folder) if os.path.isfile(os.path.join(self.image_folder, f))]
        image_extensions = ['.jpg', '.jpeg', '.png']
        images = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]
        
        if not images:
            return None
        
        latest_image = max(images, key=lambda f: os.path.getmtime(os.path.join(self.image_folder, f)))
        return os.path.join(self.image_folder, latest_image)

    def remove_background(self, image_path):
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
        
        try:
            output_filename = os.path.splitext(os.path.basename(image_path))[0] + "_no_bg.png"
            output_path = os.path.join(self.output_folder, output_filename)
            
            with open(output_path, 'wb') as f:
                R = remove(image_data)
                f.write(R)
            
            print(f"Background removed image saved at {output_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error removing background: {e}")

    def run_background_removal_pipeline(self):
        latest_image_path = self.get_latest_image()
        if latest_image_path:
            print(f"Processing latest image: {latest_image_path}")
            self.remove_background(latest_image_path)
        else:
            print("No images found in the folder.")