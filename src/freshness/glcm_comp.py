import matplotlib.pyplot as plt
import skimage
from skimage import io, color, feature
import cv2
import os
import numpy as np

class ImageProcessor:
    def __init__(self, image_path, patch_size=35):
        self.PATCH_SIZE = patch_size
        self.image = self.load_and_preprocess_image(image_path)
        self.rows, self.cols = self.image.shape
        print(f"Image dimensions: {self.rows} x {self.cols}")

    def load_and_preprocess_image(self, image_path):
        image = io.imread(image_path)
        image = color.rgb2gray(image)
        return (image * 255).astype(np.uint8)

    def compute_full_image_glcm(self):
        GLCM = feature.graycomatrix(self.image, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4])
        return feature.graycoprops(GLCM, 'energy')[0, 0]

    def get_patch(self, loc):
        if loc[0] + self.PATCH_SIZE <= self.rows and loc[1] + self.PATCH_SIZE <= self.cols:
            return self.image[loc[0]:loc[0] + self.PATCH_SIZE, loc[1]:loc[1] + self.PATCH_SIZE]
        else:
            print(f"Patch at {loc} is out of bounds.")
            return None

    def get_patches(self, locations):
        return [self.get_patch(loc) for loc in locations if self.get_patch(loc) is not None]

    def compute_glcm_properties(self, patches):
        properties = {
            'dissimilarity': [],
            'correlation': [],
            'homogeneity': [],
            'energy': [],
            'contrast': []
        }
        
        for patch in patches:
            glcm = feature.graycomatrix(patch, distances=[5], angles=[0], levels=256,
                                        symmetric=True, normed=True)
            for prop in properties:
                properties[prop].append(feature.graycoprops(glcm, prop)[0, 0])
        
        return properties

    def plot_results(self, cell_locations, scratch_locations, cell_patches, scratch_patches, properties):
        fig = plt.figure(figsize=(8, 8))

        # Original image with patch locations
        ax = fig.add_subplot(3, 2, 1)
        ax.imshow(self.image, cmap=plt.cm.gray, vmin=0, vmax=255)
        for (y, x) in cell_locations:
            ax.plot(x + self.PATCH_SIZE / 2, y + self.PATCH_SIZE / 2, 'gs')
        for (y, x) in scratch_locations:
            ax.plot(x + self.PATCH_SIZE / 2, y + self.PATCH_SIZE / 2, 'bs')
        ax.set_xlabel('Original Image')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('image')

        # GLCM properties plot
        ax = fig.add_subplot(3, 2, 2)
        ax.plot(properties['dissimilarity'][:len(cell_patches)], 
                properties['correlation'][:len(cell_patches)], 'go', label='Cells')
        ax.plot(properties['dissimilarity'][len(cell_patches):], 
                properties['correlation'][len(cell_patches):], 'bo', label='Scratch')
        ax.set_xlabel('GLCM Dissimilarity')
        ax.set_ylabel('GLCM Correlation')
        ax.legend()

        # Display cell patches
        for i, patch in enumerate(cell_patches):
            ax = fig.add_subplot(3, len(cell_patches), len(cell_patches)*1 + i + 1)
            ax.imshow(patch, cmap=plt.cm.gray, vmin=0, vmax=255)
            ax.set_xlabel(f'Cells {i + 1}')

        # Display scratch patches
        for i, patch in enumerate(scratch_patches):
            ax = fig.add_subplot(3, len(scratch_patches), len(scratch_patches)*2 + i + 1)
            ax.imshow(patch, cmap=plt.cm.gray, vmin=0, vmax=255)
            ax.set_xlabel(f'Scratch {i + 1}')

        fig.suptitle('Gray Level Co-occurrence Matrix Features', fontsize=14, y=1.05)
        plt.tight_layout()
        plt.show()


