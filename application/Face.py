import numpy as np
import face_recognition
import pickle



# ✅ 저장된 벡터 데이터 불러오기 (라즈베리파이에서 실행)
with open("/home/willtek/Bootcamp/application/resources/face_encodings.pkl", "rb") as f:
    stored_encodings, stored_names = pickle.load(f)

# ✅ 입력 이미지 얼굴 벡터 추출
input_image = face_recognition.load_image_file("/home/willtek/Bootcamp/application/captured_frame_original.jpg")
face_locations = face_recognition.face_locations(input_image)  # 얼굴 위치 찾기
print(f"감지된 얼굴 개수: {len(face_locations)}")

input_encoding = face_recognition.face_encodings(input_image, face_locations)
# input_encoding = face_recognition.face_encodings(input_image)

if input_encoding:
    input_encoding = input_encoding[0]
    
    # ✅ 거리 계산 (유클리드 거리)
    distances = np.linalg.norm(stored_encodings - input_encoding, axis=1)
    
    # ✅ 가장 가까운 얼굴 찾기
    best_match_idx = np.argmin(distances)
    matched_name = stored_names[best_match_idx]
    
    print("가장 유사한 연예인:", matched_name)
else:
    print("❌ 얼굴을 찾을 수 없습니다.")