import ncnn
import numpy as np
import cv2
import Camera as cap
from ultralytics import YOLO
# Load face detection model
ncnn_model = YOLO("/home/willtek/Bootcamp/face_det_ncnn_model/")

# Load face classification model
net = ncnn.Net()
param_path = "/home/willtek/Bootcamp/face_cls_ncnn_model/best_yolov11n_model.ncnn.param"
bin_path = "/home/willtek/Bootcamp/face_cls_ncnn_model/best_yolov11n_model.ncnn.bin"
net.load_param(param_path)
net.load_model(bin_path)

class Processing :
    def __init__(self):
        self.cropped_face = None
        self. result_list = [-1,-1,-1,-1,-1,-1]
        self.last_jpg_file = None
        
    def detect_face(self,frame):
        """ 현재 프레임을 캡처하여 저장 """
        self.cropped_face = None
        x1, y1, x2, y2 = 0,0,0,0
        # results = ncnn_model(frame, max_det=1, imgsz=128, conf=0.3)
        results = ncnn_model.predict(frame, max_det=1, imgsz=128, conf=0.3, verbose=False)
        for i, r in enumerate(results):
            for box in r.boxes.xyxy:  # bounding box (x1, y1, x2, y2)
                x1, y1, x2, y2 = map(int, box)
                upper_margin = 0
                y1 = max(0, y1-upper_margin)
                self.cropped_face = frame[y1:y2, x1:x2]
        return x1, y1, x2, y2

    def softmax_with_temperature(self, logits, temperature=1.0):

        logits = np.array(logits)

        scaled_logits = logits / temperature

        exp_values = np.exp(scaled_logits - np.max(scaled_logits))

        return exp_values / np.sum(exp_values)
    
    # 캡쳐된 jpg 파일을 받아서 classification 하고 6개짜리 리스트를 출력
    def classification_jpg(self):
        jpg_file = cv2.imread("captured_frame.jpg")
        if jpg_file is None:
            print("이미지를 불러오지 못했습니다. 파일 경로를 확인하세요!")
        else:
            print("이미지 로드 성공!")
        if not np.array_equal(jpg_file, self.last_jpg_file):
            # cv2.imread("captured_frame.jpg", jpg_file)
            self.result_list = [-1,-1,-1,-1,-1,-1]
            ex = net.create_extractor()
            cropped_face_resized = cv2.resize(jpg_file, (128, 128), interpolation=cv2.INTER_LINEAR)
            # RGB to NCNN Mat
            cropped_face_ncnn = ncnn.Mat.from_pixels(cropped_face_resized, ncnn.Mat.PixelType.PIXEL_RGB, 128, 128)
            # Normalize
            mean_vals = [0.5 * 255, 0.5 * 255, 0.5 * 255] 
            norm_vals = [1 / (0.5 * 255), 1 / (0.5 * 255), 1 / (0.5 * 255)]
            cropped_face_ncnn.substract_mean_normalize(mean_vals, norm_vals)
            # NCNN input
            ex.input("in0", cropped_face_ncnn)

            ret, output = ex.extract("out1")
            output_np = np.array(output)
            temperature = 3.5
            output = self.softmax_with_temperature(output_np, temperature)
            
            self.last_jpg_file = jpg_file
        return output