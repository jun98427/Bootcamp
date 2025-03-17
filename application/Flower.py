from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QPainterPath, QFont, QMovie, QTransform
from PyQt5.QtCore import Qt, QTimer, QPointF, QRect
import random
import math

class Flower:
    def __init__(self, width, height) -> None:
        self.image = QPixmap("/home/willtek/Bootcamp/application/resources/flower.png")
        self.flowers = []
        self.width = width
        self.height = height

    def create_flower(self, is_initial = False):
        """꽃을 생성하고 위치를 리스트에 추가"""
        flower_size = random.randint(20, 60)  # 랜덤한 꽃 크기 설정
        
        if is_initial:
            section_width = self.width // 10  # 🌿 화면을 10등분하여 분포 균일화
            x = random.randint(0, 9) * section_width + random.randint(0, section_width - flower_size)
            y = random.randint(0, self.height)  # 🌸 화면 중간까지 랜덤한 높이에서 시작
        else:
            x = random.randint(flower_size // 2, self.width - flower_size // 2)
            y = -flower_size  # 기존처럼 화면 위에서 생성
        speed = random.uniform(1, 7)  # 낙하 속도 (랜덤)
        
        angle = random.uniform(0, 2 * math.pi)  # 흔들림을 위한 초기 각도
        rotation = random.randint(0, 360)  # 🌸 회전 각도 (0~360도)
        rotation_speed = random.uniform(-10, 10)  # 🌸 회전 속도 (랜덤한 방향으로 회전)

        self.flowers.append([x, y, angle, speed, flower_size, rotation, rotation_speed])
        # self.update()

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

            if y < self.height:
                new_flowers.append([x, y, angle, speed, flower_size, rotation, rotation_speed])  # 업데이트

        self.flowers = new_flowers
        # self.update()

    def draw_flowers(self, painter) :
        for flower in self.flowers:
            x, y, _, _, flower_size, rotation, _ = flower

            # 🌸 꽃 이미지 로드
            # flower_pixmap = QPixmap("/home/willtek/Bootcamp/application/resources/flower.png")  
            flower_pixmap = self.image.scaled(flower_size, flower_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # 🎨 회전 적용
            painter.save()  # 💾 현재 상태 저장 (변환 이전 상태)
            
            transform = QTransform()
            transform.translate(x + flower_size / 2, y + flower_size / 2)  # 중심 이동
            transform.rotate(rotation)  # 회전
            transform.translate(-flower_size / 2, -flower_size / 2)  # 원래 자리로 되돌리기

            painter.setTransform(transform)
            painter.drawPixmap(0, 0, flower_pixmap)  # (0, 0)은 변환된 좌표 기준

            painter.restore()  # 🔄 원래 상태로 복구 (회전 해제)