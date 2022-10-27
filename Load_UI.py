import sys

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QSizePolicy, QVBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem,
                             QMainWindow, QWidget, QPushButton, QHeaderView)

import Perform_Analysis
from Extract_Frames import FrameFetching


# Window that shows the results of the neural network, including the timestamps and recognized poses
# Creates table with rows and columns based on the length of the feedback results
# Table gets filled with the results from the neural network
class ShowAllFeedbackWindow(QWidget):
    def __init__(self, lst_with_feedback):
        super().__init__()
        self.title = 'Honest Mirror Detailed Results Screen'
        self.setWindowTitle(self.title)

        self.createTable(lst_with_feedback)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

    # Table initiation and filling with results from the neural network
    # noinspection PyAttributeOutsideInit
    def createTable(self, lstwithfeedback):
        self.tableWidget = QTableWidget()

        # Determines the row count based on the feedbacklist
        self.tableWidget.setRowCount(len(lstwithfeedback))

        # Determines the column count based on the feedbacklist
        feedbacklength = 0
        for feedbackFrame in lstwithfeedback:
            if len(feedbackFrame) >= feedbacklength:
                feedbacklength = len(feedbackFrame)
        self.tableWidget.setColumnCount(feedbacklength)

        # TODO: Find a way to name extra columns if 2 or poses are recognized in one frame
        self.tableWidget.setHorizontalHeaderLabels(('Timestamp', 'Pose Recognized'))

        # Fills the table with the results from the neural network
        for feedbackFrame in lstwithfeedback:
            index = lstwithfeedback.index(feedbackFrame)
            for i in range(feedbacklength):
                self.tableWidget.setItem(index, i, QTableWidgetItem(str(feedbackFrame[i])))

        # Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


# noinspection PyUnresolvedReferences,PyAttributeOutsideInit
# Shows how often specific poses have been held and features feedback for the poses found 10 or more times
# Also gives the user the opportunity to open and close the table window at will
class CountPosesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Honest Mirror")
        listWithFeedback = Perform_Analysis.listWithFeedback
        layout = QVBoxLayout()

        # Searches how often a pose has been held in the feedbacklist
        crossed_arms = sum(sublist.count('crossed_arms') for sublist in listWithFeedback)
        delivered_gestures = sum(sublist.count('delivered_gestures') for sublist in listWithFeedback)
        back_to_audience = sum(sublist.count('giving_the_back_to_the_audience') for sublist in listWithFeedback)
        hands_in_pocket = sum(sublist.count('hands_in_pockets') for sublist in listWithFeedback)
        on_one_leg = sum(sublist.count('standing_with_the_bodyweight_on_one_leg') for sublist in listWithFeedback)
        hands_touching_face = sum(sublist.count('hands_touching_face') for sublist in listWithFeedback)

        # Fills the layout with the above results
        layout.addWidget(QLabel("<b>The following results have been found from your analysed video:</b>"))
        layout.addWidget(QLabel(f"Crossed_arms featured: {crossed_arms} times"))
        layout.addWidget(QLabel(f"Delivered_gestured featured: {delivered_gestures} times"))
        layout.addWidget(QLabel(f"Giving_the_back_to_the_audience featured: {back_to_audience} times"))
        layout.addWidget(QLabel(f"Hands_in_pockets featured: {hands_in_pocket} times"))
        layout.addWidget(QLabel(f"Standing_with_the_bodyweight_on_one_leg featured: {on_one_leg} times"))
        layout.addWidget(QLabel(f"Hands_touching_face featured: {hands_touching_face} times"))
        layout.addWidget(QLabel(""))

        # TODO: remove lst2 and just use the poses from the file
        # Looks up which poses have been held for 10 or more times, then adds those poses to the layout
        layout.addWidget(QLabel("<b>If some poses have been detected 10 or more times,"
                                " feedback about those poses will be shown below:</b> "))
        lst2 = [crossed_arms, delivered_gestures, back_to_audience, hands_in_pocket, on_one_leg, hands_touching_face]
        counter = 0
        file = open("Assets/feedbackmessages(EN).txt", "r")
        for textfileLine in file:
            if counter % 2 != 0:
                if lst2[(counter // 2)] >= 10:
                    label = QLabel(f"{textfileLine}")
                    label.adjustSize()
                    label.setWordWrap(True)
                    layout.addWidget(label)

            counter += 1

        # Creates a button for the window with table
        self.w = ShowAllFeedbackWindow(listWithFeedback)
        self.openButton = QPushButton("Open detailed screen")
        self.openButton.setToolTip("Open detailed screen")
        self.openButton.setStatusTip("Open detailed screen")
        self.openButton.clicked.connect(self.showScreen)
        self.openButton.setFixedHeight(24)
        layout.addWidget(self.openButton)

        self.setLayout(layout)
        file.close()

    def showScreen(self):
        if self.w.isVisible():
            self.w.hide()
        else:
            self.w.show()
        pass


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
        self.pixmap = QPixmap('Assets/logo.png')

        self.pixmap = self.pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.FastTransformation)

        # adding image to label
        self.label.setPixmap(self.pixmap)

        # Optional, resize label to image size
        self.label.resize(self.pixmap.width(),
                          self.pixmap.height())

        self.error = QLabel()
        self.error.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Creates button with functionality
        openButton = QPushButton("Open a video for analysis")
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

    # Shows the user the file manager of the computer in which they can select their video for analysis
    # Once a video has been selected, the URI will be used to access the video throughout the app
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

            self.c = CountPosesWindow()
            self.c.show()

    @staticmethod
    def exitCall():
        sys.exit(app.exec_())


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
