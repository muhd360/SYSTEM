from src.feature_Nlysis.ImageProcessor import ImageProcessor
import os


class postprocessor:

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
    
    def plot_img(image_path):
        processor = ImageProcessor(image_path)
        full_image_glcm = processor.compute_full_image_glcm()
        print(f"Full image GLCM energy: {full_image_glcm}")

        # Define patch locations
        cell_locations = [(50, 50), (100, 100)]
        scratch_locations = [(50, 200), (150, 200), (250, 150), (200, 200)]

        # Get patches
        cell_patches = processor.get_patches(cell_locations)
        scratch_patches = processor.get_patches(scratch_locations)

        # Compute GLCM properties
        all_patches = cell_patches + scratch_patches
        properties = processor.compute_glcm_properties(all_patches)

        # Plot results
        processor.plot_results(cell_locations, scratch_locations, cell_patches, scratch_patches, properties)

 