#!/usr/bin/env python2
import cv2
import rospy
from sensor_msgs.msg import Image
from threading import Lock
from cv_bridge import CvBridge, CvBridgeError

class ImagePipeline:
    def __init__(self):
        self.mutex = Lock()
        rospy.init_node('my_node', anonymous=True)
        self.bridge = CvBridge()
        topic = '/usb_cam/image_raw'
        imRos = rospy.Subscriber(topic, Image, self.imageCallBack, queue_size=3)
        self.ImOut = rospy.Publisher('/out/image', Image, queue_size=3)
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print("Rospy Spin Shut down")

    def imageCallBack(self, inp_im):
        try:
            imCV = self.bridge.imgmsg_to_cv2(inp_im, "bgr8")
        except CvBridgeError as e:
            print(e)
        if imCV is None:
            print ('frame dropped, skipping tracking')
        else:
            self.ImageProcessor(imCV)

    def ImageProcessor(self, cvImg):
        faceCascade = cv2.CascadeClassifier('/home/archit/catkin_ws/src/face_detect/src/cascade.xml')
        gray = cv2.cvtColor(cvImg, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
                            gray,
                            scaleFactor=1.1,
                            minNeighbors=5,
                            minSize=(30, 30),
                            flags=cv2.CASCADE_SCALE_IMAGE
                            )
         # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(cvImg, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # cv2.imshow("CV Image windows", cvImg)
        # cv2.waitKey(1)

        #converting the image to ROS image
        outImg = CvBridge().cv2_to_imgmsg(cvImg, encoding="bgr8")
        
        # Publish new image
        self.ImOut.publish(outImg)

imgProc = ImagePipeline()