from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QBrush, QPainterPath, QFont, QPolygonF, QMovie
from PyQt5.QtCore import Qt, QTimer, QPoint, QPointF, QRect, QPropertyAnimation
import math
import Camera as cap
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

        # UI 요소
        self.cam_label = QLabel(self)
        self.cam_label.setFixedSize(640, 480)
        self.cam_label.hide()  # 시작 전에는 숨김
        self.cam_label.setGeometry(200, 90, 640, 480)

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
            }
            QPushButton:hover {
                background-color: rgba(30, 100, 170, 250);
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
        self.touch_button.setGeometry(160, 120, 640, 480)  # (x, y, width, height)
        self.touch_button.hide()

        # 🌸 꽃 애니메이션 관련
        self.flowers = []  # 꽃 리스트 (위치 정보 저장)
        self.flower_timer = QTimer(self)
        self.flower_timer.timeout.connect(self.create_flower)
        self.flower_pixmap = QPixmap("flower.png")  # 🌸 꽃 이미지 로드
        self.flower_timer.start(150)  # 0.5초마다 꽃 생성

        # 꽃 애니메이션 타이머 (모든 꽃을 움직이게 함)
        self.animate_flower_timer = QTimer(self)
        self.animate_flower_timer.timeout.connect(self.animate_flower)
        self.animate_flower_timer.start(50)  # 50ms마다 모든 꽃 업데이트
        

        # 레이아웃
        layout = QVBoxLayout()
        # layout.addWidget(self.cam_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        # 애니메이션을 위한 타이머
        self.timer = QTimer(self)
        self.timer.start(30) #0.03초마다
        self.timer.timeout.connect(self.update_frame)
       
        # self.flower_timer.start(500)  # 0.5초마다 생성

        self.skills = {
            # "리더십": 80,
            # "신체능력": 75,
            # "총명함": 85,            
            # "매력": 90,
            # "신뢰도": 70,
            # "예술력": 95,
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

        # QLabel 크기를 GIF 크기에 맞게 설정
        self.loading_label.setFixedSize(self.movie.frameRect().size())

        # 윈도우 크기 가져오기
        window_width = self.width()
        window_height = self.height()

        # QLabel을 중앙에 배치
        center_x = 190 + (window_width - self.loading_label.width()) // 2
        center_y = 40 + (window_height - self.loading_label.height()) // 2

        self.loading_label.move(center_x, center_y)
        self.loading_label.hide()

        # 캡처 모드 관련 변수
        self.capture_mode = False
        self.skills_mode = False
        self.countdown = 0
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)

    def resetUI(self):
        """초기 상태로 되돌리기"""
        self.background_color = 'navy'
        # self.setStyleSheet("background-color: #1E3A5F;")  # 남색 계열 배경

        self.reset_button.hide()
        self.cam_label.hide()

        self.touch_button.hide()
        self.start_button.show()

        self.flower_timer.start(500)

        # 캡처 모드 관련 변수
        self.capture_mode = False
        self.skills_mode = False
        self.countdown = 0
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
        # if self.skills_mode == False:
        #     self.skills_mode = True
        if self.capture_mode:
            self.countdown = 5
            self.countdown_timer.start(1000)
        else:
            self.countdown_timer.stop()
        self.update()

    def update_countdown(self):
        """ 카운트다운 업데이트 """
        if self.countdown > 0:
            self.countdown -= 1
        else:
            self.countdown_timer.stop()
            self.cap.capture_image()
            self.capture_mode = False
            self.start_request()
            self.cam_label.hide()  # 카메라 화면 숨기기
            self.touch_button.hide()  # 캡처 모드 버튼 숨기기
            self.update()  # 차트를 그리기 위해 업데이트
            self.background_color = 'pink'
        self.update()

    def update_frame(self):
        """ 카메라 프레임 업데이트 및 배경 애니메이션 & 가이드라인 추가 """
        ret, frame = self.cap.get_frame()
        
        if ret:            
            h, w, ch = frame.shape
            bytes_per_line = ch * w
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
            painter.setPen(QPen(QColor(0, 0, 0), 12, Qt.SolidLine))
            painter.drawPath(path)

            # 흰색 경로 그리기 (원래 경로)
            painter.setPen(QPen(QColor(255, 255, 255, 255), 8, Qt.SolidLine))  # 선 두께 2배
            painter.drawPath(path)

            # 머리 (타원형, 중앙 배치)
            painter.setPen(QPen(QColor(0, 0, 0), 12, Qt.SolidLine))
            painter.setBrush(Qt.transparent)  # 내부는 투명
            painter.drawEllipse(QPointF(320, 190), 120, 140)  # 위치 조정 (기존 160, 100 → 320, 200)

            # 원래 흰색 타원 그리기
            painter.setPen(QPen(QColor(255, 255, 255, 255), 8, Qt.SolidLine))  # 흰색 테두리, 두께 8
            painter.setBrush(Qt.transparent)  # 내부는 투명
            painter.drawEllipse(QPointF(320, 190), 120, 140)  # 크기 및 위치 조정

            if self.capture_mode and self.countdown > 0:
                countdown_text = str(self.countdown)
                font = QFont("Consolas", 100, QFont.Bold)
                painter.setFont(font)
                
                # 검정색 테두리 그리기
                painter.setPen(QColor(0, 0, 0))  # 검정색
                painter.setBrush(Qt.transparent)  # 내부는 투명

                # 텍스트 외부에 테두리 그리기 (텍스트가 겹치지 않도록 여러 방향으로 그려서 테두리 효과를 낸다)
                painter.drawText(w // 2 - 40 - 2, h // 2 + 20 - 2, countdown_text)  # 위, 왼쪽
                painter.drawText(w // 2 - 40 + 2, h // 2 + 20 - 2, countdown_text)  # 위, 오른쪽
                painter.drawText(w // 2 - 40 - 2, h // 2 + 20 + 2, countdown_text)  # 아래, 왼쪽
                painter.drawText(w // 2 - 40 + 2, h // 2 + 20 + 2, countdown_text)  # 아래, 오른쪽

                # 이제 원래 색으로 텍스트 그리기
                painter.setPen(QColor(255, 255, 150, 255))  # 연노랑색
                painter.drawText(w // 2 - 40, h // 2 + 20, countdown_text)
            
            # 테두리 추가 (검정색, 두께 6)
            pen = QPen(QColor(0, 0, 0, 255), 8, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawRect(0, 0, w , h )

            # 가이드라인 (흰색, 두께 4)
            pen = QPen(QColor(255, 255, 255, 255), 4, Qt.SolidLine)
            painter.setPen(pen)

            painter.end()
            self.cam_label.setPixmap(pixmap)

        # 꽃 애니메이션 업데이트
        # self.update_flowers()
        self.update()

    def makeBox(self, painter):
        """ 능력치 차트 설명서 """
        painter.setPen(QPen(QColor(*colorList['black']), 10, Qt.SolidLine))
        painter.drawRect(25, 25, 500, 550)

        painter.setPen(QPen(QColor(*colorList['white']), 6, Qt.SolidLine))
        painter.drawRect(25, 25, 500, 550)

        text = "Hello, World!\nThis is centered text.\n당신은 예술인 !"
        font = QFont("Consolas", 16, QFont.Bold)  # 폰트 설정
        painter.setFont(font)

        # 박스 내부에 텍스트를 중앙 정렬
        text_rect = QRect(25, 25, 500, 550)
        painter.setPen(QPen(QColor(*colorList['black']), 6, Qt.SolidLine))
        painter.drawText(text_rect, Qt.AlignCenter, text)    

    def create_flower(self):
        """꽃을 생성하고 위치를 리스트에 추가"""
        
        flower_size = random.randint(20,60)  # 랜덤한 꽃 크기 설정
        x = random.randint(0, self.width() - flower_size)
        angle = random.uniform(0, 2 * math.pi)  # 흔들림을 위한 초기 각도 (랜덤)
        speed = random.uniform(2, 6)  # 낙하 속도 (랜덤)

        self.flowers.append([x, -flower_size, angle, speed, flower_size])  # (x, y, 각도, 속도, 크기) 저장
        self.update()
        
        # 🌸 첫 번째 꽃이 생성될 때 애니메이션 타이머 시작
        if not self.animate_flower_timer.isActive():
            self.animate_flower_timer.start(50)  # 50ms마다 업데이트

    def animate_flower(self):
        """꽃을 흔들면서 천천히 떨어뜨리는 애니메이션"""
        new_flowers = []
        
        for flower in self.flowers:
            x, y, angle, speed, flower_size = flower
            
            # 흔들림 (좌우 이동)
            x += math.sin(angle) * 3.0  # 흔들림 폭을 작게 (1.5)
            angle += 0.1  # 흔들림 속도도 작게 (0.03)

            # 낙하 (속도를 유지)
            y += speed  # 낙하 속도 고정 (점점 빨라지지 않음)

            if y < self.height():
                new_flowers.append([x, y, angle, speed, flower_size])  # 업데이트

        self.flowers = new_flowers  # 리스트 업데이트
        self.update()

        # 꽃이 모두 사라지면 타이머 정지 (불필요한 실행 방지)
        # if not self.flowers:
        #     self.flower_timer.stop()

    def paintEvent(self, event):
        """ 능력치 차트 그리기 """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(*colorList[self.background_color]))  # 배경을 흰색으로 설정 
        

        if self.cam_label.isVisible():
            for x, y, _, _, flower_size in self.flowers:  # 저장된 크기를 가져옴
                scaled_pixmap = self.flower_pixmap.scaled(flower_size, flower_size, Qt.KeepAspectRatio)
                painter.drawPixmap(QPointF(x, y), scaled_pixmap)  # 해당 크기로 그림

            # 흰색 본문 텍스트
            painter.setFont(QFont("Consolas", 25, QFont.Bold))  # 글꼴 크기            
            painter.setPen(QColor(*colorList['black']))  
            painter.drawText(220, 50, "🔼 상단의 카메라 렌즈를 바라봐주세요 🔼")
        

        # self.reset_button.show() # 항상 표시 (reset button 수정하기 위해서)
        if not self.cam_label.isVisible() and self.skills_mode:
            self.flower_timer.stop()
            hexagon_center_x = 770
            hexagon_center_y = 240
            hexagon_radius = 160
            self.makeBox(painter)
            self.reset_button.show() # reset button 표시

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
        
        if "error" in data:
            self.result_label.setText(f"에러 발생: {data['error']}")
        else:
            self.skills = data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())