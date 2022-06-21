import os
from cv2 import cv2
import numpy as np
from datetime import timedelta
from PIL import Image as Im

SAVING_FRAMES_PER_SECOND = 24


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
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            print(f"frame is:{frame}")
            cv2.imwrite(os.path.join(filename, f"frame{frame_duration_formatted}.jpg"), frame)
            im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            bitmaparray = im_rgb
            data = Im.fromarray(bitmaparray)
            data.save(f'folder/qwertyuiop{count}.jpg')
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        count += 1
    return


def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    # get the clip duration by dividing number of frames by the number of frames per second
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # use np.arange() to make floating-point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s


def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g. 00:00:20.05)
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return result + ".00".replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")
