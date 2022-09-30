import cv2
import numpy as np
import tensorflow as tf
import Poses_and_Gestures
from convert_Posenet_to_Person import convertPosenetToPerson

listWithFeedback = []


# the main function that handles the assignment of analysis and threading
# with defined video, obtain frames and perform Tensorflow per frame for results
def performAnalyse(bitarray, frame_duration):
    posenet_output_data = GetPoseNetInformation(bitarray)
    person = convertPosenetToPerson(posenet_output_data)
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

    if pose != '':
        print(f"'{frame_duration}','{pose}'")
        listWithFeedback.append(tuple((frame_duration, pose)))

    return None


# Obtain PoseNet information (the 17 keypoints on a body) with an image as input
def GetPoseNetInformation(bitarray):
    # Load the TFLite model and allocate tensors.
    new_posenet_interpreter = tf.lite.Interpreter(model_path="Neural Network Models/posenet_model.tflite")
    new_posenet_interpreter.allocate_tensors()

    # Get input and output tensors.
    new_posenet_input_details = new_posenet_interpreter.get_input_details()
    new_posenet_output_details = new_posenet_interpreter.get_output_details()

    # Test the model on input data.
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
    array[0] = posenet_output_data  # heatmap
    array[1] = posenet_output_data1  # offsets
    array[2] = posenet_output_data2
    array[3] = posenet_output_data3
    return array


# Obtain Feedback information (gestures and poses) with an Person object as input
def GetFeedbackInformation(posenet_output_data):
    # Load the TFLite model and allocate tensors.
    new_feedback_interpreter = tf.lite.Interpreter(model_path="Neural Network Models//feedback_model.tflite")
    new_feedback_interpreter.allocate_tensors()

    # Get input and output tensors.
    new_feedback_input_details = new_feedback_interpreter.get_input_details()
    new_feedback_output_details = new_feedback_interpreter.get_output_details()

    # Test the model on input data.
    feedback_input_data = np.array(posenet_output_data, dtype=np.float32)
    new_feedback_interpreter.set_tensor(new_feedback_input_details[0]['index'], feedback_input_data)

    new_feedback_interpreter.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    feedback_output_data = new_feedback_interpreter.get_tensor(new_feedback_output_details[0]['index'])
    return feedback_output_data


# Use OpenCV to retrieve the length of the video given by the user
# Unused
def getVideoDuration(filename):
    vidcapture = cv2.VideoCapture(filename)
    fps = vidcapture.get(cv2.CAP_PROP_FPS)
    totalNoFrames = vidcapture.get(cv2.CAP_PROP_FRAME_COUNT)
    durationInSeconds = float(totalNoFrames) / float(fps)

    return durationInSeconds
