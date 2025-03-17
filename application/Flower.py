from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QPainterPath, QFont, QMovie, QTransform
from PyQt5.QtCore import Qt, QTimer, QPointF, QRects

class Flower:
    def __init__(self) -> None:
        self.image = QPixmap("./resources/flower.png")