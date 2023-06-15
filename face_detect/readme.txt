This ROS package contains a node which will perform face detection using openCV libraries

Package also contains launch file which will start the following nodes:
    1) usb_cam
    2) my_node
    3) rqt_image_view

Dependencies: 
 - cv_bridge
 - rospy
 - std_msgs
 - openCV
 - python2
 - usb_cam
 - rqt_image_view

Author: Archit K Jaiswal
ROS Version: Melodic 1.14.13
OS Version: Ubuntu 18.04.6 LTS
Platform: NVIDIA Jetson Nano Developer Kit - Jetpack 4.6.3 [L4T 32.7.3]

Use the following command to execute the entire project:

$ roslaunch face_detect face_detect.launch