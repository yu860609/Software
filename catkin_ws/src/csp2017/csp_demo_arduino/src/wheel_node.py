#!/usr/bin/env python
import rospy
import numpy as np
from duckietown_msgs.msg import BoolStamped, Twist2DStamped

class arduinoWheel(object):
    def __init__(self):
        self.detected = BoolStamped()
        self.detected.data = False
        self.wait=BoolStamped()
        self.wait.data=False
        # =========== publisher ===========
        self.car_cmd=rospy.Publisher("~car_cmd",Twist2DStamped,queue_size=1)
        # publish to topic "car_cmd" (you may have to see the code last week)

        # =========== subscriber ===========
        self.pub_result=rospy.Subscriber("~result",BoolStamped,self.cbresult,queue_size=1)
        self.pub_carReturn=rospy.Subscriber("~carReturn",BoolStamped,self.cbCarReturn,queue_size=1)
        # subscribe to topic "result" (you should see arduino_node.py)

   # =========== subscribe distance from arduino ===========
    def cbresult(self, msg):
        cmd = Twist2DStamped()
        if self.wait.data==False:
            if msg.data==False:
                print "go forward"
                cmd.v=0
                cmd.omega=0
                self.car_cmd.publish(cmd)
                if self.detected.data == True:
                    print "return now"
                    cmd.v=0.3
                    cmd.omega=4
                    self.car_cmd.publish(cmd)
                    self.stop()
                    self.wait.data = True
            else:
                print "go backward"
                cmd.v=0.3
                cmd.omega=0
                self.car_cmd.publish(cmd)
    #===========ccccccc===========
    def cbCarReturn(self, msg):
        if msg.data == True:
            self.detected.data = True
            print "I saw it!!!!!!!!!"
    #==========stop time=========
    def stop(self):
        rospy.sleep(5)
        cmd = Twist2DStamped()
        cmd.v = 0
        cmd.omega = 0
        self.car_cmd.publish(cmd)
if __name__ == "__main__":
    rospy.init_node("arduino_wheel", anonymous = False)
    arduino_node = arduinoWheel()
    rospy.spin()
