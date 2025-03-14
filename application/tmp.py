import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import PathPatch
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from matplotlib.path import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

class PolygonRadarChart(QWidget):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.canvas = FigureCanvas(self.create_radar_chart())
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def create_radar_chart(self):
        labels = self.df.columns[1:]
        num_labels = len(labels)
        angles = [x / float(num_labels) * (2 * np.pi) for x in range(num_labels)]
        angles += angles[:1]  # 시작점과 동일한 끝점 추가
        
        my_palette = cm.get_cmap("Set2", len(self.df.index))

        fig = plt.figure(figsize=(8, 8))
        fig.set_facecolor('white')
        ax = fig.add_subplot(polar=True)

        for i, row in self.df.iterrows():
            color = my_palette(i)
            data = self.df.iloc[i].drop('Character').tolist()
            data += data[:1]

            ax.set_theta_offset(np.pi / 2)  # 시작점 (위쪽)
            ax.set_theta_direction(-1)  # 시계방향

            plt.xticks(angles[:-1], labels, fontsize=13)
            ax.tick_params(axis='x', which='major', pad=15)
            ax.set_rlabel_position(0)
            plt.yticks([0, 2, 4, 6, 8, 10], ['0', '2', '4', '6', '8', '10'], fontsize=10)
            plt.ylim(0, 10)

            ax.plot(angles, data, color=color, linewidth=2, linestyle='solid', label=row.Character)
            ax.fill(angles, data, color=color, alpha=0.4)

        for g in ax.yaxis.get_gridlines():  # 육각형 형태의 grid 적용
            g.get_path()._interpolation_steps = len(labels)

        # 폴리곤 프레임 적용
        spine = Spine(axes=ax, spine_type='circle', path=Path.unit_regular_polygon(len(labels)))
        spine.set_transform(Affine2D().scale(0.5).translate(0.5, 0.5) + ax.transAxes)
        ax.spines = {'polar': spine}

        plt.legend(loc=(0.9, 0.9))
        return fig


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 예제 데이터 (DataFrame 생성)
    data = {
        'Character': ['A', 'B', 'C'],
        'Power': [8, 6, 7],
        'Speed': [7, 8, 6],
        'Skill': [9, 7, 8],
        'Intelligence': [6, 8, 9],
        'Endurance': [8, 9, 7],
    }
    df = pd.DataFrame(data)

    window = PolygonRadarChart(df)
    window.setWindowTitle("Polygon Radar Chart in PyQt5")
    window.show()

    sys.exit(app.exec_())