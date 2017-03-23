import numpy as np
def displayResults(numSteps, numLandmarks, result):
    f=open('/home/kuri/catkin_ws/src/graph_slam/IOfiles/estimated_poses.txt', 'w')
    print 'Estimated Pose(s):'
    for i in range(numSteps+1):
        print '    ['+ ', '.join('%.3f'%x for x in result[2*i]) + ', ' \
            + ', '.join('%.3f'%x for x in result[2*i+1]) +']'
	f.write(', '.join('%.3f'%x for x in result[2*i]) + '\t' \
            + ', '.join('%.3f'%x for x in result[2*i+1]) +'\n')

    print 'Estimated Landmarks:'
    for i in range(numLandmarks):
        print '    ['+ ', '.join('%.3f'%x for x in result[2*(numSteps+i)]) + ', ' \
            + ', '.join('%.3f'%x for x in result[2*(numSteps+i)+1]) +']'


def SLAM(data, initialPosObservations, numSteps, numLandmarks, motionNoise, measurementNoise):

    	#Initialize the Omega and Xi matrices
    	#Note: Xi has width=2 because of (x,y) coordinates to store 
   	np.set_printoptions(threshold='nan')
	dimension=(1+numSteps)*2+numLandmarks*2
	omega = (dimension,dimension)	
	omega = np.matrix(np.zeros(omega))
	xi=(dimension,1)
	xi=np.matrix(np.zeros(xi))
	omega[0,0] += 1
	omega[1,1] += 1
	#initial position
	xi[0,0]    += 40
	xi[1,0]    += (-22.5)
	#initial position observations
	i=0
	print 'len(omega)', len(omega)
	for j in range (len(initialPosObservations)):
	
			Z      =initialPosObservations[j]
			lmIndex=Z[0]
			lmX    =Z[1]
			lmY    =Z[2]

			omega[2*i,2*i] 			  				+= 1/measurementNoise
			omega[2*i,(1+numSteps)*2+2*lmIndex] 				-= 1/measurementNoise
			omega[(1+numSteps)*2+2*lmIndex,2*i] 				-= 1/measurementNoise
			omega[(1+numSteps)*2+2*lmIndex,(1+numSteps)*2+2*lmIndex]	+= 1/measurementNoise

			xi   [2*i  ,		       0] 				-=lmX/measurementNoise
			xi   [(1+numSteps)*2+2*lmIndex  ,  0] 				+=lmX/measurementNoise

			omega[2*i+1,2*i+1]	  					+= 1/measurementNoise
			omega[2*i+1,(1+numSteps)*2+1+2*lmIndex] 			-= 1/measurementNoise
			omega[(1+numSteps)*2+1+2*lmIndex,2*i+1] 			-= 1/measurementNoise
			omega[(1+numSteps)*2+1+2*lmIndex,(1+numSteps)*2+1+2*lmIndex]    += 1/measurementNoise

			xi   [2*i+1,0] 							-=lmY/measurementNoise
			xi   [(1+numSteps)*2+1+2*lmIndex  ,   0]			+=lmY/measurementNoise

    	for i in range(numSteps):
		omega[2*i,2*i] 			+= 1/motionNoise
		omega[2*i,2*i+2] 		-= 1/motionNoise
		omega[2*i+2,2*i] 		-= 1/motionNoise
		omega[2*i+2,2*i+2] 		+= 1/motionNoise

		motion=data[i][1]
		print motion
		xi   [2*i  ,  0] 		-= motion[0]/motionNoise
		xi   [2*i+2,  0] 		+= motion[0]/motionNoise

		omega[2*i+1,2*i+1] 		+= 1/motionNoise
		omega[2*i+1,2*i+3] 		-= 1/motionNoise
		omega[2*i+3,2*i+1] 		-= 1/motionNoise
		omega[2*i+3,2*i+3] 		+= 1/motionNoise

		xi   [2*i+1,  0]   	        -= motion[1]/motionNoise
		xi   [2*i+3,  0] 		+= motion[1]/motionNoise

		measure			=data[i][0]
		
		k=i+1
		print 'k=', k
		for j in range (len(measure)):
			
			Z      =measure[j]

			lmIndex=Z[0]
			lmX    =Z[1]
			lmY    =Z[2]
			print 'lmindex', lmIndex
			omega[2*k,2*k] 			  				+= 1/measurementNoise
			omega[2*k,(1+numSteps)*2+2*lmIndex] 				-= 1/measurementNoise
			omega[(1+numSteps)*2+2*lmIndex,2*k] 				-= 1/measurementNoise
			omega[(1+numSteps)*2+2*lmIndex,(1+numSteps)*2+2*lmIndex]	+= 1/measurementNoise

			xi   [2*k,0] 			    				-=lmX/measurementNoise
			xi   [(1+numSteps)*2+2*lmIndex,0]   				+=lmX/measurementNoise

			omega[2*k+1,2*k+1]	  	   				+= 1/measurementNoise
			omega[2*k+1,(1+numSteps)*2+1+2*lmIndex]				-= 1/measurementNoise
			omega[(1+numSteps)*2+1+2*lmIndex,2*k+1]				-= 1/measurementNoise
			omega[(1+numSteps)*2+1+2*lmIndex,(1+numSteps)*2+1+2*lmIndex]    += 1/measurementNoise

			xi   [2*k+1,0] 							-=lmY/measurementNoise
			xi   [(1+numSteps)*2+1+2*lmIndex,0]				+=lmY/measurementNoise
	for element in data: 
		print element
	print 'len(data)', len(data)	
	print np.diag(omega)
    	mu = omega.getI() * xi
    	return mu

numLandmarks       = 28        # number of landmarks
numSteps           = 19        # time steps
motionNoise        = 1        # noise in robot motion
measurementNoise   = 1        # noise in the measurements
numOfPositions	   = 20
Z=[]*numOfPositions
for i in range (numOfPositions):
	lmAtPosition=[]
	f=open('/home/kuri/catkin_ws/src/graph_slam/IOfiles/landmarks.txt','r')
	for line in f: 
		elements=line.split()
		if(int(elements[0])==i):
			lmAtPosition.append([int(elements[1]), float(elements[2]), float(elements[3])])
	Z.append(lmAtPosition)

print 'Z', Z
#transitions=[[-20,0],[-20,0],[-20,0],[-20,0],[0,5],[20,0],[20,0],[20,0],[20,0],[0,5],[-20,0],[-20,0],[-20,0],[-20,0],[0,5],[20,0],[20,0],[20,0],[20,0], [0,5], [-20,0],[-20,0],[-20,0],[-20,0],[0,5],[20,0],[20,0],[20,0],[20,0],[0,5],[-20,0],[-20,0],[-20,0],[-20,0],[0,5],[20,0],[20,0],[20,0],[20,0], [0,5], [-20,0],[-20,0],[-20,0],[-20,0],[0,5],[20,0],[20,0],[20,0],[20,0],[0,5],[-20,0],[-20,0],[-20,0],[-20,0],[0,5],[20,0],[20,0],[20,0],[20,0]]


transitions=[[-20,0],[-20,0],[-20,0],[-20,0],[0,15],[20,0],[20,0],[20,0],[20,0],[0,15],[-20,0],[-20,0],[-20,0],[-20,0],[0,15],[20,0],[20,0],[20,0],[20,0]]
data=[]
for i in range(numOfPositions-1):
	data.append([Z[i+1], transitions[i]])
initialPosObservations=Z[0]
print 'len(data)', len(data)

result = SLAM(data, initialPosObservations, numSteps, numLandmarks, motionNoise, measurementNoise)

displayResults(numSteps, numLandmarks, result)

