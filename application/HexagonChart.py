import math
from PyQt5.QtGui import QPen, QBrush, QPolygonF, QFont, QColor
from PyQt5.QtCore import QPointF, Qt

colorList = {
    'blue': QColor(0, 0, 255),
    'white': QColor(255, 255, 255),
    'black': QColor(0, 0, 0),
    'gray': QColor(128, 128, 128),
    'chart_skyblue' : QColor(0, 150, 255),
    'dark_gray': QColor(64, 64, 64),
}

class HexagonChart:
    def __init__(self, x, y, radius, font) -> None:
        self.center = QPointF(x, y)
        self.angles = [math.radians(60*i) for i in range(6)]
        self.radius = radius
        self.font = font
    def draw_hexagon(self, painter, radius, color, pend_width=1, alpha=200) :
        hexagon_points = [
            QPointF(radius * math.cos(angle), radius * math.sin(angle))
            + self.center for angle in self.angles
        ]

        color.setAlpha(alpha)
        painter.setPen(QPen(color, pend_width))
        painter.drawPolygon(QPolygonF(hexagon_points))

        # 육각형 테두리
        if alpha != 200:    
            painter.setPen(colorList['white'])
            for point in hexagon_points:
                painter.drawLine(self.center, point)

    def draw_chart(self, painter) :
        # 내부 육각형들
        for i in range(5):
            self.draw_hexagon(painter, self.radius * i / 5, colorList['gray'])

        # 가장 외부
        self.draw_hexagon(painter, self.radius, colorList['black'], 2, 255)

    def draw_results(self, painter, skills) :
        points = []
        labels = []
        for i, (key, val) in enumerate(skills.items()):
            points.append(
                QPointF(
                    (val/100) * math.cos(self.angles[i]) * self.radius,
                    (val/100) * math.sin(self.angles[i]) * self.radius
                ) + self.center
            )
            labels.append(key)

        # 육각형 내부 (stat)
        painter.setPen(QPen(colorList['dark_gray'], 1))
        color = colorList['chart_skyblue']
        color.setAlpha(130)
        painter.setBrush(QBrush(color))
        painter.drawPolygon(QPolygonF(points))

        # status 글씨
        painter.setPen(colorList['black'])
        painter.setFont(QFont(self.font, 25, QFont.Bold))

        center = self.center + QPointF(-25, 10)
        radius2 = self.radius + 26
        y_scale = 0.97

        for l, angle in zip (labels, self.angles) :
            pos = QPointF(
                radius2 * math.cos(angle),
                radius2 * y_scale * math.sin(angle)
            ) + center
            painter.drawText(pos, l)
