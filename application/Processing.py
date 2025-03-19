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
        self. result_list = [-1,-1,-1,-1,-1,-1]
        
    def detect_face(self,frame):
        """ 현재 프레임을 캡처하여 저장 """
        self.cropped_face = None
        x1, y1, x2, y2 = 0,0,0,0

        results = ncnn_model.predict(frame, max_det=1, imgsz=128, conf=0.3, verbose=False)
        for i, r in enumerate(results):
            for box in r.boxes.xyxy:  # bounding box (x1, y1, x2, y2)
                x1, y1, x2, y2 = map(int, box)
                upper_margin = 0
                y1 = max(0, y1-upper_margin)
        return x1, y1, x2, y2

    def softmax_with_temperature(self, logits, temperature=1.0):

        logits = np.array(logits)

        scaled_logits = logits / temperature

        exp_values = np.exp(scaled_logits - np.max(scaled_logits))

        return exp_values / np.sum(exp_values)
    
    # 캡쳐된 jpg 파일을 받아서 classification 하고 6개짜리 리스트를 출력
    def classification(self, cropped_frames):
        output = np.array([0.11, 0.175, 0.1675, 0.15, 0.30, 0.12])

        arr = np.zeros(6)
        count = 0

        for cropped_frame in cropped_frames:
            ex = net.create_extractor()
            cropped_frame_resized = cv2.resize(cropped_frame, (128, 128), interpolation=cv2.INTER_LINEAR)
            cropped_frame_ncnn = ncnn.Mat.from_pixels(cropped_frame_resized, ncnn.Mat.PixelType.PIXEL_RGB, 128, 128)
            mean_vals = [0.5 * 255, 0.5 * 255, 0.5 * 255] 
            norm_vals = [1 / (0.5 * 255), 1 / (0.5 * 255), 1 / (0.5 * 255)]
            cropped_frame_ncnn.substract_mean_normalize(mean_vals, norm_vals)
            # NCNN input
            ex.input("in0", cropped_frame_ncnn)
            ret, output = ex.extract("out1") 
            output_np = np.array(output)
            temperature = 3.5
            output = self.softmax_with_temperature(output_np, temperature)
            print("output ", output_np)
            count += 1
            arr += output

        if count != 0:
            arr /= count
            return arr

        return output