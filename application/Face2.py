import os
import cv2
import numpy as np
import face_recognition
import pickle
from PyQt5.QtCore import QThread, pyqtSignal, QMutex

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
            matched_name, matched_image_path = self.recognize_face(frames)
            self.result_signal.emit({
                "matched_name" : matched_name,
                "matched_image_path" : matched_image_path
            })

    def recognize_face(self, frames):
        """
        실시간 프레임을 입력받아 얼굴을 인식하고 가장 유사한 연예인을 찾는 함수.
        :param frame: OpenCV 프레임 (numpy.ndarray)
        :return: (matched_name, matched_image_path)
        """
        arr = np.zeros(100)
        for frame in frames:
            input_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(input_image)
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
                    return None, None

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
                break

        if not matched_image_path:
            print("⚠️ 해당 연예인 이미지가 없습니다. 기본 이미지 사용.")
            matched_image_path = "/home/willtek/Bootcamp/application/resources/default_image.jpg"

        return matched_name, matched_image_path