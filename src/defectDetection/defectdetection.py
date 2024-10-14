import subprocess
class BKC:
    def __init__(self, model_path, model_type, device):
        self.model_path = model_path
        self.model_type = model_type
        self.device = device
        self.model = self.load_model()
    def call_cpp():
        #if want to build the cpp file- g++ -o DefectDetectionTop5 DefectDetectionTop5.cpp `pkg-config --cflags --libs opencv4`
        #./DefectDetectionTop5 /path/to/your/image.jpg /path/to/save/result.jpg 100 50
        '''
        <input_image_path>: Path to your local image file
        <output_image_path>: Where you want the result image to be saved
        <field_width_mm>: The actual width of the area being inspected, in millimeters
        <min_defect_size_mm>: Minimum size of defects to detect, in millimeters
        <tolerance> (optional): Tolerance factor for defect detection (default is 3)
        <threshold> (optional): Threshold for image binarization (default is 50)
        '''
        input_img, output_img = "input.jpg", "output.jpg"
        WIDTH,min_def = 100,10
        subprocess.run(["./my_program1", input_img, output_img, str(WIDTH), str(min_def)])
        