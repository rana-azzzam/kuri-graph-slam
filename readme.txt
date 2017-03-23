The scripts/ folders includes five python files: 
1-survey-area.py: saves aerial images of the arena into the images/ folder

2-analyze-aerial-images.py: reads images from the images/ folder and saves analysis of them into the file analysis.txt. This file consists of 6 columns: "image_ID	landmark_color	landmark_surface_area	landmark_x_position	landmark_y_position	landmark_shape" 

3-identify-landmarks.py: assigns IDs to landmarks and calculates the distance between the drone and the each landmark. The file analysis.txt is used as an input to this script. The output is saved into the file landmarks.txt which consists of four columns: "image_ID	landmark_ID	x_distance	y_distance"

4-graph-slam.py: reads landmarks.txt, performs graph SLAM and saves the estimated poses of the drone into the file estimated_poses.txt

5-construct-slam-map.py: reads estimated_poses.txt and constructs the map of the arena using the aerial images in the images/ folder
