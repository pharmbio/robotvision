import sys
# Add RealSense library path:
sys.path.append("/home/rikard/.pyenv/versions/3.9.0/lib/python3.9/site-packages/pyrealsense2")

import pyrealsense2 as rs
import numpy as np
import cv2
from pyzbar import pyzbar

# Start camera interface
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.infrared, 640, 480, rs.format.y8, 30)

pipeline.start(config)

a = True

try:
    while True:

        # Read image
        frames = pipeline.wait_for_frames()
        infrared_frame = frames.first(rs.stream.infrared)
        IR_image = np.asanyarray(infrared_frame.get_data())

        # Display image
        cv2.imshow('IR image', IR_image)

        # Exit on ESC key
        c = cv2.waitKey(1) % 0x100
        if c == 27:
            break

finally:
    pipeline.stop() 
    cv2.destroyAllWindows()