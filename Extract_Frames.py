import os
from datetime import timedelta
import cv2
import numpy as np

import Perform_Analysis
from Perform_Analysis import performAnalysis

SAVING_FRAMES_PER_SECOND = 10
image_width = 257
image_height = 257
dim = (image_width, image_height)


# uses video sent by user to determine frame timeslots
# receive a frame from the video with the timeslot given with the right proportions
# passes the frame to the neural network functions
def FrameFetching(video):
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
    count = 0

    while True:
        is_read, frame = cap.read()
        if not is_read:
            break
        frame_duration = count / fps

        try:
            closest_duration = saving_frames_durations[0]
        except IndexError:
            break
        if frame_duration >= closest_duration:
            resized_image = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            resized_image = resized_image.astype(np.float32)
            bitarray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
            bitarray = np.expand_dims(bitarray, axis=0)

            performAnalysis(bitarray, frame_duration)

            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        count += 1

    feedbacklist = Perform_Analysis.listWithFeedback
    return feedbacklist


# A function that returns the list of durations where to save the frames
# get the clip duration by dividing number of frames by the number of frames per second
# use np.arange() to make floating-point steps
# used by frame_fetching()
def get_saving_frames_durations(cap, saving_fps):
    saved_timestamps = []
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        saved_timestamps.append(i)
    return saved_timestamps


# create folder and save the array as an image with openCV
# unused
def save_frames_in_local_folder(video, frame_duration, resized_image):
    filename, _ = os.path.splitext(video)
    filename += "-opencv"
    if not os.path.isdir(filename):
        os.mkdir(filename)
    frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
    cv2.imwrite(os.path.join(filename, f"frame{frame_duration_formatted}.jpg"), resized_image)

    """# save image from bitarray
    data = Im.fromarray(bitarray)
    data.save(f'folder/{count}.jpg')"""
    return None


# Utility function to format timedelta objects in a cool way (e.g. 00:00:20.05) omitting microseconds and retaining milliseconds
# used by save_frames_in_local_folder()
# unused
def format_timedelta(td):
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return result + ".00".replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")


# For Testing Purposes
def writeBitarrayToFile(bitarray):
    f = open("assets/demofile2.txt", "w")
    for i in bitarray:
        f.write(str(i))

    f.close()
    return True

