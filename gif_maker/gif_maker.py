# pip3 install imageio
# python -m pip install imageio


# pip install opencv-python
"""
Video
  ↓
Extract Frames (Via OpenCV)
  ↓
frame001.png
frame002.png
frame003.png
...
  ↓
Generate GIF
"""

import cv2

input_video = "video.mp4"
video = cv2.VideoCapture(input_video)

frame_num = 0

while True:
    success, frame = video.read()

    if not success:
        break

    cv2.imwrite(
        f"frame_{frame_num:04d}.png",
        frame
    )

    frame_num += 1

video.release()

import imageio.v3 as iio

from glob import glob

filenames = sorted(glob("frame_*.png"))
# filenames = ['frame_num*.png', 'frame_num*.png'] # Manual selection
images = [ ]

for filename in filenames:
  images.append(iio.imread(filename))

filename_output = 'team.gif'

iio.imwrite(filename_output, images, duration = 500, loop = 0)