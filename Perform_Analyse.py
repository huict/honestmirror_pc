import BodyParts

import tensorflow as tf
import numpy as np
import cv2
import math
from enum import Enum

# the main function that handles the assignment of analysis and threading
# with defined video, obtain frames and perform Tensorflow per frame for results
def performAnalyse(filename, bitarray):
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
    posenet_output_data = new_posenet_interpreter.get_tensor(new_posenet_output_details[0]['index'])
    """print(f"Output_Data tensor posenet model: {posenet_output_data}")"""
    return posenet_output_data


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
    # [[[[121, 2121, 12121, 21212]]]]
    x = np.empty([1, 1, 1, 4], dtype=int)

    heatmaps = posenet_output_data[0]
    offset = posenet_output_data[1]

    for x in range(9):
        print(x)
        for y in range(9):
            print(y)
            for z in range(17):
                print(z)
                f = heatmaps[0][x][y][z]
                sigmoidf = sigmoid(f)
                heatmaps[0][x][y][z] = sigmoidf

    height = len(heatmaps[0])
    width = len(heatmaps[0][0])
    numKeypoints = len(heatmaps[0][0][0])

    # keypointPositions = np.Array(numKeypoints)  {Pair(0, 0)}
    keypointPositions = []

    for keypoint in range(numKeypoints):
        maxVal = heatmaps[0][0][0][keypoint]
        maxRow = 0
        maxCol = 0
        for row in range(height):
            for col in range(width):
                heatmaps[0][row][col][keypoint] = heatmaps[0][row][col][keypoint]
                if heatmaps[0][row][col][keypoint] > maxVal:
                    maxVal = heatmaps[0][row][col][keypoint]
                    maxRow = row
                    maxCol = col

        keypointPositions[keypoint].append(tuple((maxRow, maxCol)))

    xCoords = np.Array(numKeypoints)
    yCoords = np.Array(numKeypoints)
    confidenceScore = np.Array(numKeypoints)
    for idx in keypointPositions:
        for position in keypointPositions:
            positionX = keypointPositions[idx].first
            positionY = keypointPositions[idx].second

            hfirst = offset[0][positionY][positionX][idx]
            hsecond = offset[0][positionY][positionX][idx + numKeypoints]

            yCoords[idx] = (positionY * 32 + hsecond)
            xCoords[idx] = (positionX * 32 + hfirst)

            yCoords = yCoords[idx]
            xCoords = xCoords[idx]

            confidenceScore[idx] = heatmaps[0][positionY][positionX][idx]

    person = Person
    keypointList = np.Array(numKeypoints)
    totalscore = 0.0

    for idx in BodyParts.AllBodyparts:
        for it in BodyParts.AllBodyparts:
            keypointList[idx].AllBodyparts = it
            keypointList[idx].position.setX(xCoords[idx], 257)
            keypointList[idx].position.setY(yCoords[idx], 257)

            keypointList[idx].score = confidenceScore[idx]
            totalscore += confidenceScore[idx]

    person.score = totalscore / numKeypoints
    return person


class Person:
    def __init__(self, score, keypoints):
        self.score = score
        self.keyPoints = keypoints


def sigmoid(f):
    return 1 / (1 + (math.pow(-f.toDouble(), 2.0)))


# Use OpenCV to retrieve the length of the video given by the user
def getVideoDuration(filename):
    vidcapture = cv2.VideoCapture(filename)
    fps = vidcapture.get(cv2.CAP_PROP_FPS)
    totalNoFrames = vidcapture.get(cv2.CAP_PROP_FRAME_COUNT)
    durationInSeconds = float(totalNoFrames) / float(fps)

    return durationInSeconds
