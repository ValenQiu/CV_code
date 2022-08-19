# a function of detecting the pose of aruco codes

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
            
