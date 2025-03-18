import pickle  
import numpy as np
import face_recognition
import cv2
import os
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

class Celebrity :
    def __init__(self) -> None:
        # ✅ 저장된 벡터 데이터 불러오기
        with open("/home/willtek/Bootcamp/application/resources/face_encodings.pkl", "rb") as f:
            self.stored_encodings, self.stored_names = pickle.load(f)

    def guess(self):
        # ✅ 입력 이미지 얼굴 벡터 추출
        input_image = face_recognition.load_image_file("/home/willtek/Bootcamp/application/captured_frame_original.jpg")
        face_locations = face_recognition.face_locations(input_image)
        print(f"감지된 얼굴 개수: {len(face_locations)}")

        input_encoding = face_recognition.face_encodings(input_image, face_locations)

        if input_encoding:
            input_encoding = input_encoding[0]

        else:
            input_image = cv2.imread("/home/willtek/Bootcamp/application/captured_frame.jpg")  # 이미지 로드
            input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)  # BGR → RGB 변환 (face_recognition 호환)
            height, width, _ = input_image.shape

            # ✅ 이미지 전체를 얼굴 영역으로 지정
            full_image_location = [(0, width, height, 0)]  # (top, right, bottom, left)

            # avg_color = np.mean(input_image, axis=(0, 1))  # (R, G, B) 평균
            # input_encoding = np.tile(avg_color / 255.0, (128 // 3 + 1))[:128]  # 128차원으로 확장
            input_encoding = face_recognition.face_encodings(input_image, full_image_location)
            input_encoding = input_encoding[0]
            # input_encoding = avg_color / 255.0  # 0~1 사이로 정규화
            # print("❌ 얼굴을 찾을 수 없습니다.")
            print("???")
            # return -1, None
    
        # ✅ 거리 계산 (유클리드 거리)
        distances = np.linalg.norm(self.stored_encodings - input_encoding, axis=1)
    
        # ✅ 가장 가까운 얼굴 찾기
        best_match_idx = np.argmin(distances)
        matched_name = self.stored_names[best_match_idx]
    
        print("가장 유사한 연예인:", matched_name)

        # ✅ 다양한 확장자로 파일 찾기
        celebrity_folder = "/home/willtek/Bootcamp/application/resources/celebrity_faces/"
        image_extensions = [".jpg", ".jpeg", ".png", ".jfif", ".webp", ".bmp", ".tiff"]

        matched_image_path = None
        for ext in image_extensions:
            temp_path = os.path.join(celebrity_folder, f"{matched_name}{ext}")
            if os.path.exists(temp_path):
                matched_image_path = temp_path
                break
        
        return matched_name, matched_image_path