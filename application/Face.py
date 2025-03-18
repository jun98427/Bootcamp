import pickle  
import numpy as np
import face_recognition
import cv2
import os
from PIL import Image
import matplotlib.pyplot as plt

# ✅ 저장된 벡터 데이터 불러오기
with open("/home/willtek/Bootcamp/application/resources/face_encodings.pkl", "rb") as f:
    stored_encodings, stored_names = pickle.load(f)

# ✅ 입력 이미지 얼굴 벡터 추출
input_image = face_recognition.load_image_file("/home/willtek/Bootcamp/application/captured_frame_original.jpg")
face_locations = face_recognition.face_locations(input_image)
print(f"감지된 얼굴 개수: {len(face_locations)}")

input_encoding = face_recognition.face_encodings(input_image, face_locations)

if input_encoding:
    input_encoding = input_encoding[0]
    
    # ✅ 거리 계산 (유클리드 거리)
    distances = np.linalg.norm(stored_encodings - input_encoding, axis=1)
    
    # ✅ 가장 가까운 얼굴 찾기
    best_match_idx = np.argmin(distances)
    matched_name = stored_names[best_match_idx]
    
    print("가장 유사한 연예인:", matched_name)

    # ✅ 다양한 확장자로 파일 찾기
    celebrity_folder = "/home/willtek/Bootcamp/application/resources/celebrity_faces/"
    image_extensions = [".jpg", ".jpeg", ".png", ".jfif", ".webp", ".bmp", ".tiff"]

    matched_image_path = None
    for ext in image_extensions:
        temp_path = os.path.join(celebrity_folder, f"{matched_name}{ext}")
        print("2")
        if os.path.exists(temp_path):
            matched_image_path = temp_path
            print("1")
            break
    
    if matched_image_path:
        # ✅ OpenCV 대신 PIL + Matplotlib 사용 (한글 경로 문제 해결)
        img = Image.open(matched_image_path)
        img = np.array(img)
        
        plt.imshow(img)
        plt.axis("off")
        plt.title(f"가장 유사한 연예인: {matched_name}", fontproperties="AppleGothic")  # 한글 지원 폰트 설정
        plt.show()

    else:
        print("❌ 해당 연예인의 사진 파일을 찾을 수 없습니다.")

else:
    print("❌ 얼굴을 찾을 수 없습니다.")
