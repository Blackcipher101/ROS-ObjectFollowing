#! /usr/bin/python
# Copyright (c) 2015, Rethink Robotics, Inc.

# Using this CvBridge Tutorial for converting
# ROS images to OpenCV2 images
# http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython

# Using this OpenCV2 tutorial for saving Images:
# http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html

# rospy for the subscriber
import rospy
# ROS Image message
from sensor_msgs.msg import Image
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
# OpenCV2 for saving an image
import cv2
import image_processing
pub = None
# Instantiate CvBridge
bridge = CvBridge()
c=1
backSub = cv2.createBackgroundSubtractorMOG2()
def image_callback(msg):
    global c

    #print("Received an image!")
    try:
        # Convert your ROS Image message to OpenCV2
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")

    except CvBridgeError, e:
        print(e)
    else:

        # Save your OpenCV2 image as a jpeg
        if cv2_img is None:
            exit()
        fgMask = backSub.apply(cv2_img)


        cv2.rectangle(cv2_img, (10, 2), (100,20), (255,255,255), -1)


        cv2.imshow('Frame', cv2_img)
        cv2.imshow('FG Mask', fgMask)
        keyboard = cv2.waitKey(30)
        take_action(fgMask)
def take_action(fgMask):
    msg = Twist()
    linear_x = 0
    angular_z = 0

    state_description = ''

    regions=image_processing.process_frame(fgMask)
    if regions['left']>regions['right']:
        print('left')
        linear_x=0.3
        angular_z=-1
    elif regions['left']<regions['right']:
        print('right')
        linear_x=0.3
        angular_z=1
    else:
        print('no object')
        linear_x=0.2

    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pub.publish(msg)


def main():
    global pub

    rospy.init_node('image_listener')
    # Define your image topic
    image_topic = "/rrbot/camera1/image_raw"

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    # Set up your subscriber and define its callback
    rospy.Subscriber(image_topic, Image, image_callback)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()
