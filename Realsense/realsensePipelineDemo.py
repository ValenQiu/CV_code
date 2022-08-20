import pyrealsense2 as rs
import cv2
import numpy as np

# Camera
fx = 1.18346606e+03
fy = 1.18757422e+03
cx = 3.14407234e+02
cy = 2.38823696e+02
k1 = -0.51328742
k2 = 0.33232725
p1 = 0.01683581
p2 = -0.00078608
k3 = -0.1159959
cameraMatrix = np.array([[fx, 0, cx],
                         [0, fy, cy],
                         [0, 0, 1]])
dist = np.array([k1, k2, p1, p2, k3])

# Start streaming
pipeline.start(config)
align = rs.align(rs.stream.color)

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)
align = rs.align(rs.stream.color)


# the function of set up camera, return the image from realsense (optional)
def Camera():
    global pipeline, align
    frames = pipeline.wait_for_frames()
    # aligned_frames = align.process(frames)
    # profile = frames.get_profile()
    # depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    # get the width and height
    color_image = np.asanyarray(color_frame.get_data())

    # remove the dist
    h1, w1 = color_image.shape[:2]
    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (h1, w1), 0, (h1, w1))
    frame = cv2.undistort(color_image, cameraMatrix, dist, None, newCameraMatrix)
    # height, width, channel = frame.shape
    # print(height, " ", width)
    # cv2.imshow("frame", frame)
    return frame

  
while True:
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)
    profile = frames.get_profile()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    # get the width and height
    color_image = np.asanyarray(color_frame.get_data())
    depth_image = np.asanyarray(depth_frame.get_data())

    # remove the dist
    h1, w1 = color_image.shape[:2]
    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (h1, w1), 0, (h1, w1))
    frame = cv2.undistort(color_image, cameraMatrix, dist, None, newCameraMatrix)
    height, width, channel = frame.shape
    print(height, " ", width)
    cv2.imshow("frame", frame)

