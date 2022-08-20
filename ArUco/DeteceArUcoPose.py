# a function of detecting the pose of aruco codes

import array
import pyrealsense2 as rs
import cv2
import cv2.aruco as aruco
import numpy as np

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

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)
align = rs.align(rs.stream.color)

def DetectArucoPose(self):
        # get frames
        # this one is for realsense, need to start the pipeline  before using this function
        frames = self.pipeline.wait_for_frames()
        # aligned_frames = align.process(frames)
        # profile = frames.get_profile()
        # depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        # get the width and height
        color_image = np.asanyarray(color_frame.get_data())

        h1, w1 = color_image.shape[:2]
        newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(LU.cameraMatrix, LU.dist, (h1, w1), 0, (h1, w1))
        frame = cv2.undistort(color_image, LU.cameraMatrix, LU.dist, None, newCameraMatrix)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

        parameters = aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if ids is not None:
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.05, LU.cameraMatrix, LU.dist)
            # print("rvec: ", rvec)
            # print("tvex: ", tvec)
            for i in range(rvec.shape[0]):
                tvecCopy = tvec[i, :, :] + [10., 0, 0]
                # print("tvecCopy", tvecCopy)
                aruco.drawAxis(frame, LU.cameraMatrix, LU.dist, rvec[i, :, :], tvec[i, :, :], 0.03)
                aruco.drawDetectedMarkers(frame, corners, ids)
                # print("rvec[", i, ",: , ：]: ", rvec[i, :, :])
            cv2.imshow("arucoDetector", frame)
        
# demo function
while True:
        key = cv2.waitKey(1)
    if key & 0xFF == ord('q') or key == 27:
        break
    DetectArucoPose()
            
