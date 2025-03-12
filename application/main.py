import sys
import cv2
import numpy as np
import random
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QBrush, QPainterPath, QFont, QPolygonF, QMovie
from PyQt5.QtCore import Qt, QTimer, QPointF, QRect, QThread, pyqtSignal
import math
import Camera as cap
import Api as req
 
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
 
        self.showMaximized() # 최대화면으로 전환
        # self.showFullScreen()  # 전체 화면으로 전환
 
        # 카메라 설정
        self.cap = cap.Camera()
 
        # UI 요소
        self.cam_label = QLabel(self)
        self.cam_label.setFixedSize(640, 480)
        self.cam_label.hide()  # 시작 전에는 숨김
        self.cam_label.setGeometry(200, 60, 640, 480)
 
        self.start_button = QPushButton("✨ 시작하기 ✨", self)
        self.start_button.setStyleSheet("""
            QPushButton {
                font-size: 24px;
                font-weight: bold;
                color: white;
                background-color: rgba(50, 130, 200, 220);
                border-radius: 25px;
                padding: 15px 30px;
                border: 2px solid white;
            }
            QPushButton:hover {
                background-color: rgba(30, 100, 170, 250);
            }
        """)
        self.start_button.clicked.connect(self.start_camera)
 
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
 
        # 레이아웃
        layout = QVBoxLayout()
        # layout.addWidget(self.cam_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)
 
        # 애니메이션을 위한 타이머
        self.timer = QTimer(self)
        self.timer.start(30)
        self.timer.timeout.connect(self.update_frame)
        self.flowers = []  # 시작 전에는 꽃이 없음

        self.loading_label = QLabel(self)
        self.movie = QMovie('loading.gif')
        self.loading_label.setMovie(self.movie)
        self.loading_label.hide()
        layout.addWidget(self.loading_label)
 
        # 캡처 모드 관련 변수
        self.capture_mode = False
        self.skills_mode = False
        self.countdown = 0
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
 
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
                font = QFont("Arial", 100, QFont.Bold)
                painter.setFont(font)
               
                # 검정색 테두리 그리기
                painter.setPen(QColor(0, 0, 0))  # 검정색
                painter.setBrush(Qt.transparent)  # 내부는 투명
 
                # 텍스트 외부에 테두리 그리기 (텍스트가 겹치지 않도록 여러 방향으로 그려서 테두리 효과를 낸다)
                painter.drawText(w // 2 - 30 - 2, h // 2 + 20 - 2, countdown_text)  # 위, 왼쪽
                painter.drawText(w // 2 - 30 + 2, h // 2 + 20 - 2, countdown_text)  # 위, 오른쪽
                painter.drawText(w // 2 - 30 - 2, h // 2 + 20 + 2, countdown_text)  # 아래, 왼쪽
                painter.drawText(w // 2 - 30 + 2, h // 2 + 20 + 2, countdown_text)  # 아래, 오른쪽
 
                # 이제 원래 색으로 텍스트 그리기
                painter.setPen(QColor(255, 255, 150, 255))  # 연노랑색
                painter.drawText(w // 2 - 30, h // 2 + 20, countdown_text)
           
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
        self.update()
 
    def makeBox(self, painter):
        """ 능력치 차트 설명서 """
        pen = QPen(QColor(*colorList['black']), 10, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawRect(25, 25, 400, 500)
 
        pen = QPen(QColor(*colorList['white']), 6, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawRect(25, 25, 400, 500)
 
        text = "Hello, World!\nThis is centered text."
        font = QFont("Arial", 16, QFont.Bold)  # 폰트 설정
        painter.setFont(font)
 
        # 박스 내부에 텍스트를 중앙 정렬
        text_rect = QRect(25, 25, 400, 500)
        painter.drawText(text_rect, Qt.AlignCenter, text)    
 
    def paintEvent(self, event):
        """ 능력치 차트 그리기 """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(*colorList[self.background_color]))  # 배경을 흰색으로 설정
 
 
        if self.cam_label.isVisible() :
            painter.setFont(QFont("Arial", 20, QFont.Bold))  # 글꼴 크기 설정
 
            # 흰색 본문 텍스트
            painter.setPen(QColor(*colorList['black']))  # 연노랑색 (또는 흰색)
            painter.drawText(300, 40, "🔼 상단의 카메라 렌즈를 바라봐주세요 🔼")
        
        if not self.cam_label.isVisible() and self.skills_mode:
            hexagon_center_x = 750
            hexagon_center_y = 270
            hexagon_radius = 150
            self.makeBox(painter)
 
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
            center2 = QPointF(hexagon_center_x-48, hexagon_center_y+7)
            radius2 = hexagon_radius+65
            y_scale = 0.85
 
            for i, label in enumerate(self.skills.keys()):
                text_pos = QPointF(
                    center2.x() + radius2 * math.cos(angles[i]),
                    center2.y() + (radius2 * y_scale * math.sin(angles[i]))
                )
                painter.setPen(QColor(*colorList['black']))
                painter.setFont(QFont("Arial", 20, QFont.Bold))
                painter.drawText(text_pos, label)
 
            painter.end()

    def closeEvent(self, event):
        """ 프로그램 종료 시 카메라 해제 """
        self.cap.close()
        event.accept()

    def start_request(self):
        self.movie.start()
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
