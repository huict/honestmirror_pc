from cv2 import cv2
import numpy

framecount = 24


# the main function that handles the assignment of analysis and threading
# with defined video, obtain frames and perform Tensorflow per frame for results
def performAnalyse(filename):
    bitmapList = []
    bitmapQueue = []

    integerQueue = numpy.arange(0, getVideoDuration(filename), 0.04167)
    print(integerQueue)
    return None


# Use OpenCV to retrieve the length of the video given by the user
def getVideoDuration(filename):
    vidcapture = cv2.VideoCapture(filename)
    fps = vidcapture.get(cv2.CAP_PROP_FPS)
    totalNoFrames = vidcapture.get(cv2.CAP_PROP_FRAME_COUNT)
    durationInSeconds = float(totalNoFrames) / float(fps)

    return durationInSeconds
