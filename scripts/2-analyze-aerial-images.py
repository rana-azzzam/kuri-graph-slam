
import re
import os

import cv2 
import matplotlib.pyplot as plt
import numpy as np


def identinfy_shape (area): 
	if (area >= 1300 and area <=2000):
		return 'square'
	elif (area >=600 and area <=850):
		return 'large_circle'
	elif (area >=35 and area <=70):
		return 'small_circle'
	elif (area >=250 and area <=450):
		return 'rectangle'
	else: 
		return 'unknown'
lower_red=np.array([0, 200, 200])
upper_red=np.array([10, 255, 255])

lower_green=np.array([50, 200 ,200])
upper_green=np.array([70, 255, 255])

lower_blue=np.array([110,200,200])
upper_blue=np.array([130,255,255])

lower_yellow=np.array([20, 200, 200])
upper_yellow=np.array([40, 255, 255])

lower_cyan=np.array([80, 200 ,200])
upper_cyan=np.array([100, 255, 255])

lower_magenta=np.array([140,200,200])
upper_magenta=np.array([160,255,255])

lower_orange=np.array([10, 200, 200])
upper_orange=np.array([19, 255, 255])

f=open('/home/kuri/catkin_ws/src/graph_slam/IOfiles/analysis.txt','w')

images_list= os.listdir("/home/kuri/catkin_ws/src/graph_slam/images/")
positions=[]
for image in images_list:
	patch=cv2.imread("/home/kuri/catkin_ws/src/graph_slam/images/"+str(image))
	hsv=cv2.cvtColor(patch, cv2.COLOR_BGR2HSV)
	match = re.match(r"([a-z]+)([0-9]+)", image, re.I)
	if match:
	    	items = match.groups()
		print items
		imageID=items[1]
		centroids=[]
		mask_blue=cv2.inRange(hsv, lower_blue, upper_blue)
		_,mask_blue = cv2.threshold(mask_blue,0,255,cv2.THRESH_OTSU)
		h, w = mask_blue.shape[:2]
		contours0, hierarchy = cv2.findContours( mask_blue.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
		moments  = [cv2.moments(cnt) for cnt in contours0]
		areas = [cv2.contourArea(cnt) for cnt in contours0]
		centroids=[]
		for m in moments:
			if (m['m00']!=0):
				centroids.append ([int(round(m['m10']/m['m00'])),int(round(m['m01']/m['m00'])) ]) 
			else:
				centroids.append ([0,0])
		for i in range (len(areas)):
			if (areas[i])>20: 
				f.write(imageID+'\tblue\t'+ str(areas[i])+ '\t'+str(centroids[i][0])+ '\t'+str(centroids[i][1])+ '\t'+ identinfy_shape(areas[i])+ '\n')
		centroids=[]
		mask_green=cv2.inRange(hsv, lower_green, upper_green)
		_,mask_green = cv2.threshold(mask_green,0,255,cv2.THRESH_OTSU)
		h, w = mask_green.shape[:2]
		contours0, hierarchy = cv2.findContours(mask_green.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
		moments  = [cv2.moments(cnt) for cnt in contours0]
		areas = [cv2.contourArea(cnt) for cnt in contours0]
		centroids=[]
		for m in moments:
			if (m['m00']!=0):
				centroids.append ([int(round(m['m10']/m['m00'])),int(round(m['m01']/m['m00'])) ]) 
			else:
				centroids.append ([0,0])
		for i in range (len(areas)):
			if (areas[i])>20:
				f.write(imageID+'\tgreen\t'+ str(areas[i])+ '\t'+str(centroids[i][0])+ '\t'+str(centroids[i][1])+ '\t'+ identinfy_shape(areas[i])+'\n')
		centroids=[]
		mask_orange=cv2.inRange(hsv, lower_orange, upper_orange)
		_,mask_orange = cv2.threshold(mask_orange,0,255,cv2.THRESH_OTSU)
		h, w = mask_orange.shape[:2]

		contours0, hierarchy = cv2.findContours( mask_orange.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
		moments  = [cv2.moments(cnt) for cnt in contours0]
		areas = [cv2.contourArea(cnt) for cnt in contours0]
		for m in moments:
			if (m['m00']!=0):
				centroids.append ([int(round(m['m10']/m['m00'])),int(round(m['m01']/m['m00'])) ]) 
			else:
				centroids.append ([0,0])
		for i in range (len(areas)):
			if (areas[i])>20:
				f.write(imageID+'\torange\t'+ str(areas[i])+ '\t'+str(centroids[i][0])+ '\t'+str(centroids[i][1])+ '\t'+ identinfy_shape(areas[i])+'\n')
		centroids=[]
		mask_yellow=cv2.inRange(hsv, lower_yellow, upper_yellow)
		_,mask_yellow = cv2.threshold(mask_yellow,0,255,cv2.THRESH_OTSU)
		h, w = mask_yellow.shape[:2]
		contours0, hierarchy = cv2.findContours( mask_yellow.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
		moments  = [cv2.moments(cnt) for cnt in contours0]
		areas = [cv2.contourArea(cnt) for cnt in contours0]
		for m in moments:
			if (m['m00']!=0):
				centroids.append ([int(round(m['m10']/m['m00'])),int(round(m['m01']/m['m00'])) ]) 
			else:
				centroids.append ([0,0])
		for i in range (len(areas)):
			if (areas[i])>20:
				f.write(imageID+'\tyellow\t'+ str(areas[i])+ '\t'+str(centroids[i][0])+ '\t'+str(centroids[i][1])+ '\t'+ identinfy_shape(areas[i])+'\n')
		centroids=[]
		mask_magenta=cv2.inRange(hsv, lower_magenta, upper_magenta)
		_,mask_magenta = cv2.threshold(mask_magenta,0,255,cv2.THRESH_OTSU)
		h, w = mask_magenta.shape[:2]
		contours0, hierarchy = cv2.findContours( mask_magenta.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
		moments  = [cv2.moments(cnt) for cnt in contours0]
		areas = [cv2.contourArea(cnt) for cnt in contours0]
		for m in moments:
			if (m['m00']!=0):
				centroids.append ([int(round(m['m10']/m['m00'])),int(round(m['m01']/m['m00'])) ]) 
			else:
				centroids.append ([0,0])
		for i in range (len(areas)):
			if (areas[i])>20:
				f.write(imageID+'\tmagenta\t'+ str(areas[i])+ '\t'+str(centroids[i][0])+ '\t'+str(centroids[i][1])+ '\t'+ identinfy_shape(areas[i])+'\n')
		centroids=[]
		mask_red=cv2.inRange(hsv, lower_red, upper_red)
		_,mask_red = cv2.threshold(mask_red,0,255,cv2.THRESH_OTSU)
		h, w = mask_red.shape[:2]
		contours0, hierarchy = cv2.findContours( mask_red.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
		moments  = [cv2.moments(cnt) for cnt in contours0]
		areas = [cv2.contourArea(cnt) for cnt in contours0]
		for m in moments:
			if (m['m00']!=0):
				centroids.append ([int(round(m['m10']/m['m00'])),int(round(m['m01']/m['m00'])) ]) 
			else:
				centroids.append ([0,0])
		for i in range (len(areas)):
			if (areas[i])>20:
				f.write(imageID+'\tred\t'+ str(areas[i])+ '\t'+str(centroids[i][0])+ '\t'+str(centroids[i][1])+ '\t'+ identinfy_shape(areas[i])+'\n')

		centroids=[]
		mask_cyan=cv2.inRange(hsv, lower_cyan, upper_cyan)
		_,mask_cyan = cv2.threshold(mask_cyan,0,255,cv2.THRESH_OTSU)
		h, w = mask_cyan.shape[:2]
		contours0, hierarchy = cv2.findContours( mask_cyan.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
		moments  = [cv2.moments(cnt) for cnt in contours0]
		areas = [cv2.contourArea(cnt) for cnt in contours0]
		for m in moments:
			if (m['m00']!=0):
				centroids.append ([int(round(m['m10']/m['m00'])),int(round(m['m01']/m['m00'])) ]) 
			else:
				centroids.append ([0,0])
		for i in range (len(areas)):
			if (areas[i])>20:
				f.write(imageID+'\tcyan\t'+ str(areas[i])+ '\t'+str(centroids[i][0])+ '\t'+str(centroids[i][1])+ '\t'+ identinfy_shape(areas[i])+'\n')


