#!/usr/bin/python

import rospy
import time
import board
import busio
import adafruit_adxl34x
from std_msgs.msg import Float32MultiArray

def accelerometer():
	i2c = busio.I2C(board.SCL, board.SDA)
	accelerometer = adafruit_adxl34x.ADXL345(i2c)

	while True:
		time.sleep(1)
	data=accelerometer.acceleration
	return data

def talker(data):
	pub = rospy.Publisher('accelerometer', FLoat32MultiArray, queue_size=10)
	rospy.init_node('accelerometer', anonymous=True)
     	rate = rospy.Rate(10) # 10hz
     	while not rospy.is_shutdown():
        	rospy.loginfo(data)
        	pub.publish(data)
        	rate.sleep()

if __name__ == '__main__':
	try:
		data=accelerometer()
		talker(data)
     	except rospy.ROSInterruptException:
                pass
