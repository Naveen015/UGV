#!/usr/bin/python

import Adafruit_DHT
import rospy
from std_msgs.msg import Float32MultiArray

def humidity():
	sensor = Adafruit_DHT.DHT11
	pin = 4
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	data = [humidity,temperature]
	return data 

def talker(data):
	pub = rospy.Publisher('humidity', FLoat32MultiArray, queue_size=10)
	rospy.init_node('humidity', anonymous=True)
     	rate = rospy.Rate(10) # 10hz
     	while not rospy.is_shutdown():
        	rospy.loginfo(data)
        	pub.publish(data)
        	rate.sleep()

if __name__ == '__main__':
	try:
		data=humidity()
		talker(data)
     	except rospy.ROSInterruptException:
                pass
