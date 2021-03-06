#!/usr/bin/env python
# vim:set ts=4 sw=4 et:
#
# Copyright 2015 UAVenture AG.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
# Updated: Tarek Taha : tarek.taha@kustar.ac.ae, Vladimir Ermakov
#    - Changed topic names after re-factoring : https://github.com/mavlink/mavros/issues/233
#    - Use mavros.setpoint module for topics

import rospy
import thread
import threading
import time
import mavros
import tf
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
from math import *
from mavros.utils import *
from mavros import setpoint as SP
from tf.transformations import quaternion_from_euler

from geometry_msgs.msg import Pose
from skimage.measure import structural_similarity as ssim
from geometry_msgs.msg import PoseStamped
class SetpointPosition:
    """
    This class sends position targets to FCU's position controller
    """
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.currentPoseX = 0
        self.currentPoseY = 0
        self.currentPoseZ = 0
        self.image_ID=0
        self.image_data=[]
        self.cvImage=[]
        self.bridge=CvBridge()
        self.image2Analyze=[]
        # publisher for mavros/setpoint_position/local
        self.pub = SP.get_pub_position_local(queue_size=10)
        # subscriber for mavros/local_position/local
        self.sub = rospy.Subscriber(mavros.get_topic('local_position', 'pose'),
                                    SP.PoseStamped, self.reached)
        self.waypointsub = rospy.Subscriber("/uav_3/waypoint", SP.PoseStamped, self.updateposition, queue_size=1)
        self.image_pub=rospy.Publisher("/uav_3/downward_cam/image_output", Image, queue_size=10)
        self.camsub=rospy.Subscriber("/uav_3/downward_cam/camera/image", Image, self.image_callback)
        self.psmsub=rospy.Subscriber("/uav_3/odometry_sensor1/pose", PoseStamped, self.ps_callback, queue_size=10)
        self.f=open('/home/kuri/catkin_ws/src/graph_slam/IOfiles/analysis.txt','w')
        self.done = False
        self.done_evt = threading.Event()
        try:
            thread.start_new_thread(self.navigate, ())
        except:
            fault("Error: Unable to start thread")


    def updateposition(self,p):
        self.setPose(p.pose.position.x,p.pose.position.y,p.pose.position.z,0,False)
    def navigate(self):
        rospy.loginfo("Navigate")
        rate = rospy.Rate(10)   # 10hz

        msg = SP.PoseStamped(
            header=SP.Header(
                frame_id="base_footprint",  # no matter, plugin don't use TF
                stamp=rospy.Time.now()),    # stamp should update
        )

        while not rospy.is_shutdown():
            msg.pose.position.x = self.x
            msg.pose.position.y = self.y
            msg.pose.position.z = self.z

            # For demo purposes we will lock yaw/heading to north.
            yaw_degrees = 0  # North
            yaw = radians(yaw_degrees)
            quaternion = quaternion_from_euler(0, 0, yaw)
            msg.pose.orientation = SP.Quaternion(*quaternion)

            self.pub.publish(msg)
            rate.sleep()

    def setPose(self, x, y, z, delay=0, wait=True):
        self.done = False
        self.x = x
        self.y = y
        self.z = z

        if wait:
            rate = rospy.Rate(5)
            while not self.done and not rospy.is_shutdown():
                rate.sleep()
        time.sleep(delay)

    def takeoff(self, z, delay=0, wait=True):
        diff = z - self.currentPoseZ
        while not abs(diff)<0.2:
            diff = z - self.currentPoseZ
            print diff
            if diff>0:
                self.setPose(self.currentPoseX,self.currentPoseY,self.currentPoseZ + 1 ,2)
            else:
                self.setPose(self.currentPoseX,self.currentPoseY,self.currentPoseZ - 1 ,2)

    def land(self, delay=0, wait=True):
        altitude = self.currentPoseZ
        while altitude > 0.2:
            altitude = self.currentPoseZ
            self.setPose(self.currentPoseX,self.currentPoseY,self.currentPoseZ - 1 ,2)

    def reached(self, topic):
        def is_near(msg, x, y):
            rospy.logdebug("Position %s: local: %d, target: %d, abs diff: %d",
                           msg, x, y, abs(x - y))
            return abs(x - y) < 0.2
        self.currentPoseX = topic.pose.position.x
        self.currentPoseY = topic.pose.position.y
        self.currentPoseZ = topic.pose.position.z

        if is_near('X', topic.pose.position.x, self.x) and \
           is_near('Y', topic.pose.position.y, self.y) and \
           is_near('Z', topic.pose.position.z, self.z):
            self.done = True
            self.done_evt.set()

    def ps_callback(self, ps):
	    self.ps = ps
    def image_callback(self, data):
        self.image_data=data
        try:    
            self.cvImage=self.bridge.imgmsg_to_cv2(self.image_data, "bgr8")
        except CvBridgeError, e: 
            print e 

        self.image2Analyze=self.cvImage.copy()

        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(self.image2Analyze, "bgr8"))
        except CvBridgeError, e: 
            print e

    def save_image(self, image_ID, x, y,r):
        #cv2.imwrite('/home/kuri/catkin_ws/src/kuri_mbzirc_challenge_3/kuri_mbzirc_challenge_3/images/image'+str(image_ID))+'x'+str(int(x))+'y'+str(int(y))+'r'+str(int(r))+'.jpeg', self.image2Analyze)
        cv2.imwrite('/home/kuri/catkin_ws/src/graph_slam/images/image'+str(image_ID)+'.jpeg', self.image2Analyze)
    def motion_model(self, x, y, z, delay=0, wait=True):
	previous_ps=self.ps.pose.position
    	previous_orientation=self.ps.pose.orientation
    	prev_quaternion = (previous_orientation.x, previous_orientation.y, previous_orientation.z, 		previous_orientation.w)     
    	prev_euler = tf.transformations.euler_from_quaternion(prev_quaternion)
    	prev_yaw = prev_euler[2]
    	prev_yaw %= 2 * pi
	
    	self.setPose(x, y, z, delay)
    	current_ps=self.ps.pose.position
    	current_orientation=self.ps.pose.orientation
    	current_quaternion = (current_orientation.x, current_orientation.y, current_orientation.z, current_orientation.w)     
    	current_euler = tf.transformations.euler_from_quaternion(current_quaternion)
    	current_yaw = current_euler[2]
    	current_yaw %= 2 * pi	
    	drones_image=self.image2Analyze
    	print previous_ps.x, previous_ps.y, current_ps.x, current_ps.y, prev_yaw, current_yaw
        self.f.write(str(self.image_ID)+'\t'+str(current_ps.x)+'\t'+str(current_ps.y)+'\n')
	self.save_image(self.image_ID, current_ps.x, current_ps.y, current_yaw)
	self.image_ID+=1
    	

def setpoint_demo():
    rospy.init_node('setpoint_position_demo_3')
    mavros.set_namespace('/uav_3/mavros')
    rate = rospy.Rate(10)
    setpoint = SetpointPosition()
    time.sleep(1)
    x_max=22.5
    y_max=40
    y_min=-40
    print "taking off"
    setpoint.takeoff(10.0)
    for k in range (2):
        for i in range (5):
                print "Moving to Pose:",i
                setpoint.motion_model(x_max,y_max-((i)*20),10,25)         
                print "Reached Pose: ", i, "Saving Image..."
               
        x_max-=15
        for j in range (5):
                print "Moving to Pose:",j
                setpoint.motion_model(x_max, y_min+((j)*20),10,25) 
                print "Reached Pose: ", j, "Saving Image..."
                
        x_max-=15
        
    print "Landing"
    #rospy.loginfo("Landing")
    setpoint.land()
    print "landed"
    rospy.loginfo("Bye!")
def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	s = ssim(imageA, imageB)
	return s

if __name__ == '__main__':
    try:
        setpoint_demo()
    except rospy.ROSInterruptException:
        pass
