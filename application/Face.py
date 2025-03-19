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
    # def get_average_point(points):
    #     """ 주어진 랜드마크 포인트들의 평균 좌표를 반환 """
    #     x_coords = [p[0] for p in points]
    #     y_coords = [p[1] for p in points]
    #     return (np.mean(x_coords), np.mean(y_coords))
    
    def classify_face_type(self,face_landmarks):
        # 주요 포인트 가져오기
        A = np.mean(np.array(face_landmarks['top_lip']), axis=0)  # 헤어라인 중심
        Q = np.mean(np.array(face_landmarks['bottom_lip']), axis=0)  # 턱 중심
        C = np.mean(np.array(face_landmarks['left_eyebrow'][:2] + face_landmarks['right_eyebrow'][:2]), axis=0)  # 눈썹 앞머리 평균
        D = np.mean(np.array(face_landmarks['left_eyebrow'][2:4] + face_landmarks['right_eyebrow'][2:4]), axis=0)  # 눈썹 산 평균
        E = np.mean(np.array(face_landmarks['left_eyebrow'][4:] + face_landmarks['right_eyebrow'][4:]), axis=0)  # 눈썹 꼬리 평균
        F = np.mean(np.array(face_landmarks['left_eye'][:2] + face_landmarks['right_eye'][:2]), axis=0)  # 눈 앞머리 평균
        H = np.mean(np.array(face_landmarks['left_eye'][3:] + face_landmarks['right_eye'][3:]), axis=0)  # 눈 꼬리 평균
        I = np.mean(np.array(face_landmarks['chin'][7:10]), axis=0)  # 광대뼈 위치
        R = np.mean(np.array(face_landmarks['nose_bridge']), axis=0)  # 눈 위(코 시작점)
        
        # 거리 및 비율 계산
        face_length = np.linalg.norm(A - Q)
        face_width = np.linalg.norm(np.array(face_landmarks['chin'][0]) - np.array(face_landmarks['chin'][-1]))
        eye_length = np.linalg.norm(F - H)
        eyebrow_curve = np.linalg.norm(C - D) + np.linalg.norm(D - E)
        eye_eyebrow_gap = np.linalg.norm(R - H)
        cheekbone_width = np.linalg.norm(np.array(face_landmarks['chin'][2]) - np.array(face_landmarks['chin'][-3]))
        
        # 분류 기준 적용
        if eye_length > face_width * 0.3 and eyebrow_curve > face_width * 0.15 and eye_eyebrow_gap < face_length * 0.1:
            return "고양이상"
        elif face_length > face_width * 1.3 and Q[1] < I[1]:
            return "황제상"
        elif face_length < face_width * 1.1 and eye_length > face_width * 0.25:
            return "너구리상"
        elif eye_length < face_width * 0.2 and eyebrow_curve > face_width * 0.2 and cheekbone_width > face_width * 0.5:
            return "구렁이상"
        elif cheekbone_width > face_width * 0.6 and face_length > face_width * 1.2:
            return "이리상"
        else:
            return "호랑이상"
        
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
            face_landmarks_list = face_recognition.face_landmarks(input_image)
            if face_landmarks_list:
                face_type = self.classify_face_type(face_landmarks_list[0])
                print("얼굴 유형:", face_type)
            else:
                print("얼굴을 찾을 수 없습니다.")
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