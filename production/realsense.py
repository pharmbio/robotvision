# import sys
# Add RealSense library path:
# sys.path.append("/home/rikard/.pyenv/versions/3.9.0/lib/python3.9/site-packages/pyrealsense2")
import pyrealsense2 as rs
import numpy as np
import cv2

framerate = 6
width = 1280
height = 720

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, framerate)

class Livefeed(object):
    def __init__(self):
        pipeline.start(config)

    def __del__(self):
        pipeline.stop()

    def get_frame(self):
        frame = pipeline.wait_for_frames()
        color_frame = frame.get_color_frame()

        image = np.asanyarray(color_frame.get_data())
        (ret, jpeg) = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
