#!/usr/bin/python
import RPi.GPIO as GPIO
import time

#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Float32MultiArray

def sonic(trig,ech):
	try:
	      GPIO.setmode(GPIO.BOARD)

	      PIN_TRIGGER = trig
	      PIN_ECHO = ech

	      GPIO.setup(PIN_TRIGGER, GPIO.OUT)
	      GPIO.setup(PIN_ECHO, GPIO.IN)

	      GPIO.output(PIN_TRIGGER, GPIO.LOW)

	      time.sleep(2)

	      GPIO.output(PIN_TRIGGER, GPIO.HIGH)

	      time.sleep(0.00001)

	      GPIO.output(PIN_TRIGGER, GPIO.LOW)

	      while GPIO.input(PIN_ECHO)==0:
	            pulse_start_time = time.time()
	      while GPIO.input(PIN_ECHO)==1:
	            pulse_end_time = time.time()

	      pulse_duration = pulse_end_time - pulse_start_time
	      distance = round(pulse_duration * 17150, 2)
	      return distance

	finally:
	      GPIO.cleanup()

def talker(dist):
	pub = rospy.Publisher('ultrasonic', FLoat32MultiArray, queue_size=10)
	rospy.init_node('talker', anonymous=True)
     	rate = rospy.Rate(10) # 10hz
     	while not rospy.is_shutdown():
        	rospy.loginfo(dist)
        	pub.publish(dist)
        	rate.sleep()

if __name__ == '__main__':
	try:
		trig1=1
		trig2=2
		trig3=3
		trig4=4
		echo1=1
		echo2=2
		echo3=3
		echo4=4
		dist1=sonic(trig1,echo1)
		dist2=sonic(trig2,echo2)
		dist3=sonic(trig3,echo3)
		dist4=sonic(trig4,echo4)
		dist=[dist1,dist2,dist3,dist4]
		talker(dist)
     	except rospy.ROSInterruptException:
                pass





