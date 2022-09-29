import os
from datetime import timedelta

import cv2
import numpy as np

from Perform_Analyse import performAnalyse

SAVING_FRAMES_PER_SECOND = 24
image_width = 257
image_height = 257
dim = (image_width, image_height)


# Creates a folder, retrieves frames from the video and saves them in the folder
# make a folder by the name of the video file
# read the video file
# get the FPS of the video
# if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
# get the list of duration spots to save
# start the loop
# break out of the loop if there are no frames to read
# get the duration by dividing the frame count by the FPS
# get the earliest duration to save
# the list is empty, all duration frames were saved
# if closest duration is less than or equals the frame duration,
# then save the frame
# drop the duration spot from the list, since this duration spot is already saved
# increment the frame count
def FrameFetching(video):
    filename, _ = os.path.splitext(video)
    filename += "-opencv"
    if not os.path.isdir(filename):
        os.mkdir(filename)
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

            """ # save the array as an image with openCV
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            cv2.imwrite(os.path.join(filename, f"frame{frame_duration_formatted}.jpg"), resized_image)
            
                # save image from bitarray
            data = Im.fromarray(bitarray)
            data.save(f'folder/{count}.jpg')
            """
            performAnalyse(bitarray)

            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        count += 1
    return


# A function that returns the list of durations where to save the frames
# get the clip duration by dividing number of frames by the number of frames per second
# use np.arange() to make floating-point steps
def get_saving_frames_durations(cap, saving_fps):
    saved_timestamps = []
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        saved_timestamps.append(i)
    return saved_timestamps


# Utility function to format timedelta objects in a cool way (e.g. 00:00:20.05) omitting microseconds and retaining milliseconds
def format_timedelta(td):
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return result + ".00".replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")
