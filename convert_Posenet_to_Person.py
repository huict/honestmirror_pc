import math
import numpy as np
import BodyParts


def convertPosenetToPerson(posenet_output_data):
    heatmaps = posenet_output_data[0]
    offsets = posenet_output_data[1]

    for x in range(9):
        for y in range(9):
            for z in range(17):
                heatmap_value = heatmaps[0][x][y][z]
                sigmoid_value = sigmoid(heatmap_value)
                heatmaps[0][x][y][z] = sigmoid_value

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

    for personKeypoint in person.keyPoints:
        listwith1_34values.append(personKeypoint.position.x)
        listwith1_34values.append(personKeypoint.position.y)

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
    i = 1 / (1 + (math.pow(-f, 2.0)))
    return i
