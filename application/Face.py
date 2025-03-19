import pickle  
import numpy as np
import face_recognition
import cv2
import os
from PyQt5.QtCore import QThread, pyqtSignal

class Celebrity(QThread) :
    finished_signal = pyqtSignal(dict)  # 완료 신호 (응답 데이터 전달)
    def __init__(self) -> None:
        # ✅ 저장된 벡터 데이터 불러오기
        with open("/home/willtek/Bootcamp/application/resources/face_encodings.pkl", "rb") as f:
            self.stored_encodings, self.stored_names = pickle.load(f)
            
    def get_average_point(points):
        """ 주어진 랜드마크 포인트들의 평균 좌표를 반환 """
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        return (np.mean(x_coords), np.mean(y_coords))
    
    def classify_face_type(face_landmarks):
        """ 얼굴 랜드마크를 기반으로 6가지 유형 중 하나로 분류 """

        # 랜드마크에서 특정 부위 추출
        left_eye = face_landmarks['left_eye']
        right_eye = face_landmarks['right_eye']
        left_eyebrow = face_landmarks['left_eyebrow']
        right_eyebrow = face_landmarks['right_eyebrow']
        chin = face_landmarks['chin']
        nose_bridge = face_landmarks['nose_bridge']
        nose_tip = face_landmarks['nose_tip']

        # 주요 포인트 계산
        A = get_average_point([chin[0], chin[-1]])  # 헤어라인 (추정)
        Q = chin[len(chin) // 2]  # 턱 중앙
        F = get_average_point([left_eye[0], right_eye[0]])  # 두 눈 앞머리 평균
        C = get_average_point([left_eyebrow[0], right_eyebrow[0]])  # 눈썹 앞머리 평균
        D = get_average_point([left_eyebrow[2], right_eyebrow[2]])  # 눈썹산
        E = get_average_point([left_eyebrow[-1], right_eyebrow[-1]])  # 눈썹 꼬리
        R = get_average_point([left_eye[1], right_eye[1]])  # 눈 위 지점
        H = get_average_point([left_eye[-1], right_eye[-1]])  # 눈꼬리
        I = get_average_point([chin[5], chin[-6]])  # 광대뼈 중앙

        # 얼굴 주요 비율 계산
        eye_slant = (H[1] - F[1]) / max(abs(H[0] - F[0]), 1)  # 눈매 기울기
        jaw_ratio = abs(A[1] - Q[1]) / max(abs(A[0] - Q[0]), 1)  # 턱선 비율
        face_width = abs(chin[0][0] - chin[-1][0])  # 얼굴 너비
        face_length = abs(A[1] - Q[1])  # 얼굴 길이
        face_ratio = face_length / max(face_width, 1)  # 얼굴 길이 대비 너비 비율

        # 얼굴형 분류
        if eye_slant > 0.2 and jaw_ratio > 0.5:
            return "고양이상"
        elif 0.8 <= face_ratio <= 1.2 and 0.4 <= jaw_ratio <= 0.6:
            return "황제상"
        elif face_ratio < 0.9 and jaw_ratio < 0.4:
            return "너구리상"
        elif eye_slant < -0.1 and face_ratio > 1.2:
            return "구렁이상"
        elif 1.0 <= face_ratio <= 1.3 and jaw_ratio >= 0.5:
            return "이리상"
        else:
            return "호랑이상"
    def guess(self):
        # ✅ 입력 이미지 얼굴 벡터 추출
        input_image = face_recognition.load_image_file("/home/willtek/Bootcamp/application/captured_frame_original.jpg")
        face_locations = face_recognition.face_locations(input_image)
        print(f"감지된 얼굴 개수: {len(face_locations)}")

        input_encoding = face_recognition.face_encodings(input_image, face_locations)
        face_landmarks_list = face_recognition.face_landmarks(input_image)

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