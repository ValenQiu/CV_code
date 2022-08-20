import pyrealsense2 as rs
import cv2
import cv2.aruco as aruco
import numpy as np
import math


class Realsense:
    # Camera
    fx = 461.84448242
    fy = 443.28289795
    cx = 308.69522309
    cy = 177.70244623
    k1 = 0.04266696
    k2 = -0.11292418
    p1 = 0.00306782
    p2 = -0.00409565
    k3 = 0.02006348
    cameraMatrix = np.array([[fx, 0, cx],
                             [0, fy, cy],
                             [0, 0, 1]])
    dist = np.array([k1, k2, p1, p2, k3])

    def start(self):
        # Configure depth and color streams
        config = rs.config()
        # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        # Start streaming
        self.pipeline = rs.pipeline()
        self.pipeline.start(config)

    def stop(self):
        self.pipeline.stop()
        cv2.destroyAllWindows()

    def show_image(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        # get the width and height
        color_image = np.asanyarray(color_frame.get_data())
        cv2.imshow("image", color_image)


lu = LU()
lu.start()
while True:
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q') or key == 27:
        lu.stop()
        break
    centers, angles= lu.DetectArucoPose()
    print("centers", centers)
    print("angles", angles)
