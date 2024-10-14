import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
import requests
from rembg import remove

# Define the folder where the images are located
image_folder = "/home/muhd/Desktop/GRID/images/box"
output_folder = "/home/muhd/Desktop/GRID/images/box/box_remove"

# Ensure output folder exists
if not os.path.exists(output_folder):
    print("not exist")


# Function to get the latest image from the folder
def get_latest_image(folder_path):
    # List all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Filter out non-image files (basic check for jpg, png, etc.)
    image_extensions = ['.jpg', '.jpeg', '.png']
    images = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]

    # If no images found, return None
    if not images:
        return None

    # Get the latest image by modification time
    latest_image = max(images, key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
    return os.path.join(folder_path, latest_image)

# Function to remove background from an image
def remove_background(image_path):

    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    
    try:

        
        # Generate output filename
        output_filename = os.path.splitext(os.path.basename(image_path))[0] + "_no_bg.png"
        output_path = os.path.join(output_folder, output_filename)
        
        # Save the result (background-removed image)
        with open(output_path, 'wb') as f:
            R=remove(image_data)
            f.write(R)
        
        print(f"Background removed image saved at {output_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error removing background: {e}")
# Main pipeline function
def background_removal_pipeline():
    # Fetch the latest image from the folder
    latest_image_path = get_latest_image(image_folder)
    
    if latest_image_path:
        print(f"Processing latest image: {latest_image_path}")
        # Perform background removal
        remove_background(latest_image_path)
    else:
        print("No images found in the folder.")

# Run the pipeline
if __name__ == "__main__":
    background_removal_pipeline()
