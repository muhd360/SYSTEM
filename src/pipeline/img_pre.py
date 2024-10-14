import numpy as np
import pytesseract
import cv2
import imutils
import os

class OCRImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None
        self.gray = None
        self.thresh = None
        self.dist = None
        self.opening = None
        self.mask = None
        self.final = None
        self.output_dir = "output_images"

    def load_image(self):
        self.image = cv2.imread(self.image_path)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def apply_otsu_threshold(self):
        self.thresh = cv2.threshold(self.gray, 0, 255,
                                    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    def apply_distance_transform(self):
        dist = cv2.distanceTransform(self.thresh, cv2.DIST_L2, 5)
        dist = cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
        self.dist = (dist * 255).astype("uint8")
        self.dist = cv2.threshold(self.dist, 0, 255,
                                  cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    def apply_morphological_operations(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        self.opening = cv2.morphologyEx(self.dist, cv2.MORPH_OPEN, kernel)

    def find_character_contours(self):
        cnts = cv2.findContours(self.opening.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        chars = []
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            if w >= 35 and h >= 100:
                chars.append(c)
        return chars

    def create_convex_hull_mask(self, chars):
        chars = np.vstack([chars[i] for i in range(0, len(chars))])
        hull = cv2.convexHull(chars)
        self.mask = np.zeros(self.image.shape[:2], dtype="uint8")
        cv2.drawContours(self.mask, [hull], -1, 255, -1)
        self.mask = cv2.dilate(self.mask, None, iterations=2)

    def apply_final_mask(self):
        self.final = cv2.bitwise_and(self.opening, self.opening, mask=self.mask)

    def process_image(self):
        self.load_image()
        self.apply_otsu_threshold()
        self.apply_distance_transform()
        self.apply_morphological_operations()
        chars = self.find_character_contours()
        self.create_convex_hull_mask(chars)
        self.apply_final_mask()

    def save_results(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        cv2.imwrite(os.path.join(self.output_dir, "original.png"), self.image)
        cv2.imwrite(os.path.join(self.output_dir, "otsu.png"), self.thresh)
        cv2.imwrite(os.path.join(self.output_dir, "dist.png"), self.dist)
        cv2.imwrite(os.path.join(self.output_dir, "opening.png"), self.opening)
        cv2.imwrite(os.path.join(self.output_dir, "mask.png"), self.mask)
        cv2.imwrite(os.path.join(self.output_dir, "final.png"), self.final)
        
        print(f"Results saved in the '{self.output_dir}' directory.")

def process_image(image_path):
    processor = OCRImageProcessor(image_path)
    processor.process_image()
    processor.save_results()

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="path to input image to be OCR'd")
    args = vars(ap.parse_args())
    process_image(args["image"])
