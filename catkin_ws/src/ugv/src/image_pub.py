#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image

import cv2
from cv_bridge import CvBridge, CvBridgeError

rospy.init_node('VideoPublisher', anonymous=True)

VideoRaw = rospy.Publisher('VideoRaw', Image, queue_size=10)

cam = cv2.VideoCapture('output.avi')

while cam.isOpened():
    meta, frame = cam.read()

    # I want to publish the original Image
    msg_frame = CvBridge().cv2_to_imgmsg(frame)

    VideoRaw.publish(msg_frame)

    time.sleep(0.1)
