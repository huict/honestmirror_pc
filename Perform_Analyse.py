import BodyParts

import tensorflow as tf
import numpy as np
import cv2
import math
from itertools import compress


# the main function that handles the assignment of analysis and threading
# with defined video, obtain frames and perform Tensorflow per frame for results
def performAnalyse(bitarray):
    posenet_output_data = GetPoseNetInformation(bitarray)
    convertArrayFrom_1_9_9_7_to_1_34(posenet_output_data)
    feedback_output_data = GetFeedbackInformation(posenet_output_data)

    # extra value needs to be made, as the current data is stored in a double array
    feedback_output_data_poses = feedback_output_data[0]
    """print(f"Output_Data tensor feedback model: {feedback_output_data_poses}")

    print(feedback_output_data_poses[0])
    print(feedback_output_data_poses[1])
    print(feedback_output_data_poses[2])
    print(feedback_output_data_poses[3])
    print(feedback_output_data_poses[4])
    print(feedback_output_data_poses[5])

    print("most scoring pose:")"""

    highest_scoring_pose = 0
    count = 0
    index = 0
    for pose in feedback_output_data_poses:
        if pose > highest_scoring_pose:
            highest_scoring_pose = pose
            index = count
        count += 1

    print(f"The highest scoring pose has a score of {highest_scoring_pose} and it's on index {index}")

    """integerQueue = np.arange(0, getVideoDuration(filename), 0.04167)
    # print(integerQueue)"""
    return None


def GetPoseNetInformation(bitarray):
    # Load the TFLite model and allocate tensors.
    new_posenet_interpreter = tf.lite.Interpreter(model_path="Neural Network Models/posenet_model.tflite")
    new_posenet_interpreter.allocate_tensors()

    # Get input and output tensors.
    new_posenet_input_details = new_posenet_interpreter.get_input_details()
    new_posenet_output_details = new_posenet_interpreter.get_output_details()

    # Test the model on random input data.
    # new_posenet_input_shape = new_posenet_input_details[0]['shape']
    posenet_input_data = np.array(bitarray, dtype=np.float32)
    new_posenet_interpreter.set_tensor(new_posenet_input_details[0]['index'], posenet_input_data)

    new_posenet_interpreter.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    array = np.array([1, 2, 3, 4], dtype=object)
    posenet_output_data = new_posenet_interpreter.get_tensor(new_posenet_output_details[0]['index'])
    posenet_output_data1 = new_posenet_interpreter.get_tensor(new_posenet_output_details[1]['index'])
    posenet_output_data2 = new_posenet_interpreter.get_tensor(new_posenet_output_details[2]['index'])
    posenet_output_data3 = new_posenet_interpreter.get_tensor(new_posenet_output_details[3]['index'])
    """print(f"Output_Data tensor posenet model: {posenet_output_data}")"""
    array[0] = posenet_output_data
    array[1] = posenet_output_data1
    array[2] = posenet_output_data2
    array[3] = posenet_output_data3
    return array


def GetFeedbackInformation(posenet_output_data):
    # Load the TFLite model and allocate tensors.
    new_feedback_interpreter = tf.lite.Interpreter(model_path="Neural Network Models//feedback_model.tflite")
    new_feedback_interpreter.allocate_tensors()

    # Get input and output tensors.
    new_feedback_input_details = new_feedback_interpreter.get_input_details()
    new_feedback_output_details = new_feedback_interpreter.get_output_details()

    # Test the model on random input data.
    new_feedback_input_shape = new_feedback_input_details[0]['shape']
    feedback_input_data = np.array(posenet_output_data, dtype=np.float32)
    new_feedback_interpreter.set_tensor(new_feedback_input_details[0]['index'], feedback_input_data)

    new_feedback_interpreter.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    feedback_output_data = new_feedback_interpreter.get_tensor(new_feedback_output_details[0]['index'])
    return feedback_output_data


def convertArrayFrom_1_9_9_7_to_1_34(posenet_output_data):
    heatmaps = posenet_output_data[0]
    offsets = posenet_output_data[1]

    for x in range(9):
        for y in range(9):
            for z in range(17):
                f = heatmaps[0][x][y][z]
                sigmoidf = sigmoid(f)
                heatmaps[0][x][y][z] = sigmoidf

    height = len(heatmaps[0])
    width = len(heatmaps[0][0])
    numKeypoints = len(heatmaps[0][0][0])

    keypointPositions = []

    for keypoint in range(numKeypoints):
        maxVal = heatmaps[0][0][0][keypoint]
        maxRow = 0
        maxCol = 0
        for row in range(height):
            for col in range(width):
                if heatmaps[0][row][col][keypoint] > maxVal:
                    maxVal = heatmaps[0][row][col][keypoint]
                    maxRow = row
                    maxCol = col

        print("keypoints = ")
        print(keypoint)
        keypointPositions.append(tuple((maxRow, maxCol)))

    xCoords = [0] * numKeypoints
    yCoords = [0] * numKeypoints
    confidenceScore = np.empty([numKeypoints])
    for keypoint in range(numKeypoints):
        positionX = keypointPositions[keypoint][0]
        positionY = keypointPositions[keypoint][1]

        hfirst = offsets[0][positionY][positionX][keypoint]
        hsecond = offsets[0][positionY][positionX][keypoint + numKeypoints]

        print(f"YCoords before change: {yCoords}")
        yCoords[keypoint] = positionY * 32 + hsecond
        xCoords[keypoint] = positionX * 32 + hfirst
        print(f"YCoords after change: {yCoords}")

        yCoords[keypoint] = yCoords[keypoint]
        xCoords[keypoint] = xCoords[keypoint]

        confidenceScore[keypoint] = heatmaps[0][positionY][positionX][keypoint]

    person = Person
    Keypoints_bodypart = []
    Keypoints_position = []
    Keypoints_score = []
    totalscore = 0.0

    for idx in BodyParts.AllBodyparts:
        for it in BodyParts.AllBodyparts:
            Keypoints_bodypart.append(it.value)
            Keypoints_position.append(Position(xCoords[idx.value], 257))
            Keypoints_position.append(Position(yCoords[idx.value], 257))

            Keypoints_score = confidenceScore[idx.value]
            totalscore += confidenceScore[idx.value]

    person.score = totalscore / numKeypoints
    return person


class Person:
    def __init__(self, score, keypoints):
        self.score = score
        self.keyPoints = keypoints


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setX(self, setter, horizontalres):
        self.x = setter / horizontalres

    def setY(self, setter, verticalres):
        self.y = setter / verticalres


def sigmoid(f):
    return 1 / (1 + (math.pow(-f, 2.0)))


# Use OpenCV to retrieve the length of the video given by the user
def getVideoDuration(filename):
    vidcapture = cv2.VideoCapture(filename)
    fps = vidcapture.get(cv2.CAP_PROP_FPS)
    totalNoFrames = vidcapture.get(cv2.CAP_PROP_FRAME_COUNT)
    durationInSeconds = float(totalNoFrames) / float(fps)

    return durationInSeconds
