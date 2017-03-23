import math
f=open('/home/kuri/catkin_ws/src/graph_slam/IOfiles/analysis.txt','r')
f2=open('/home/kuri/catkin_ws/src/graph_slam/IOfiles/landmarks.txt','w')
image_ID=[]
object_color=[]
object_xPosition=[]
object_yPosition=[]
object_shape=[]
object_area=[]
object_ID=[]
for line in f:

	object_prop=line.split()
	if(object_prop[5]!='unknown'):
		image_ID.append(object_prop[0])
		object_color.append(object_prop[1])
		object_area.append(object_prop[2])
		object_xPosition.append(object_prop[3])
		object_yPosition.append(object_prop[4])
		object_shape.append(object_prop[5])
		if (object_prop[5]=='square'):
			if (object_prop[1]=='red'):
				object_ID.append(20)
			elif (object_prop[1]=='green'):
				object_ID.append(1)
			elif (object_prop[1]=='blue'):
				object_ID.append(2)
			elif (object_prop[1]=='cyan'):
				object_ID.append(3)
			elif (object_prop[1]=='yellow'):
				object_ID.append(4)
			elif (object_prop[1]=='magenta'):
				object_ID.append(5)
			elif (object_prop[1]=='orange'):
				object_ID.append(6)
		elif (object_prop[5]=='large_circle'):
			if (object_prop[1]=='red'):
				object_ID.append(7)
			elif (object_prop[1]=='green'):
				object_ID.append(8)
			elif (object_prop[1]=='blue'):
				object_ID.append(9)
			elif (object_prop[1]=='cyan'):
				object_ID.append(10)
			elif (object_prop[1]=='yellow'):
				object_ID.append(11)
			elif (object_prop[1]=='magenta'):
				object_ID.append(12)
			elif (object_prop[1]=='orange'):
				object_ID.append(13)
		elif (object_prop[5]=='small_circle'):
			if (object_prop[1]=='red'):
				object_ID.append(14)
			elif (object_prop[1]=='green'):
				object_ID.append(15)
			elif (object_prop[1]=='blue'):
				object_ID.append(16)
			elif (object_prop[1]=='cyan'):
				object_ID.append(17)
			elif (object_prop[1]=='yellow'):
				object_ID.append(18)
			elif (object_prop[1]=='magenta'):
				object_ID.append(19)
			elif (object_prop[1]=='orange'):
				object_ID.append(0)
		elif (object_prop[5]=='rectangle'):
			if (object_prop[1]=='red'):
				object_ID.append(21)
			elif (object_prop[1]=='green'):
				object_ID.append(22)
			elif (object_prop[1]=='blue'):
				object_ID.append(23)
			elif (object_prop[1]=='cyan'):
				object_ID.append(24)
			elif (object_prop[1]=='yellow'):
				object_ID.append(25)
			elif (object_prop[1]=='magenta'):
				object_ID.append(26)
			elif (object_prop[1]=='orange'):
				object_ID.append(27)

for i in range(len(object_ID)):
	#image_ID	Object_ID 	xDistance to landmark (in pixels)	yDistance to landmark (in pixels)
	distX=-int(object_xPosition[i])+320
	distY=+int(object_yPosition[i])-240
	
	f2.write(str(image_ID[i])+'\t'+str(object_ID[i])+'\t'+str(((10*math.tan(math.radians(50)))/320)*(distX))+'\t'+str(((10*math.tan(math.radians(50)))/320)*(distY))+'\n')
	#f2.write(str(image_ID[i])+'\t'+str(object_ID[i])+'\t'+str(((10*math.tan(math.radians(50)))/320)*(320-int(object_xPosition[i])))+'\t'+str(((10*math.tan(math.radians(50)))/320)*(240-int(object_yPosition[i])))+'\n')
