
import re
import os
import linecache
import cv2 
import matplotlib.pyplot as plt
import numpy as np


img = np.zeros([2000, 3500, 3],dtype=np.uint8)
img.fill(0) # or img[:] = 255

x_offset=y_offset=0

images_list= os.listdir("/home/kuri/catkin_ws/src/graph_slam/images/")
positions=[]
for image in images_list:
	patch=cv2.imread("/home/kuri/catkin_ws/src/graph_slam/images/"+str(image))

	match = re.match(r"([a-z]+)([0-9]+)", image, re.I)
	if match:
	    	items = match.groups()
		imageID=int(items[1])
		print imageID
	line = linecache.getline('/home/kuri/catkin_ws/src/graph_slam/IOfiles/estimated_poses.txt', imageID+1)
	pose=line.split()

	x_odom=int(round(float(pose[0])))
	y_odom=int(round(float(pose[1])))
	if (x_odom>=0 and y_odom>=0):	
		
		x_image=(img.shape[1]/2)-int(x_odom*26.85)
		y_image=(img.shape[0]/2)+int(y_odom*26.85)
		x_offset=x_image-320
		y_offset=y_image-240
		
		print x_odom, y_odom
		print x_offset, y_offset
		img[y_offset:y_offset+patch.shape[0], x_offset:x_offset+patch.shape[1]] = patch
	elif (x_odom>=0 and y_odom<=0):	
		
		x_image=(img.shape[1]/2)- int(x_odom*26.85)
		y_image=(img.shape[0]/2)- abs(int(y_odom*26.85))
		x_offset=x_image-320
		y_offset=y_image-240
		
		print x_odom, y_odom
		print x_offset, y_offset
		img[y_offset:y_offset+patch.shape[0], x_offset:x_offset+patch.shape[1]] = patch

	elif (x_odom<=0 and y_odom>=0):	
		
		x_image=(img.shape[1]/2)+abs(int(x_odom*26.85))
		y_image=(img.shape[0]/2)+int(y_odom*26.85)
		x_offset=x_image-320
		y_offset=y_image-240
		
		print x_odom, y_odom
		print x_offset, y_offset
		img[y_offset:y_offset+patch.shape[0], x_offset:x_offset+patch.shape[1]] = patch

	elif (x_odom<=0 and y_odom<=0 ):	
		
		x_image=(img.shape[1]/2)+ abs(int(x_odom*26.85))
		y_image=(img.shape[0]/2)- abs(int(y_odom*26.85))
		x_offset=x_image-320
		y_offset=y_image-240
		
		print x_odom, y_odom
		print x_offset, y_offset
		img[y_offset:y_offset+patch.shape[0], x_offset:x_offset+patch.shape[1]] = patch

print positions

plt.imshow(img),plt.title('Input')

cv2.imwrite('/home/kuri/catkin_ws/src/graph_slam/maps/constructed_map.jpeg', img)

plt.show()
