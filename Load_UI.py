import collections
import sys

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QSizePolicy, QVBoxLayout, QMessageBox)
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton

import Perform_Analysis
from Extract_Frames import FrameFetching


class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        lst = Perform_Analysis.listWithFeedback
        layout = QVBoxLayout()
        for i in lst:
            s = ""
            for j in i:
                s += str(j)
                s += " | "
            self.label = QLabel(s)
            layout.addWidget(self.label)
        self.setLayout(layout)


class CountWindow(QWidget):
    def __init__(self):
        super().__init__()
        lst = Perform_Analysis.listWithFeedback
        layout = QVBoxLayout()
        ca = sum(sublist.count("crossed_arms") for sublist in lst)
        dg = sum(sublist.count("delivered_gestures") for sublist in lst)
        bta = sum(sublist.count("giving_the_back_to_the_audience") for sublist in lst)
        hip = sum(sublist.count("hands_in_pockets") for sublist in lst)
        swbool = sum(sublist.count("standing_with_the_bodyweight_on_one_leg") for sublist in lst)
        htf = sum(sublist.count("hands_touching_face") for sublist in lst)

        self.label = QLabel(f"Crossed_arms featured: {ca} times")
        layout.addWidget(self.label)
        self.label = QLabel(f"Delivered_gestured featured: {dg} times")
        layout.addWidget(self.label)
        self.label = QLabel(f"Giving_the_back_to_the_audience featured: {bta} times")
        layout.addWidget(self.label)
        self.label = QLabel(f"Hands_in_pockets featured: {hip} times")
        layout.addWidget(self.label)
        self.label = QLabel(f"Standing_with_the_bodyweight_on_one_leg featured: {swbool} times")
        layout.addWidget(self.label)
        self.label = QLabel(f"Hands_touching_face featured: {htf} times")
        layout.addWidget(self.label)
        self.setLayout(layout)


# noinspection PyUnresolvedReferences
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Honest Mirror")
        self.setGeometry(0, 0, 500, 500)

        # creating label
        self.label = QLabel(self)

        # loading image
        self.pixmap = QPixmap('assets/logo.png')

        self.pixmap = self.pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.FastTransformation)

        # adding image to label
        self.label.setPixmap(self.pixmap)

        # Optional, resize label to image size
        self.label.resize(self.pixmap.width(),
                          self.pixmap.height())

        self.error = QLabel()
        self.error.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        openButton = QPushButton("Open a Video for analysis")
        openButton.setToolTip("Open Video File")
        openButton.setStatusTip("Open Video File")
        openButton.setFixedHeight(24)
        openButton.clicked.connect(self.openFile)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(openButton)

        # Set widget to contain window contents
        wid.setLayout(layout)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a video for analysis",
                                                  QDir.homePath(), filter="*.mp4;*.avi;*.mov;*.flv;*.mkv")

        if fileName != '':
            print(f"{fileName}")
            print("starting frame cutting...")
            FrameFetching(fileName)
            print("finished!")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Analysis complete")
            dlg.setText("The Frame extraction has been complete")
            dlg.exec()

            self.w = AnotherWindow()
            self.w.show()
            self.c = CountWindow()
            self.c.show()

    @staticmethod
    def exitCall():
        sys.exit(app.exec_())


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
