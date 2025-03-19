import os
import cv2
import numpy as np
import face_recognition
import pickle
from PyQt5.QtCore import QThread, pyqtSignal, QMutex
from PIL import Image

class FaceRecognitionThread(QThread):
    result_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        with open("/home/willtek/Bootcamp/application/resources/face_encodings.pkl", "rb") as f:
            self.stored_encodings, self.stored_names = pickle.load(f)
        self.frames = None
        self.mutex = QMutex()

    def set_frame(self, frames):
        """ 새로운 프레임을 설정하고 스레드를 실행 """
        self.mutex.lock()
        self.frames = frames
        self.mutex.unlock()
        
        if not self.isRunning():
            self.start()

    def run(self):
        """ 프레임이 설정될 때만 실행 """
        self.mutex.lock()
        frames = self.frames
        self.mutex.unlock()
        
        if len(frames) != 0:
            matched_name, matched_image_path, landmark = self.recognize_face(frames)
            self.result_signal.emit({
                "matched_name" : matched_name,
                "matched_image_path" : matched_image_path,
                "landmark": landmark
            })

    def draw_landmarks(self, face_landmarks, frame):
        # 프레임 크기 가져오기
        h, w, _ = frame.shape

        # 랜드마크를 위한 흰 배경 생성
        landmark = np.full((h, w, 3), (255, 192, 203), dtype=np.uint8)

        # 모든 랜드마크 좌표를 리스트로 변환
        all_points = np.array([point for points in face_landmarks.values() for point in points])

        # 중심 좌표 계산
        center_x = np.mean(all_points[:, 0])
        center_y = np.mean(all_points[:, 1])

        # 새로운 중심 좌표 (이미지의 중앙)
        new_center_x = w // 2
        new_center_y = h // 2

        # 기존 중심을 기준으로 조정된 좌표 계산
        adjusted_landmarks = {
            feature: [(int(x - center_x + new_center_x), int(y - center_y + new_center_y)) for x, y in points]
            for feature, points in face_landmarks.items()
        }

        # 조정된 좌표로 랜드마크 그리기
        for feature, points in adjusted_landmarks.items():
            for point in points:
                cv2.circle(landmark, point, 5, (0, 0, 255), -1)

        # 저장 및 반환
        # cv2.imwrite("/home/willtek/Bootcamp/application/captured_frame_centered.jpg", landmark)
        return landmark
        
    def recognize_face(self, frames):
        """
        실시간 프레임을 입력받아 얼굴을 인식하고 가장 유사한 연예인을 찾는 함수.
        :param frame: OpenCV 프레임 (numpy.ndarray)
        :return: (matched_name, matched_image_path)
        """
        arr = np.zeros(100)
        landmark = None

        for frame in frames:
            input_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(input_image)
            face_landmarks_list = face_recognition.face_landmarks(input_image)
            if face_landmarks_list and landmark is None:
                landmark = self.draw_landmarks(face_landmarks_list[0], input_image)
                # print("얼굴 유형:", face_type)
            # else:
                # print("얼굴을 찾을 수 없습니다.")
            # print(f"감지된 얼굴 개수: {len(face_locations)}")

            input_encoding = face_recognition.face_encodings(input_image, face_locations)
            if input_encoding:
                input_encoding = input_encoding[0]
            else:
                height, width, _ = input_image.shape
                full_image_location = [(0, width, height, 0)]
                input_encoding = face_recognition.face_encodings(input_image, full_image_location)
                if input_encoding:
                    input_encoding = input_encoding[0]
                else:
                    print("❌ 얼굴을 찾을 수 없습니다.")
                    continue

                if len(self.stored_encodings) == 0:
                    print("❌ 저장된 얼굴 데이터가 없습니다.")
                    return None, None, None

            distances = np.linalg.norm(self.stored_encodings - input_encoding, axis=1)
            best_match_idx = np.argmin(distances)
            matched_name = self.stored_names[best_match_idx]
            print("가장 유사한 연예인:", matched_name)
            arr[best_match_idx] += 1
        
        best_match_idx = np.argmax(arr)
        matched_name = self.stored_names[best_match_idx]
        celebrity_folder = "/home/willtek/Bootcamp/application/resources/celebrity_faces/"
        image_extensions = [".jpg", ".jpeg", ".png", ".jfif", ".webp", ".bmp", ".tiff"]

        matched_image_path = None
        for ext in image_extensions:
            temp_path = os.path.join(celebrity_folder, f"{matched_name}{ext}")
            if os.path.exists(temp_path):
                matched_image_path = temp_path
                if ext == ".webp" :
                    png_path = os.path.splitext(matched_image_path)[0] + ".png"
                    img = Image.open(matched_image_path)
                    img.save(png_path, "PNG")
                    matched_image_path = png_path
                break

        if not matched_image_path:
            print("⚠️ 해당 연예인 이미지가 없습니다. 기본 이미지 사용.")
            matched_image_path = "/home/willtek/Bootcamp/application/resources/default_image.jpg"
        
        self.landmark = None
        return matched_name, matched_image_path, landmark