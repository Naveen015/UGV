#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from imutils import build_montages
from datetime import datetime
import numpy as np
import imagezmq
import argparse
import imutils
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", default=MobileNetSSD_deploy.prototxt,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", default=MobileNetSSD_deploy.caffemodel,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
ap.add_argument("-mW", "--montageW", type=int, default=1,
	help="montage frame width")
ap.add_argument("-mH", "--montageH", type=int, default=1,
	help="montage frame height")
args = vars(ap.parse_args())

def image_callback():
	# initialize the list of class labels MobileNet SSD was trained to
	# detect, then generate a set of bounding box colors for each class
	CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "tvmonitor", "cellphone", "bottle", "laptop", "book", "clock", "scissors"]

	# load our serialized model from disk
	print("[INFO] loading model...")
	net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

	# initialize the consider set (class labels we care about and want
	# to count), the object count dictionary, and the frame  dictionary
	CONSIDER = set(["person", "cellphone","laptop","book","clock","scissors"])
	objCount = {obj: 0 for obj in CONSIDER}
	frameDict = {}

	# assign montage width and height so we can view all incoming frames
	# in a single "dashboard"
	mW = args["montageW"]
	mH = args["montageH"]
	print("[INFO] detecting: {}...".format(", ".join(obj for obj in
		CONSIDER)))
	cv2_img = bridge.imgmsg_to_cv2(image, "bgr8")
	while True:
		frame = imutils.resize(cv2_img, width=800)
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
			0.007843, (300, 300), 127.5)

		# pass the blob through the network and obtain the detections and
		# predictions
		net.setInput(blob)
		detections = net.forward()

		# reset the object count for each object in the CONSIDER set
		objCount = {obj: 0 for obj in CONSIDER}

		# loop over the detections
		for i in np.arange(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with
			# the prediction
			confidence = detections[0, 0, i, 2]

			# filter out weak detections by ensuring the confidence is
			# greater than the minimum confidence
			if confidence > args["confidence"]:
				# extract the index of the class label from the
				# detections
				idx = int(detections[0, 0, i, 1])

				# check to see if the predicted class is in the set of
				# classes that need to be considered
				if CLASSES[idx] in CONSIDER:
					# increment the count of the particular object
					# detected in the frame
					objCount[CLASSES[idx]] += 1

					# compute the (x, y)-coordinates of the bounding box
					# for the object
					box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
					(startX, startY, endX, endY) = box.astype("int")

					# draw the bounding box around the detected object on
					# the frame
					cv2.rectangle(frame, (startX, startY), (endX, endY),
						(255, 0, 0), 2)
					cv2.putText(frame, CLASSES[idx], (startX+2, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

		# draw the sending device name on the frame
		cv2.putText(frame, rpiName, (10, 25),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

		# draw the object count on the frame
		#label = ", ".join("{}: {}".format(obj, count) for (obj, count) in
		#	objCount.items())
		#cv2.putText(frame, label, (10, h - 20),
		#	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255,0), 2)

		# update the new frame in the frame dictionary
		frameDict[rpiName] = frame

		# build a montage using images in the frame dictionary
		montages = build_montages(frameDict.values(), (w, h), (mW, mH))

		# display the montage(s) on the screen
		for (i, montage) in enumerate(montages):
			cv2.imshow("Home pet location monitor ({})".format(i),
				montage)

		# detect any kepresses
		key = cv2.waitKey(1) & 0xFF
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

	# do a bit of cleanup
	cv2.destroyAllWindows()
	

    
def listener():

	# In ROS, nodes are uniquely named. If two nodes with the same
	# name are launched, the previous one is kicked off. The
    	# anonymous=True flag means that rospy will choose a unique
    	# name for our 'listener' node so that multiple listeners can
    	# run simultaneously.
	rospy.init_node('listener', anonymous=True)
	ultrasonic_data=rospy.Subscriber("ultrasonic", Float32MultiArray)
	humidity_data=rospy.Subscriber("humidity", Float32MultiArray)
	accelerometer_data=rospy.Subscriber("accelerometer", Float32MultiArray)
	image=rospy.Subscriber("VideoRaw", Image, image_callback)

	
	#print  
   	spin() #simply keeps python from exiting until this node is stopped
   	rospy.spin()

if __name__ == '__main__':
	listener()
