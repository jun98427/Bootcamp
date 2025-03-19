from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QPainterPath, QFont, QMovie, QTransform, QTextDocument, QFontDatabase
from PyQt5.QtCore import Qt, QTimer, QPointF, QRect, QRectF, QFile, QTextStream
import math
import Camera as cap
import Processing as pro
import Api as req
import sys
import cv2
import numpy as np
import random
import HexagonChart as hexa
import Inference as infer
import os
import Face as face

delete_jpg_file = "/home/willtek/Bootcamp/application/captured_frame.jpg"
delete_jpg_file2 = "/home/willtek/Bootcamp/application/captured_frame_original.jpg"

font_path = "/home/willtek/Bootcamp/application/resources/concon_font.ttf"


colorList = {
    'red': QColor(255, 0, 0),
    'green': QColor(0, 255, 0),
    'white': QColor(255, 255, 255),
    'black': QColor(0, 0, 0),
    'pink': QColor(255, 192, 203),
    'navy': QColor(30, 58, 95),
    'yellow': QColor(255, 255, 0),
    'light_yellow': QColor(255, 255, 150),
    'gray': QColor(128, 128, 128),
}

#리더십 매력 신뢰도 피지컬 예술 지능
skills_calk = [
    [95, 80, 92.5, 67.5, 70, 90],
    [77.5, 87.5, 85, 62.5, 80, 77.5],
    [72.5, 80, 90, 62.5, 65, 82.5],
    [75, 80, 85, 95, 50, 70],
    [77.5, 77.5, 80, 55, 92.5, 85],
    [77.5, 65, 92.5, 65, 50, 90]
]

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()

        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print("❌ 폰트 로드 실패!")
        else:
            print("✅ 폰트 로드 성공!")
        self.font_families = QFontDatabase.applicationFontFamilies(font_id)
        # if self.font_families:
        #     custom_font = QFont(self.font_families[0], 16)  # 16pt 크기로 설정
        # else:
        #     custom_font = QFont(self.font_families[0], 16)  # 기본 폰트 (실패 시)

        # 윈도우 설정
        self.setWindowTitle("🌸 아름다운 카메라 앱 🌸")
        self.background_color = 'navy'

        self.showFullScreen()  # 전체 화면으로 전환

        self.load_stylesheet()

        # 카메라 설정
        self.cap = cap.Camera()
        self.pro = pro.Processing()

        # UI 요소
        self.cam_label = QLabel(self)
        self.cam_label.setFixedSize(640, 480)
        self.cam_label.hide()  # 시작 전에는 숨김
        self.cam_label.setGeometry(200, 90, 640, 480)
        self.flower_state = True

        # 윈도우 크기 가져오기
        self.actual_width = 1024

        self.start_button = QPushButton("✨ 시작하기 ✨", self)
        self.start_button.setFont(QFont(self.font_families[0]))
        self.start_button.setObjectName('start')
        self.start_button.setGeometry(512, 400, 180, 100)
        self.start_button.clicked.connect(lambda:self.start_camera("result_info"))
        self.start_button.show()
 
        self.job_button = QPushButton("추천 직업", self)
        self.job_button.setFont(QFont(self.font_families[0]))
        self.job_button.setObjectName('result')
        self.job_button.setGeometry(520, 500, 120, 60)
        self.job_button.clicked.connect(lambda: self.re_game("job"))
        self.job_button.hide()
 
        self.animal_button = QPushButton("닮은 동물", self)
        self.animal_button.setFont(QFont(self.font_families[0]))
        self.animal_button.setObjectName('result')
        self.animal_button.setGeometry(680, 500, 120, 60)
        self.animal_button.clicked.connect(lambda: self.re_game("animal"))
        self.animal_button.hide()
 
        self.celeb_button = QPushButton("닮은 연예인", self)
        self.celeb_button.setFont(QFont(self.font_families[0]))
        self.celeb_button.setObjectName('result')
        self.celeb_button.setGeometry(840, 500, 120, 60)
        self.celeb_button.clicked.connect(lambda: self.re_game("celeb"))
        self.celeb_button.hide()

         # ▶ "초기화" 버튼 추가
        self.reset_button = QPushButton("처음으로", self)
        self.reset_button.setFont(QFont(self.font_families[0]))
        self.reset_button.setObjectName('operation')
        self.reset_button.setGeometry(80, 500, 120, 60)
        self.reset_button.clicked.connect(self.resetUI)
        self.reset_button.hide()

        self.result_info_button = QPushButton("능력치", self)
        self.result_info_button.setFont(QFont(self.font_families[0]))
        self.result_info_button.setObjectName('operation')
        self.result_info_button.setGeometry(280, 500, 120, 60)
        self.result_info_button.clicked.connect(lambda: self.re_game("result_info"))
        self.result_info_button.hide()

        self.temp_button = QPushButton("관상", self)
        self.temp_button.setFont(QFont(self.font_families[0]))
        self.temp_button.setObjectName('operation')
        self.temp_button.setGeometry(840, 50, 120, 60)
        self.temp_button.clicked.connect(lambda: self.re_game("temp"))
        self.temp_button.hide()

        self.setCursor(Qt.BlankCursor)

        # 꽃 애니메이션 타이머 (모든 꽃을 움직이게 함)
        self.flower_pixmap = QPixmap("/home/willtek/Bootcamp/application/resources/flower.png")
        self.animate_flower_timer = QTimer(self)
        self.animate_flower_timer.timeout.connect(self.animate_flower)
        self.animate_flower_timer.start(50)  # 50ms마다 모든 꽃 업데이트


        # 🌸 꽃 애니메이션 관련
        self.flowers = []  # 꽃 리스트 (위치 정보 저장)
        for _ in range(100):
            self.create_flower(is_initial=True)
        self.flower_timer = QTimer(self)
        self.flower_timer.timeout.connect(self.create_flower)
          # 🌸 꽃 이미지 로드
        self.flower_timer.start(150)  # 0.5초마다 꽃 생성

        # 레이아웃
        layout = QVBoxLayout()
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        # cam 부분
        self.timer = QTimer(self)
        self.timer.start(100) #0.03초마다
        self.timer.timeout.connect(self.update_frame)
       
        self.skills = {
            "매력": 90,
            "신뢰도": 70,
            "리더십": 80,            
            "지능": 85,
            "피지컬": 75, 
            "예술": 95,
        }

        self.loading_label = QLabel(self)
        self.movie = QMovie("/home/willtek/Bootcamp/application/resources/loading.gif")
        self.loading_label.setMovie(self.movie)
        self.movie.start()  # GIF 실행

        # 윈도우 크기 가져오기
        window_width = self.actual_width
        window_height = self.height()

        # QLabel 크기를 GIF 크기에 맞게 설정
        self.loading_label.setFixedSize(self.movie.frameRect().size())
        
        # QLabel을 중앙에 배치
        center_x = (window_width - self.loading_label.width()) // 2
        center_y = 40 + (window_height - self.loading_label.height()) // 2

        self.loading_label.move(center_x, center_y)
        self.loading_label.hide()

        # 캡처 모드 관련 변수
        self.skills_mode = False
        self.countdown = 2
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.cropped_face = None
        self.line_color = 'white'

        self.greenCnt = 0
        self.redCnt = 0
        self.capture_data = False
        self.result_type = None

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFont(QFont("Noto Color Emoji", 70))  # 글자 크기 키우기
        self.image_label.setGeometry(90, 90, 300, 300)  # (x, y, width, height)

        self.api_result = None
        self.api_result2 = None
        self.face = face.Celebrity()

    def re_game(self, button_type):
        """다른 게임 선택하기 (세미 초기화)"""
        self.result_type = button_type
 
        self.reset_button.show()
        self.result_info_button.show()
        self.cam_label.hide()
 
        self.start_button.hide()
        self.job_button.show()
        self.animal_button.show()
        self.celeb_button.show()
        self.temp_button.show()
 
        self.countdown_timer.stop()
        self.background_color = 'pink'
        self.update()

    def resetUI(self):
        """초기 상태로 되돌리기"""
        self.background_color = 'navy'

        self.reset_button.hide()
        self.result_info_button.hide()
        self.cam_label.hide()

        self.start_button.show()
        self.job_button.hide()
        self.animal_button.hide()
        self.celeb_button.hide()
        self.temp_button.hide()

        self.flower_timer.start(500)

        # 캡처 모드 관련 변수
        self.skills_mode = False
        self.countdown = 2
        self.greenCnt = 0
        self.redCnt = 0
        self.cropped_face = None
        self.line_color = 'white'
        self.capture_data = False
        self.result_type = None
        self.flower_state = True

        if os.path.exists(delete_jpg_file):  # 파일이 존재하는지 확인
            os.remove(delete_jpg_file)  # 파일 삭제
            print(f"{delete_jpg_file} 삭제 완료!")
        else:
            print("파일이 존재하지 않습니다.")

        if os.path.exists(delete_jpg_file2):  # 파일이 존재하는지 확인
            os.remove(delete_jpg_file2)  # 파일 삭제
            print(f"{delete_jpg_file2} 삭제 완료!")
        else:
            print("파일이 존재하지 않습니다.")

        self.update()

    def start_camera(self, button_type):
        """ 카메라 시작 """
        self.result_type = button_type
 
        # 처음 진입시 (직업, 동물 등등)
        if not self.capture_data :
            self.start_button.hide()
            self.cam_label.show()
           
            self.background_color = 'white'
            self.capture_data = True
        # 1번 경험 --> 처음으로 --> 재선택 (재촬영 필요 X)
        else :
            self.start_button.hide()
            # self.start_request()
            self.cam_label.hide()  # 카메라 화면 숨기기
            self.background_color = 'pink'
        self.update()

    def update_countdown(self):
        """ 카운트다운 업데이트 """
        if self.countdown > 0:
            self.countdown -= 1
        else:
            self.countdown_timer.stop()
            self.loading_label.show()
            self.start_request()
            self.cam_label.hide()  # 카메라 화면 숨기기
            self.background_color = 'pink'
        self.update()

    def update_frame(self):
        """ 카메라 프레임 업데이트 및 배경 애니메이션 & 가이드라인 추가 """
        if self.background_color != 'pink' :
            ret, frame = self.cap.get_frame()
            if ret:
                tmp_x1,tmp_y1,tmp_x2,tmp_y2 = self.pro.detect_face(frame)
                face_center_x = (tmp_x1 + tmp_x2)/2
                face_center_y = (tmp_y1 + tmp_y2)/2
                # print(face_center_x,face_center_y)

                # 640 x 480 size
                if self.cam_label.isVisible() :
                    if face_center_x > 120 and face_center_x <= 520 and face_center_y > 140 and face_center_y <= 340:
                        self.cropped_face = frame[tmp_y1:tmp_y2, tmp_x1:tmp_x2]
                        self.greenCnt += 1
                        self.redCnt = 0

                        #5연속시 캡처
                        if self.greenCnt >= 10 :
                            self.line_color = 'green'
                            self.cropped_face = cv2.cvtColor(self.cropped_face, cv2.COLOR_BGR2RGB)
                            self.cap.capture_face(self.cropped_face)
                            self.cap.capture_original_face(frame=frame)
                            self.greenCnt = 0
                            tmp_name, tmp_image_path = self.face.guess()
                            if tmp_name != -1 :
                                self.matched_name = tmp_name
                            if tmp_image_path != None :
                                self.image_path = tmp_image_path
                                print("matched_name ", self.matched_name, " path ", self.image_path)
                            if not self.countdown_timer.isActive():
                                self.countdown_timer.start(1000)
        
                    else :
                        self.redCnt += 1
                        self.greenCnt = 0

                        if self.redCnt >= 10 :
                            self.line_color = 'red'
                            self.redCnt = 0
                            if self.countdown_timer.isActive():
                                self.countdown_timer.stop()
                        
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                frame = cv2.resize(frame, (640, 480))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)
                qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimg)

                # 페인터 객체 생성
                painter = QPainter(pixmap)
                painter.setRenderHint(QPainter.Antialiasing)

                # 흉상 가이드라인 (중앙 기준 확대)
                path = QPainterPath()
                path.moveTo(80, 420)  # 왼쪽 어깨 시작 (기존 40 → 2배)
                path.cubicTo(200, 300, 440, 300, 560, 420)  # 어깨 곡선 확장 (X, Y 모두 2배)
                path.lineTo(600, 640)  # 팔 아래 (기존 300, 320 → 600, 640)
                path.lineTo(40, 640)  # 반대편 팔 아래 (기존 20, 320 → 40, 640)
                path.lineTo(80, 420)  # 다시 어깨로
                path.closeSubpath()

                # 검정색 테두리 그리기 (테두리 두께 12 → 2배)
                painter.setPen(QPen(colorList['black'], 12, Qt.SolidLine))
                painter.drawPath(path)

                # 흰색 경로 그리기 (원래 경로)
                painter.setPen(QPen(colorList[self.line_color], 8, Qt.SolidLine))  # 선 두께 2배
                painter.drawPath(path)

                # 머리 (타원형, 중앙 배치)
                painter.setPen(QPen(colorList['black'], 12, Qt.SolidLine))
                painter.setBrush(Qt.transparent)  # 내부는 투명
                painter.drawEllipse(QPointF(320, 190), 120, 140)  # 위치 조정 (기존 160, 100 → 320, 200)

                # 원래 흰색 타원 그리기
                painter.setPen(QPen(colorList[self.line_color], 8, Qt.SolidLine))  # 흰색 테두리, 두께 8
                painter.setBrush(Qt.transparent)  # 내부는 투명
                painter.drawEllipse(QPointF(320, 190), 120, 140)  # 크기 및 위치 조정

                if self.line_color == 'green' and self.countdown > 0:
                    countdown_text = str(self.countdown)
                    font = QFont(self.font_families[0], 100, QFont.Bold)
                    painter.setFont(font)
                    
                    # 검정색 테두리 그리기
                    painter.setPen(colorList['black'])  # 검정색
                    painter.setBrush(Qt.transparent)  # 내부는 투명

                    # 텍스트 외부에 테두리 그리기 (텍스트가 겹치지 않도록 여러 방향으로 그려서 테두리 효과를 낸다)
                    painter.drawText(w // 2 - 40 - 2, h // 2 + 20 - 2, countdown_text)  # 위, 왼쪽
                    painter.drawText(w // 2 - 40 + 2, h // 2 + 20 - 2, countdown_text)  # 위, 오른쪽
                    painter.drawText(w // 2 - 40 - 2, h // 2 + 20 + 2, countdown_text)  # 아래, 왼쪽
                    painter.drawText(w // 2 - 40 + 2, h // 2 + 20 + 2, countdown_text)  # 아래, 오른쪽

                    # 이제 원래 색으로 텍스트 그리기
                    painter.setPen(colorList['light_yellow'])  # 연노랑색
                    painter.drawText(w // 2 - 40, h // 2 + 20, countdown_text)
                
                # 테두리 추가 (검정색, 두께 6)
                pen = QPen(colorList['black'], 8, Qt.SolidLine)
                painter.setPen(pen)
                painter.drawRect(0, 0, w , h )

                # 가이드라인 (흰색, 두께 4)
                pen = QPen(colorList[self.line_color], 4, Qt.SolidLine)
                painter.setPen(pen)

                painter.end()
                self.cam_label.setPixmap(pixmap)
            self.update()

    def makeBox(self, painter):
        """ 능력치 차트 설명서 """
        painter.setPen(QPen(colorList['black'], 10, Qt.SolidLine))
        painter.drawRect(479, 25, 520, 550)

        painter.setPen(QPen(colorList['white'], 6, Qt.SolidLine))
        painter.drawRect(479, 25, 520, 550)

        font = QFont(self.font_families[0], 16, QFont.Bold)  # 폰트 설정
        painter.setFont(font)
        text_rect = QRect(479, 5, 520, 550)
        painter.setPen(QPen(colorList['black'], 6, Qt.SolidLine))

        if self.result_type == "job":
            formatted_text = self.careers_info.format(
                int(self.careers_scores[0]), self.careers[0].split(maxsplit=1)[-1],
                int(self.careers_scores[1]), self.careers[1].split(maxsplit=1)[-1],
                int(self.careers_scores[2]), self.careers[2].split(maxsplit=1)[-1],
                self.api_result2
            )

            # ✅ QTextDocument 사용 (HTML 렌더링 가능)
            doc = QTextDocument()
            doc.setHtml(formatted_text)  # ✅ HTML 적용 (가로 정렬 포함)
            doc.setTextWidth(text_rect.width())
            doc.setDefaultFont(font)

            # ✅ 세로 중앙 정렬
            total_text_height = doc.size().height()
            y_offset = text_rect.top() + (text_rect.height() - total_text_height) / 2

            # ✅ 텍스트 출력
            painter.save()
            painter.translate(text_rect.left(), y_offset)  # ✅ x 좌표 조정 (10 제거)
            doc.drawContents(painter)  # HTML 기반으로 출력
            painter.restore()

        elif self.result_type == "animal":
            formatted_text = self.animals_info.format(
                int(self.animals_scores[0]), self.animals[0].split(maxsplit=1)[-1],
                int(self.animals_scores[1]), self.animals[1].split(maxsplit=1)[-1],
                int(self.animals_scores[2]), self.animals[2].split(maxsplit=1)[-1],
                self.api_result3
            )

            # ✅ QTextDocument 사용 (HTML 렌더링 가능)
            doc = QTextDocument()
            doc.setHtml(formatted_text)  # ✅ HTML 적용 (가로 정렬 포함)
            doc.setTextWidth(text_rect.width())
            doc.setDefaultFont(font)

            # ✅ 세로 중앙 정렬
            total_text_height = doc.size().height()
            y_offset = text_rect.top() + (text_rect.height() - total_text_height) / 2

            # ✅ 텍스트 출력
            painter.save()
            painter.translate(text_rect.left(), y_offset)  # ✅ x 좌표 조정 (10 제거)
            doc.drawContents(painter)  # HTML 기반으로 출력
            painter.restore()

        elif self.result_type == "celeb":
            # self.matched_name, self.image_path
            # text = f"가장 닮은 연예인 : {self.matched_name}"
            # formatted_silver = "<br>".join(self.api_result.split("\n")) 
            formatted_text = self.celeb_info.format(
               self.matched_name,
               self.api_result
            )

            # ✅ QTextDocument 사용 (HTML 렌더링 가능)
            doc = QTextDocument()
            doc.setHtml(formatted_text)  # ✅ HTML 적용 (가로 정렬 포함)
            doc.setTextWidth(text_rect.width())
            doc.setDefaultFont(font)

            # ✅ 세로 중앙 정렬
            total_text_height = doc.size().height()
            y_offset = text_rect.top() + (text_rect.height() - total_text_height) / 2

            # ✅ 텍스트 출력
            painter.save()
            painter.translate(text_rect.left(), y_offset)  # ✅ x 좌표 조정 (10 제거)
            doc.drawContents(painter)  # HTML 기반으로 출력
            painter.restore()
            
        elif self.result_type == "result_info":
            # text = self.result_info
            font = QFont(self.font_families[0], 18)  # 폰트 설정
            painter.setFont(font)
            painter.setFont(font)  # 기존 폰트 유지

            text_rect = QRectF(479, 25, 500, 550)  # 전체 텍스트 영역

            # ✅ QTextDocument 사용 (HTML 렌더링 가능)
            doc = QTextDocument()
            doc.setDefaultFont(font)
            doc.setHtml(self.result_info)

            # ✅ 세로 중앙 정렬
            total_text_height = doc.size().height()
            y_offset = -20 + text_rect.top() + (text_rect.height() - total_text_height) / 2

            # ✅ 텍스트 출력
            painter.save()
            painter.translate(text_rect.left()+10, y_offset)
            doc.drawContents(painter)
            painter.restore()

        elif self.result_type == "temp":
            formatted_text = self.celeb_info.format(
               self.matched_name,
               self.api_result2
            )

            # ✅ QTextDocument 사용 (HTML 렌더링 가능)
            doc = QTextDocument()
            doc.setHtml(formatted_text)  # ✅ HTML 적용 (가로 정렬 포함)
            doc.setTextWidth(text_rect.width())
            doc.setDefaultFont(font)

            # ✅ 세로 중앙 정렬
            total_text_height = doc.size().height()
            y_offset = text_rect.top() + (text_rect.height() - total_text_height) / 2

            # ✅ 텍스트 출력
            painter.save()
            painter.translate(text_rect.left(), y_offset)  # ✅ x 좌표 조정 (10 제거)
            doc.drawContents(painter)  # HTML 기반으로 출력
            painter.restore()

    def create_flower(self,is_initial=False):
        """꽃을 생성하고 위치를 리스트에 추가"""
        flower_size = random.randint(20, 60)  # 랜덤한 꽃 크기 설정
        
        if is_initial:
            section_width = self.actual_width // 10  # 🌿 화면을 10등분하여 분포 균일화
            x = random.randint(0, 9) * section_width + random.randint(0, section_width - flower_size)
            y = random.randint(0, self.height())  # 🌸 화면 중간까지 랜덤한 높이에서 시작
        else:
            x = random.randint(flower_size // 2, self.actual_width - flower_size // 2)
            y = -flower_size  # 기존처럼 화면 위에서 생성
        speed = random.uniform(1, 7)  # 낙하 속도 (랜덤)
        
        angle = random.uniform(0, 2 * math.pi)  # 흔들림을 위한 초기 각도
        rotation = random.randint(0, 360)  # 🌸 회전 각도 (0~360도)
        rotation_speed = random.uniform(-10, 10)  # 🌸 회전 속도 (랜덤한 방향으로 회전)

        self.flowers.append([x, y, angle, speed, flower_size, rotation, rotation_speed])
        
        # 애니메이션 타이머 시작
        if not self.animate_flower_timer.isActive():
            self.animate_flower_timer.start(30)  # 50ms마다 업데이트
        self.update()

    def animate_flower(self):
        """꽃을 흔들면서 회전하며 떨어뜨리는 애니메이션"""
        new_flowers = []
        
        for flower in self.flowers:
            x, y, angle, speed, flower_size, rotation, rotation_speed = flower
            
            # 🌿 흔들림 (좌우 이동)
            x += math.sin(angle) * 4.0
            angle += 0.05  # 흔들림 속도
            
            # 🌸 회전 (랜덤 속도로 회전)
            rotation += rotation_speed  

            # 🍃 낙하
            y += speed  

            if y < self.height():
                new_flowers.append([x, y, angle, speed, flower_size, rotation, rotation_speed])  # 업데이트

        self.flowers = new_flowers
        self.update()

    def paintEvent(self, event):
        """ 능력치 차트 그리기 """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), colorList[self.background_color])  # 배경을 흰색으로 설정
        self.image_label.hide()
        
        if self.flower_state and (self.cam_label.isVisible() or self.loading_label.isVisible()):
            # 꽃내리는거 ON
            for flower in self.flowers:
                x, y, _, _, flower_size, rotation, _ = flower

                # 🌸 꽃 이미지 로드
                flower_pixmap = self.flower_pixmap.scaled(flower_size, flower_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                # 🎨 회전 적용
                painter.save()  # 💾 현재 상태 저장 (변환 이전 상태)
                
                transform = QTransform()
                transform.translate(x + flower_size / 2, y + flower_size / 2)  # 중심 이동
                transform.rotate(rotation)  # 회전
                transform.translate(-flower_size / 2, -flower_size / 2)  # 원래 자리로 되돌리기

                painter.setTransform(transform)
                painter.drawPixmap(0, 0, flower_pixmap)  # (0, 0)은 변환된 좌표 기준

                painter.restore()  # 🔄 원래 상태로 복구 (회전 해제)

            # 🎯 텍스트는 회전 없이 정상적으로 출력됨!
            if not self.loading_label.isVisible():
                painter.setFont(QFont(self.font_families[0], 30, QFont.Bold))  # 글꼴 크기            
                painter.setPen(colorList['black']) 
                painter.drawText(215, 50, "↑ ↑ 상단의 카메라 렌즈를 바라봐주세요 ↑ ↑")
                # painter.drawText(220, 50, " 상단의 카메라 렌즈를 바라봐주세요 🔼")
                
        if not self.cam_label.isVisible() and self.skills_mode:
            self.flower_state = False
            self.countdown = 2
            
            self.makeBox(painter)
            self.reset_button.show() # reset button 표시
            self.result_info_button.show()
            self.job_button.show()
            self.animal_button.show()
            self.celeb_button.show()
            self.temp_button.show()

            if self.result_type == "job":
                emoji = self.careers[0].split()[0]
                # emoji = "👨🏻‍⚖️"
                self.image_label.setText(f"<h1>{emoji}</h1>")
                # self.image_label.setFont(QFont("Noto Color Emoji"))
                self.image_label.setAlignment(Qt.AlignCenter)  # 중앙 정렬
                self.image_label.show()
                if not hasattr(self, "label_y"):  
                    self.label_y = self.image_label.y()  # 초기 Y 좌표 저장

                self.image_label.setGeometry(
                    self.image_label.x(), self.label_y + 50,  # Y 좌표 고정
                    self.image_label.width(), self.image_label.height()
                )
            elif self.result_type == "animal":
                emoji = self.animals[0].split()[0]
                # emoji = "👩🏻‍💼"
                self.image_label.setText(f"<h1>{emoji}</h1>")
                # self.image_label.setFont(QFont("Noto Color Emoji"))
                self.image_label.setAlignment(Qt.AlignCenter)  # 중앙 정렬
                self.image_label.show()
                if not hasattr(self, "label_y"):  
                    self.label_y = self.image_label.y()  # 초기 Y 좌표 저장

                self.image_label.setGeometry(
                    self.image_label.x(), self.label_y + 50,  # Y 좌표 고정
                    self.image_label.width(), self.image_label.height()
                )
            elif self.result_type == "celeb":
                # ✅ 이미지 로드 및 QLabel에 표시
                pixmap = QPixmap(self.image_path)  # 경로에서 Pixmap 생성
                max_width = 400
                max_height = 550

                # ✅ 1단계: 높이를 먼저 550px로 맞추기 (비율 유지)
                resized_pixmap = pixmap.scaledToHeight(max_height, Qt.SmoothTransformation)

                # ✅ 2단계: 가로가 520px을 초과하면 중앙을 기준으로 크롭
                if resized_pixmap.width() > max_width:
                    left = (resized_pixmap.width() - max_width) // 2  # 중앙 기준으로 잘라낼 왼쪽 좌표
                    rect = QRect(left, 0, max_width, max_height)  # 520x550 크기로 자르기
                    resized_pixmap = resized_pixmap.copy(rect)
                x_size = resized_pixmap.width()
                x_pos = (450 - x_size) // 2
                # ✅ QLabel 또는 painter에 출력
                painter.drawPixmap(x_pos, 20, resized_pixmap)
            elif self.result_type == "result_info":
                # self.image_label.hide()
                hexagon_center_x = 230
                hexagon_center_y = 270
                hexagon_radius = 160
                self.chart = hexa.HexagonChart(hexagon_center_x, hexagon_center_y, hexagon_radius, self.font_families[0])
                self.chart.draw_chart(painter)
                self.chart.draw_results(painter, self.skills)
            elif self.result_type == "temp":
                pixmap = QPixmap(self.image_path)  # 경로에서 Pixmap 생성
                max_width = 400
                max_height = 550

                # ✅ 1단계: 높이를 먼저 550px로 맞추기 (비율 유지)
                resized_pixmap = pixmap.scaledToHeight(max_height, Qt.SmoothTransformation)

                # ✅ 2단계: 가로가 520px을 초과하면 중앙을 기준으로 크롭
                if resized_pixmap.width() > max_width:
                    left = (resized_pixmap.width() - max_width) // 2  # 중앙 기준으로 잘라낼 왼쪽 좌표
                    rect = QRect(left, 0, max_width, max_height)  # 520x550 크기로 자르기
                    resized_pixmap = resized_pixmap.copy(rect)
                x_size = resized_pixmap.width()
                x_pos = (450 - x_size) // 2
                # ✅ QLabel 또는 painter에 출력
                painter.drawPixmap(x_pos, 20, resized_pixmap)

            painter.end()
    
    def closeEvent(self, event):
        """ 프로그램 종료 시 카메라 해제 """
        self.cap.close()
        event.accept()

    def start_request(self):
        inf = infer.Inference(self.pro.classification_jpg())
        self.skills = inf.get_skills()  
        self.careers, self.animals, self.careers_scores, self.animals_scores = inf.infer_careers()
        self.result_info, self.careers_info, self.animals_info, self.celeb_info = inf.get_formats()

        # API 요청을 백그라운드에서 실행
        self.api_thread = req.ApiThread(self.skills, self.careers[0].split(maxsplit=1)[-1], self.animals[0].split(maxsplit=1)[-1], self.matched_name)
        self.api_thread.finished_signal.connect(self.handle_response)  # 완료 시 실행할 함수 연결
        self.api_thread.start()

    def handle_response(self, data):
        self.loading_label.hide()  # 로딩 메시지 숨김
        self.skills_mode = True
        # print("📌 받은 데이터:", data)  # 터미널에서 확인

        # 딕셔너리에서 "content" 값 가져오기
        self.api_result = data.get("content", "데이터 없음")
        self.api_result2 = data.get("content2", "데이터 없음")
        self.api_result3 = data.get("content3", "데이터 없음")
        print("📌 content 값:", self.api_result)  # 터미널에서 확인
        print("📌 content2 값:", self.api_result2)  # 터미널에서 확인
        print("📌 content3 값:", self.api_result3)  # 터미널에서 확인

    def load_stylesheet(self):
        # stylesheet.qss 파일 로드
        qss_file = QFile('/home/willtek/Bootcamp/application/stylesheet/stylesheet.qss')
        qss_file.open(QFile.ReadOnly | QFile.Text)
        qss_stream = QTextStream(qss_file)
        self.setStyleSheet(qss_stream.readAll())
        qss_file.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOverrideCursor(Qt.BlankCursor)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())