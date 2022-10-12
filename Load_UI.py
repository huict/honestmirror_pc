import sys

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QSizePolicy, QVBoxLayout, QMessageBox)
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton

import Perform_Analysis
from Extract_Frames import FrameFetching


class ShowAllFeedbackWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Honest Mirror")
        lstWithAllFeedback = Perform_Analysis.listWithFeedback
        layout = QVBoxLayout()
        for feedbackPerFrame in lstWithAllFeedback:
            s = ""
            for pose in feedbackPerFrame:
                s += str(pose)
                s += " | "
            self.label = QLabel(s)
            layout.addWidget(self.label)
        self.setLayout(layout)


# Show how often specific poses have been held and features feedback voor the poses found 10 times or more
class CountPosesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Honest Mirror")
        lst = Perform_Analysis.listWithFeedback
        layout = QVBoxLayout()

        crossed_arms = sum(sublist.count('crossed_arms') for sublist in lst)
        delivered_gestures = sum(sublist.count('delivered_gestures') for sublist in lst)
        back_to_audience = sum(sublist.count('giving_the_back_to_the_audience') for sublist in lst)
        hands_in_pocket = sum(sublist.count('hands_in_pockets') for sublist in lst)
        on_one_leg = sum(sublist.count('standing_with_the_bodyweight_on_one_leg') for sublist in lst)
        hands_touching_face = sum(sublist.count('hands_touching_face') for sublist in lst)

        layout.addWidget(QLabel(f"Crossed_arms featured: {crossed_arms} times"))
        layout.addWidget(QLabel(f"Delivered_gestured featured: {delivered_gestures} times"))
        layout.addWidget(QLabel(f"Giving_the_back_to_the_audience featured: {back_to_audience} times"))
        layout.addWidget(QLabel(f"Hands_in_pockets featured: {hands_in_pocket} times"))
        layout.addWidget(QLabel(f"Standing_with_the_bodyweight_on_one_leg featured: {on_one_leg} times"))
        layout.addWidget(QLabel(f"Hands_touching_face featured: {hands_touching_face} times"))
        layout.addWidget(QLabel(""))

        lst2 = [crossed_arms, delivered_gestures, back_to_audience, hands_in_pocket, on_one_leg, hands_touching_face]
        counter = 0
        file = open("assets/feedbackmessages(EN).txt", "r")
        for textfileLine in file:
            if counter % 2 != 0:
                if lst2[(counter // 2)] >= 10:
                    label = QLabel(f"{textfileLine}")
                    label.adjustSize()
                    label.setWordWrap(True)
                    layout.addWidget(label)

            counter += 1

        self.setLayout(layout)


# noinspection PyUnresolvedReferences,PyAttributeOutsideInit
# The main function that sets the opening window, featuring the logo and button to start analysis
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

            self.w = ShowAllFeedbackWindow()
            self.w.show()
            self.c = CountPosesWindow()
            self.c.show()

    @staticmethod
    def exitCall():
        sys.exit(app.exec_())


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
