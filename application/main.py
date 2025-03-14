from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QBrush, QPainterPath, QFont, QPolygonF, QMovie, QTransform
from PyQt5.QtCore import Qt, QTimer, QPoint, QPointF, QRect, QPropertyAnimation
import math
import Camera as cap
import Processing as pro
import Api as req
import sys
import cv2
import numpy as np
import random

# colorList = [(255,0,0),(0,255,0),(0,0,255),(0,0,255),(0,0,255),(255, 182, 193),(30, 58, 95)] # R G B, white, black, pink, navy
colorList = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'pink': (255, 192, 203),
    'navy': (30, 58, 95),
    'yellow': (255, 255, 0),
    'light_yellow': (255, 255, 150),
    'light_gray': (192, 192, 192),
    'gray': (128, 128, 128),
    'dark_gray': (64, 64, 64),
    'chart_skyblue' : (0, 150, 255)
}

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()

        # 윈도우 설정
        self.setWindowTitle("🌸 아름다운 카메라 앱 🌸")
        self.setGeometry(100, 100, 640, 480)
        self.background_color = 'navy'
        # self.setStyleSheet("background-color: #1E3A5F;")  # 남색 계열 배경

        # self.showMaximized() # 최대화면으로 전환
        self.showFullScreen()  # 전체 화면으로 전환

        # 카메라 설정
        self.cap = cap.Camera()
        self.pro = pro.Processing()

        # UI 요소
        self.cam_label = QLabel(self)
        self.cam_label.setFixedSize(640, 480)
        self.cam_label.hide()  # 시작 전에는 숨김
        self.cam_label.setGeometry(200, 90, 640, 480)

        # 윈도우 크기 가져오기
        self.actual_width = 1024

        self.start_button = QPushButton("✨ 시작하기 ✨", self)
        self.start_button.setStyleSheet("""
            QPushButton {
                font-size: 45px;
                font-weight: bold;
                color: white;
                background-color: rgba(50, 130, 200, 220);
                border-radius: 25px;
                padding: 30px 60px;
                border: 2px solid white;
                outline: none; /* 포커스 박스 제거 */
            }
            QPushButton:hover {
                background-color: rgba(30, 100, 170, 250);
            }
            QPushButton:focus {
                outline: none; /* 포커스 효과 제거 */
            }
        """)

        self.start_button.clicked.connect(self.start_camera)

         # ▶ "초기화" 버튼 추가
        self.reset_button = QPushButton("처음으로", self)
        self.reset_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                font-weight: bold;
                color: black;
                background-color: rgba(70, 220, 200, 220);
                border-radius: 25px;
                padding: 15 10px;
                border: 2px solid black;
            }
            QPushButton:hover {
                background-color: rgba(40, 150, 160, 250);
            }
        """)
        self.reset_button.setGeometry(820, 500, 120, 60)
        self.reset_button.clicked.connect(self.resetUI)
        # self.reset_button.show()
        self.reset_button.hide()

        self.finish_button = QPushButton("종료하기", self)
        self.finish_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                font-weight: bold;
                color: black;
                background-color: rgba(70, 220, 200, 220);
                border-radius: 25px;
                padding: 15 10px;
                border: 2px solid black;
            }
            QPushButton:hover {
                background-color: rgba(40, 150, 160, 250);
            }
        """)
        self.finish_button.setGeometry(620, 500, 120, 60)
        self.finish_button.clicked.connect(self.closeEvent)
        # self.finish_button.show()
        self.finish_button.hide()

        self.setCursor(Qt.BlankCursor)

        # 투명한 터치 버튼 추가
        self.touch_button = QPushButton(self)
        self.touch_button.setFixedSize(640, 480)
        # self.touch_button.setStyleSheet("color: white;")
        self.touch_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)
        self.touch_button.clicked.connect(self.toggle_capture_mode)
        self.touch_button.setGeometry(200, 90, 640, 480)  # (x, y, width, height)
        self.touch_button.hide()

        # 꽃 애니메이션 타이머 (모든 꽃을 움직이게 함)
        self.animate_flower_timer = QTimer(self)
        self.animate_flower_timer.timeout.connect(self.animate_flower)
        self.animate_flower_timer.start(50)  # 50ms마다 모든 꽃 업데이트


        # 🌸 꽃 애니메이션 관련
        self.flowers = []  # 꽃 리스트 (위치 정보 저장)
        for _ in range(100):
            self.create_flower(is_initial=True)
        self.flower_timer = QTimer(self)
        self.flower_timer.timeout.connect(self.create_flower)
        self.flower_pixmap = QPixmap("flower.png")  # 🌸 꽃 이미지 로드
        self.flower_timer.start(150)  # 0.5초마다 꽃 생성

        
        

        # 레이아웃
        layout = QVBoxLayout()
        # layout.addWidget(self.cam_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        # cam 부분
        self.timer = QTimer(self)
        self.timer.start(100) #0.03초마다
        self.timer.timeout.connect(self.update_frame)
       
        # self.flower_timer.start(500)  # 0.5초마다 생성

        self.skills = {
            "매력": 90,
            "신뢰도": 70,
            "리더십": 80,            
            "지능": 85,
            "피지컬": 75, 
            "예술": 95,
        }
       

        self.loading_label = QLabel(self)
        self.movie = QMovie("loading.gif")
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
        # self.loading_label.show()

        # 캡처 모드 관련 변수
        self.capture_mode = False
        self.skills_mode = False
        self.face_detected = False
        self.countdown = 5
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        # self.FacePosition = {0,0,0,0}
        self.cropped_face = None
        self.line_color = 'white'

        self.greenCnt = 0
        self.redCnt = 0
        self.still_countdown = False
        self.last_still_countdown = False

    def resetUI(self):
        """초기 상태로 되돌리기"""
        self.background_color = 'navy'
        # self.setStyleSheet("background-color: #1E3A5F;")  # 남색 계열 배경

        self.reset_button.hide()
        self.finish_button.hide()
        self.cam_label.hide()

        self.touch_button.hide()
        self.start_button.show()

        self.flower_timer.start(500)

        # 캡처 모드 관련 변수
        self.capture_mode = False
        self.skills_mode = False
        self.face_detected = False
        self.still_countdown = False
        self.last_still_countdown = False
        self.countdown = 5
        self.greenCnt = 0
        self.redCnt = 0
        self.cropped_face = None
        self.line_color = 'white'
        self.update()

    def start_camera(self):
        """ 카메라 시작 """
        self.start_button.hide()
        self.cam_label.show()
        self.touch_button.show()
        
        self.background_color = 'white'
        
        self.update()

    def toggle_capture_mode(self):
        """ 카메라 화면 터치 시 캡처 모드 토글 """
        self.capture_mode = not self.capture_mode
        if self.capture_mode:
            # self.countdown = 5
            self.countdown_timer.start(1000)
        else:
            self.countdown_timer.stop()

    def update_countdown(self):
        """ 카운트다운 업데이트 """
        if self.countdown > 0:
            self.countdown -= 1
        else:
            self.countdown_timer.stop()
            # if self.face_detected:
            #     self.cap.capture_face(self.cropped_face)
            # else :
            #     self.cap.capture_image()            
            self.capture_mode = False
            self.start_request()
            self.cam_label.hide()  # 카메라 화면 숨기기
            self.touch_button.hide()  # 캡처 모드 버튼 숨기기
            self.background_color = 'pink'
        self.update()

    def update_frame(self):
        """ 카메라 프레임 업데이트 및 배경 애니메이션 & 가이드라인 추가 """
        if self.background_color != 'pink' :
            ret, frame = self.cap.get_frame()
            self.line_color = 'white'
            if ret:
                tmp_x1,tmp_y1,tmp_x2,tmp_y2 = self.pro.detect_face(frame)
                face_center_x = (tmp_x1 + tmp_x2)/2
                face_center_y = (tmp_y1 + tmp_y2)/2
                # 640 x 480 size
                if self.cam_label.isVisible() :
                    if face_center_x > 150 and face_center_x <= 490 and face_center_y > 0 and face_center_y <= 350:
                        self.face_detected = True
                        self.cropped_face = frame[tmp_y1:tmp_y2, tmp_x1:tmp_x2]
                        self.greenCnt += 1
                        if self.redCnt > 0 :
                            self.redCnt -= 1
                        # self.redCnt = 0
                        if not self.countdown_timer.isActive():
                            self.countdown_timer.start(1000)
                    else :
                        self.redCnt += 1
                        if self.greenCnt > 0 :
                            self.greenCnt -= 1
                        # self.countdown = 5
                        if self.still_countdown == False :
                            self.countdown_timer.stop()

                if self.greenCnt >= self.redCnt:
                    self.line_color = 'green'
                    if self.greenCnt >= 5 :
                        self.still_countdown = True
                        # self.cropped_face = frame[tmp_y1:tmp_y2, tmp_x1:tmp_x2]
                        if self.last_still_countdown == False :
                            self.cropped_face = cv2.cvtColor(self.cropped_face, cv2.COLOR_BGR2RGB)
                            self.cap.capture_face(self.cropped_face)
                    if self.greenCnt >= 10 :
                        self.greenCnt = 9
                elif self.redCnt >  self.greenCnt:
                    self.line_color = 'red'
                    if self.redCnt >= 10 :
                        self.redCnt = 9
                else :
                    self.line_color = 'white'
                
                if self.still_countdown and face_center_x == 0 and face_center_y == 0 :
                    self.line_color = 'green'

                # print(tmp_x2,tmp_y2,tmp_x2,tmp_y2) 
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
                painter.setPen(QPen(QColor(*colorList['black']), 12, Qt.SolidLine))
                painter.drawPath(path)
                self.line_color
                # 흰색 경로 그리기 (원래 경로)
                painter.setPen(QPen(QColor(*colorList[self.line_color]), 8, Qt.SolidLine))  # 선 두께 2배
                painter.drawPath(path)

                # 머리 (타원형, 중앙 배치)
                painter.setPen(QPen(QColor(*colorList['black']), 12, Qt.SolidLine))
                painter.setBrush(Qt.transparent)  # 내부는 투명
                painter.drawEllipse(QPointF(320, 190), 120, 140)  # 위치 조정 (기존 160, 100 → 320, 200)

                # 원래 흰색 타원 그리기
                painter.setPen(QPen(QColor(*colorList[self.line_color]), 8, Qt.SolidLine))  # 흰색 테두리, 두께 8
                painter.setBrush(Qt.transparent)  # 내부는 투명
                painter.drawEllipse(QPointF(320, 190), 120, 140)  # 크기 및 위치 조정

                if (self.capture_mode or self.still_countdown) and self.countdown > 0:
                    countdown_text = str(self.countdown)
                    font = QFont("Consolas", 100, QFont.Bold)
                    painter.setFont(font)
                    
                    # 검정색 테두리 그리기
                    painter.setPen(QColor(*colorList['black']))  # 검정색
                    painter.setBrush(Qt.transparent)  # 내부는 투명

                    # 텍스트 외부에 테두리 그리기 (텍스트가 겹치지 않도록 여러 방향으로 그려서 테두리 효과를 낸다)
                    painter.drawText(w // 2 - 40 - 2, h // 2 + 20 - 2, countdown_text)  # 위, 왼쪽
                    painter.drawText(w // 2 - 40 + 2, h // 2 + 20 - 2, countdown_text)  # 위, 오른쪽
                    painter.drawText(w // 2 - 40 - 2, h // 2 + 20 + 2, countdown_text)  # 아래, 왼쪽
                    painter.drawText(w // 2 - 40 + 2, h // 2 + 20 + 2, countdown_text)  # 아래, 오른쪽

                    # 이제 원래 색으로 텍스트 그리기
                    painter.setPen(QColor(*colorList['light_yellow']))  # 연노랑색
                    painter.drawText(w // 2 - 40, h // 2 + 20, countdown_text)
                
                # 테두리 추가 (검정색, 두께 6)
                pen = QPen(QColor(*colorList['black']), 8, Qt.SolidLine)
                painter.setPen(pen)
                painter.drawRect(0, 0, w , h )

                # 가이드라인 (흰색, 두께 4)
                pen = QPen(QColor(*colorList[self.line_color]), 4, Qt.SolidLine)
                painter.setPen(pen)

                painter.end()
                self.cam_label.setPixmap(pixmap)

            # 꽃 애니메이션 업데이트
            # self.update_flowers()
            self.last_still_countdown = self.still_countdown
            self.update()

    def update_careers(self):
        skills2= self.pro.classification_jpg()
        # for i in range(6) :
        self.skills["리더십"] = skills2[0] * 100
        self.skills["매력"] = skills2[1] * 100
        self.skills["신뢰도"] = skills2[2] * 100
        self.skills["피지컬"] = skills2[3] * 100
        self.skills["예술"] = skills2[4] * 100
        self.skills["지능"] = skills2[5] * 100
        # print(self.skills)
        self.careers = {
            # 🎭 예술 & 창작 직군 (매력 & 예술 최우선, 신뢰도 & 피지컬 낮음)
            "🎭 배우, 모델, 인플루언서": self.skills["매력"] * 4.8 + self.skills["예술"] * 3.5 + self.skills["신뢰도"] * 1.0 + self.skills["리더십"] * 0.1 + self.skills["지능"] * 0.1 + self.skills["피지컬"] * 0.5,
            "🎨 디자이너, 일러스트레이터, 화가": self.skills["매력"] * 0.5 + self.skills["예술"] * 7.1 + self.skills["신뢰도"] * 2.25 + self.skills["리더십"] * 0.15 + self.skills["지능"] * 0.1 + self.skills["피지컬"] * 0.3,
            "🎤 가수, 성우, 연예인": self.skills["매력"] *4.3 + self.skills["예술"] * 3.7 + self.skills["신뢰도"] * 1.0 + self.skills["리더십"] * 0.1 + self.skills["지능"] * 0.1 + self.skills["피지컬"] * 0.8,

            # 💼 경영 & 리더십 직군 (리더십 & 신뢰도 최우선, 예술 & 피지컬 낮음)
            "📢 CEO, 정치가, 경영자": self.skills["매력"] * 0.3 + self.skills["예술"] * 0.05 + self.skills["신뢰도"] * 0.8 + self.skills["리더십"] * 4.0 + self.skills["지능"] * 4.8 + self.skills["피지컬"] * 0.05,
            "📊 마케터, 광고기획자": self.skills["매력"] * 1.5 + self.skills["예술"] * 3.5 + self.skills["신뢰도"] * 2.0 + self.skills["리더십"] * 0.5 + self.skills["지능"] * 2.0 + self.skills["피지컬"] * 0.5,
            "🏛️ 외교관, 공무원, 행정가": self.skills["매력"] * 0.15 + self.skills["예술"] * 0.15 + self.skills["신뢰도"] * 4.5 + self.skills["리더십"] * 2.0 + self.skills["지능"] * 3.0 + self.skills["피지컬"] * 0.2,

            # 🏋️‍♂️ 스포츠 & 육체 직군 (피지컬 최우선, 지능 & 예술 낮음)
            "⚽ 운동선수, 트레이너": self.skills["매력"] * 1.5 + self.skills["예술"] * 0.1 + self.skills["신뢰도"] * 0.3 + self.skills["리더십"] * 1.0 + self.skills["지능"] * 0.1 + self.skills["피지컬"] * 7.0,
            "🚔 경찰, 군인, 소방관": self.skills["매력"] * 0.1 + self.skills["예술"] * 0.1 + self.skills["신뢰도"] * 2.0 + self.skills["리더십"] * 1.1 + self.skills["지능"] * 1.2 + self.skills["피지컬"] * 5.5,
            "🚀 파일럿, 레이서": self.skills["매력"] * 1.0 + self.skills["예술"] * 1.0 + self.skills["신뢰도"] * 1.7 + self.skills["리더십"] * 1.5 + self.skills["지능"] * 0.8 + self.skills["피지컬"] * 4.0,

            # 🧠 학문 & 기술 직군 (지능 최우선, 피지컬 & 예술 낮음)
            "🔬 과학자, 교수, 연구원": self.skills["매력"] * 0.15 + self.skills["예술"] * 0.05 + self.skills["신뢰도"] * 1.5 + self.skills["리더십"] * 1.4 + self.skills["지능"] * 6.0 + self.skills["피지컬"] * 0.4,
            "💻 프로그래머, 데이터 과학자": self.skills["매력"] * 0.3 + self.skills["예술"] * 1.2 + self.skills["신뢰도"] * 1.0 + self.skills["리더십"] * 0.3 + self.skills["지능"] * 7.0 + self.skills["피지컬"] * 0.2,
            "⚖️ 변호사, 판사": self.skills["매력"] * 0.7 + self.skills["예술"] * 0.2 + self.skills["신뢰도"] * 4.0 + self.skills["리더십"] * 1.0 + self.skills["지능"] * 4.0 + self.skills["피지컬"] * 0.1,

            # 🌍 서비스 & 커뮤니케이션 직군 (매력 & 신뢰도 최우선, 피지컬 낮음)
            "🎙️ 기자, 아나운서, 방송인": self.skills["매력"] * 3.5 + self.skills["예술"] * 0.5 + self.skills["신뢰도"] * 3.5 + self.skills["리더십"] * 0.5 + self.skills["지능"] * 1.5 + self.skills["피지컬"] * 0.5,
            "🛫 호텔리어, 승무원, 바텐더": self.skills["매력"] * 6.0 + self.skills["예술"] * 0.6 + self.skills["신뢰도"] * 1.5 + self.skills["리더십"] * 0.5 + self.skills["지능"] * 0.4 + self.skills["피지컬"] * 1.0,
        }

    def makeBox(self, painter):
        """ 능력치 차트 설명서 """
        painter.setPen(QPen(QColor(*colorList['black']), 10, Qt.SolidLine))
        painter.drawRect(25, 25, 500, 550)

        painter.setPen(QPen(QColor(*colorList['white']), 6, Qt.SolidLine))
        painter.drawRect(25, 25, 500, 550)

        # sorted_skills = sorted(self.skills.items(), key=lambda item: item[1], reverse=True)

        self.update_careers()
        
        sorted_careers = sorted(self.careers.items(), key=lambda x: x[1], reverse=True)

        top1 = sorted_careers[0][0]  # 1순위 직업
        top2 = sorted_careers[1][0]  # 2순위 직업
        top3 = sorted_careers[2][0]  # 3순위 직업

        text = f"🔥 추천 직업 🔥\n1st: {top1}\n2nd: {top2}\n3rd: {top3}"
        font = QFont("Consolas", 16, QFont.Bold)  # 폰트 설정
        painter.setFont(font)

        # 박스 내부에 텍스트를 중앙 정렬
        text_rect = QRect(25, 25, 500, 550)
        painter.setPen(QPen(QColor(*colorList['black']), 6, Qt.SolidLine))
        painter.drawText(text_rect, Qt.AlignCenter, text)    

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
            # x += math.sin(angle) * random.uniform(-4.0, 4.0)
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
        painter.fillRect(self.rect(), QColor(*colorList[self.background_color]))  # 배경을 흰색으로 설정 
        
        if self.cam_label.isVisible() or self.loading_label.isVisible():
            # 꽃내리는거 ON
            for flower in self.flowers:
                x, y, _, _, flower_size, rotation, _ = flower

                # 🌸 꽃 이미지 로드
                flower_pixmap = QPixmap("flower.png")  
                flower_pixmap = flower_pixmap.scaled(flower_size, flower_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

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
                painter.setFont(QFont("Consolas", 25, QFont.Bold))  # 글꼴 크기            
                painter.setPen(QColor(*colorList['black']))  
                painter.drawText(220, 50, "🔼 상단의 카메라 렌즈를 바라봐주세요 🔼")
                

        # self.reset_button.show() # 항상 표시 (reset button 수정하기 위해서)
        if not self.cam_label.isVisible() and self.skills_mode:
            # self.flower_timer.stop()
            self.countdown = 5
            hexagon_center_x = 770
            hexagon_center_y = 240
            hexagon_radius = 160
            self.makeBox(painter)
            self.reset_button.show() # reset button 표시
            self.finish_button.show()

            for i in range(6):
                center = QPointF(hexagon_center_x, hexagon_center_y)  
                radius = hexagon_radius*i/(6-1)
                angles = [math.radians(60 * i) for i in range(6)]
                hexagon_points = [
                QPointF(center.x() + radius * math.cos(angle), center.y() + radius * math.sin(angle))
                for angle in angles
                ]
                painter.setPen(QPen(QColor(*colorList['gray'], 200), 1))
                painter.setBrush(Qt.NoBrush)
                painter.drawPolygon(QPolygonF(hexagon_points))  # ✅ 리스트 전달
            

            # ⚡ 육각형 중심 및 반지름
            center = QPointF(hexagon_center_x, hexagon_center_y)  
            radius = hexagon_radius  
            angles = [math.radians(60 * i) for i in range(6)]  

            # ⚡ 육각형 꼭짓점 계산
            hexagon_points = [
                QPointF(center.x() + radius * math.cos(angle), center.y() + radius * math.sin(angle))
                for angle in angles
            ]

            # ⚡ 능력치 값에 따른 내부 다각형 좌표 계산
            skill_points = [
                QPointF(
                    center.x() + (radius * (self.skills[label] / 100) * math.cos(angle)),
                    center.y() + (radius * (self.skills[label] / 100) * math.sin(angle))
                )
                for label, angle in zip(self.skills.keys(), angles)
            ]

            # ⚡ 육각형 외곽선 그리기
            painter.setPen(QPen(QColor(*colorList['black']), 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawPolygon(QPolygonF(hexagon_points))  # ✅ 리스트 전달

            # ⚡ 능력치 내부 다각형 그리기 (반투명 색상)
            painter.setPen(QPen(QColor(*colorList['dark_gray']), 2))
            painter.setBrush(QBrush(QColor(*colorList['chart_skyblue'],130)))  # 반투명 파란색 채우기
            painter.drawPolygon(QPolygonF(skill_points))  # ✅ 리스트 전달

            # ⚡ 능력치 직선 연결
            for point in hexagon_points:
                # pen = QPen(QColor(255, 255, 255), 2)  # 흰색, 두께 2
                painter.setPen(QColor(*colorList['white']))
                painter.drawLine(center, point)

            # ⚡ 능력치 항목 표시 (찌그러진 육각형 바깥)
            center2 = QPointF(hexagon_center_x-25, hexagon_center_y+10)
            radius2 = hexagon_radius+26
            y_scale = 0.97

            for i, label in enumerate(self.skills.keys()):
                text_pos = QPointF(
                    center2.x() + radius2 * math.cos(angles[i]),
                    center2.y() + (radius2 * y_scale * math.sin(angles[i]))
                )
                painter.setPen(QColor(*colorList['black']))
                painter.setFont(QFont("Consolas", 20, QFont.Bold))
                painter.drawText(text_pos, label)
            painter.end()
    
    def closeEvent(self, event):
        """ 프로그램 종료 시 카메라 해제 """
        if self.cap.isOpened():
            self.cap.release()
        event.accept()
        # sys.exit(app.exec_())

    def start_request(self):
        # self.movie.start()
        self.loading_label.show()  # 로딩 메시지 표시
        
        # API 요청을 백그라운드에서 실행
        self.api_thread = req.ApiThread()
        self.api_thread.finished_signal.connect(self.handle_response)  # 완료 시 실행할 함수 연결
        self.api_thread.start()

    def handle_response(self, data):
        self.loading_label.hide()  # 로딩 메시지 숨김
        self.skills_mode = True
        
        # if "error" in data:
        #     self.result_label.setText(f"에러 발생: {data['error']}")
        # else:
        #     self.skills = data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOverrideCursor(Qt.BlankCursor)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())