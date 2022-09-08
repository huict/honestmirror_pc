import math
import cv2
import numpy as np
import tensorflow as tf
import BodyParts
import Poses_and_Gestures


# the main function that handles the assignment of analysis and threading
# with defined video, obtain frames and perform Tensorflow per frame for results
def performAnalyse(bitarray):
    posenet_output_data = GetPoseNetInformation(bitarray)
    person = convertArrayFrom_1_9_9_7_to_1_34(posenet_output_data)
    feedback_output_data = GetFeedbackInformation(person)

    # extra value needs to be made, as the current data is stored in a double array
    feedback_output_data_poses = feedback_output_data[0]

    highest_scoring_pose = 0
    count = 0
    index = 0
    for pose in feedback_output_data_poses:
        if pose > highest_scoring_pose:
            highest_scoring_pose = pose
            index = count
        count += 1

    pose = ''
    for idx in Poses_and_Gestures.PosesAndGestures:
        if idx.value == index:
            pose = idx.name

    print(f"The highest scoring pose has a score of '{highest_scoring_pose}' and features pose:  '{pose}'")
    return None


def GetPoseNetInformation(bitarray):
    # Load the TFLite model and allocate tensors.
    new_posenet_interpreter = tf.lite.Interpreter(model_path="Neural Network Models/posenet_model.tflite")
    new_posenet_interpreter.allocate_tensors()

    # Get input and output tensors.
    new_posenet_input_details = new_posenet_interpreter.get_input_details()
    new_posenet_output_details = new_posenet_interpreter.get_output_details()

    # Test the model on random input data.
    posenet_input_data = np.array(bitarray, dtype=np.float32)
    new_posenet_interpreter.set_tensor(new_posenet_input_details[0]['index'], posenet_input_data)

    new_posenet_interpreter.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    array = np.array([0, 0, 0, 0], dtype=object)
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

        keypointPositions.append(tuple((maxRow, maxCol)))

    xCoords = [0] * numKeypoints
    yCoords = [0] * numKeypoints
    confidenceScore = np.empty([numKeypoints])
    for keypoint in range(numKeypoints):
        positionX = keypointPositions[keypoint][0]
        positionY = keypointPositions[keypoint][1]

        hfirst = offsets[0][positionY][positionX][keypoint]
        hsecond = offsets[0][positionY][positionX][keypoint + numKeypoints]

        yCoords[keypoint] = positionY * 32 + hsecond
        xCoords[keypoint] = positionX * 32 + hfirst

        yCoords[keypoint] = yCoords[keypoint]
        xCoords[keypoint] = xCoords[keypoint]

        confidenceScore[keypoint] = heatmaps[0][positionY][positionX][keypoint]

    totalscore = 0.0
    Keypointslist = []
    index = 0

    for idx in BodyParts.AllBodyparts:
        Keypointslist.append(
            Keypoints(
                idx.name,
                Position((xCoords[index]), (yCoords[index])),
                confidenceScore[idx.value]
            )
        )
        index += 1
        totalscore += confidenceScore[idx.value]

    score = totalscore / numKeypoints
    person = Person(score, Keypointslist)

    lst = []
    listwith1_34values = []

    for x in person.keyPoints:
        listwith1_34values.append(x.position.x)
        listwith1_34values.append(x.position.y)

    lst.append(listwith1_34values)
    return lst


class Person:
    def __init__(self, score, keypoints):
        self.score = score
        self.keyPoints = keypoints


class Keypoints:
    def __init__(self, bodypart, position, score):
        self.bodypart = bodypart
        self.position = position
        self.score = score


class Position:
    def __init__(self, x, y):
        self.x = x / 257
        self.y = y / 257


def sigmoid(f):
    return 1 / (1 + (math.pow(-f, 2.0)))


# Use OpenCV to retrieve the length of the video given by the user
def getVideoDuration(filename):
    vidcapture = cv2.VideoCapture(filename)
    fps = vidcapture.get(cv2.CAP_PROP_FPS)
    totalNoFrames = vidcapture.get(cv2.CAP_PROP_FRAME_COUNT)
    durationInSeconds = float(totalNoFrames) / float(fps)

    return durationInSeconds
