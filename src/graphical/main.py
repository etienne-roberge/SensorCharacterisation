import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from mathgl import *
import numpy as np


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.label = QLabel("Empty")
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

        self.mglData = mglData()
        self.mglData.Create(6, 9)
        self.mglGraph = mglGraph(0, 600, 500)
        self.mglGraph.Rotate(60, 250)
        self.mglGraph.Light(True)
        self.mglGraph.SetTicks('x', 1, 0);
        self.mglGraph.Alpha(False)
        self.mglGraph.SetRanges(0, 6, 0, 4, -800, 800)
        self.mglGraph.Axis()

        self.updateTimer = QTimer()
        self.updateTimer.timeout.connect(self.updateGraph)
        self.updateTimer.start(200)

    def updateGraph(self):
        image = QImage(np.array(self.mglGraph.GetRGBA()), self.mglGraph.GetWidth(), self.mglGraph.GetHeight(), QImage.Format_RGBA8888)
        self.label.setPixmap(QPixmap.fromImage(image))

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()