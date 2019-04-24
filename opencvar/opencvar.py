import numpy as np
import argparse
import cv2
from matplotlib import pyplot as plt
from objloader_simple import *
import os
import math
from mtl import *
import pygame
from OpenGL.GL import *

# Minimum number of matches that have to be found
# to consider the recognition valid
MIN_MATCHES = 1400

def main():
	homography = None 
	# matrix of camera parameters (made up but works quite well for me) 
	camera_parameters = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]])
	#img1 = cv2.imread('/Users/kamlesh.panchal/Downloads/augmented-reality-master/reference/model.png')         
	# queryImage
	img2 = cv2.imread('/Users/kamlesh.panchal/Downloads/augmented-reality-master/reference/book.jpg',0)
	img2 = cv2.resize(img2, (900, 1000))
	# Initiate SIFT detector
	sift = cv2.xfeatures2d.SIFT_create()
    #Load 3d object
	obj = OBJ('/Users/kamlesh.panchal/Desktop/opencv/jet.obj', swapyz=False)  
	# Detect & compute keypoint of query image using sift method
	kp2, des2 = sift.detectAndCompute(img2,None)
	cap = cv2.VideoCapture(0)
	ret = cap.set(3,900)
	ret = cap.set(4,1000)
	
	while (1):
		# take first frame of the video
		ret,frame = cap.read()

		#convert video frame into grayscale color
		gray = cv2.cvtColor(frame, 0)

		# find the keypoints and descriptors with SIFT
		kp1, des1 = sift.detectAndCompute(frame,None)

		# FLANN parameters
		FLANN_INDEX_KDTREE = 0
		index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
		search_params = dict(checks=50)

		flann = cv2.FlannBasedMatcher(index_params,search_params)
		# compute feature matching
		matches = flann.knnMatch(des1,des2,k=2)
		# Sort by their distance.
		matches = sorted(matches, key = lambda x:x[0].distance)

		## (6) Ratio test, to get good matches.
		good = [m1 for (m1, m2) in matches if m1.distance < 0.7 * m2.distance]
		#canvas = img2.copy()

		print (len(matches))

		# check if feature matching of video frame is bigger than minimum feature matches

		if len(matches) > MIN_MATCHES:
			# differenciate between source points and destination points
			src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
			dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
			print ("method in")
			# compute Homography
			homography, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
			print (homography)
			'''
			if args.rectangle:
			    # Draw a rectangle that marks the found model in the frame
				h, w = img2.shape[:2]
				pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
				# project corners into frame
				dst = cv2.perspectiveTransform(pts, homography)
				# connect them with lines  
				gray = cv2.polylines(gray, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)  
				# if a valid homography matrix was found render model
			'''	
			if homography is not None:
			    try:
			        # obtain 3D projection matrix from homography matrix and camera parameters
			        projection = projection_matrix(camera_parameters, homography)  
			      
			        # project and render jet model
			        gray = render(gray, obj, projection, img2, True)
			        #frame = render(frame, model, projection)
			    except:
			        pass
			    # draw first 10 matches.
			#if args.matches:
				#gray = cv2.drawMatches(img2,kp2,gray,kp1,good[:10],None)#,**draw_params)
			cv2.imshow('keypoints',gray)
				#cv2.waitKey();
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		else:
			print ("Not enough matches found - %d/%d" % (len(matches), MIN_MATCHES))
			cv2.imshow('keypoints',gray)
				#cv2.waitKey();
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

	cap.release()  
	cv2.destroyAllWindows()
	return 0


def render(img, obj, projection, model, color=False):
    """
    Render a loaded obj model into the current video frame
    """
    vertices = obj.vertices
    scale_matrix = np.eye(3) * 3
    h, w = model.shape

    for face in obj.faces:
        face_vertices = face[0]
        points = np.array([vertices[vertex - 1] for vertex in face_vertices])
        points = np.dot(points, scale_matrix)
        # render model in the middle of the reference surface. To do so,
        # model points must be displaced
        points = np.array([[p[0] + w / 2, p[1] + h / 2, p[2]] for p in points])
        dst = cv2.perspectiveTransform(points.reshape(-1, 1, 3), projection)
        imgpts = np.int32(dst)
        if color is False:
            cv2.fillConvexPoly(img, imgpts, (137, 27, 211))
        else:
            color = hex_to_rgb(face[-1])
            color = color[::-1]  # reverse
            cv2.fillConvexPoly(img, imgpts, color)

    return img

def projection_matrix(camera_parameters, homography):
    """
    From the camera calibration matrix and the estimated homography
    compute the 3D projection matrix
    """
    # Compute rotation along the x and y axis as well as the translation
    homography = homography * (-1)
    rot_and_transl = np.dot(np.linalg.inv(camera_parameters), homography)
    col_1 = rot_and_transl[:, 0]
    col_2 = rot_and_transl[:, 1]
    col_3 = rot_and_transl[:, 2]
    # normalise vectors
    l = math.sqrt(np.linalg.norm(col_1, 2) * np.linalg.norm(col_2, 2))
    rot_1 = col_1 / l
    rot_2 = col_2 / l
    translation = col_3 / l
    # compute the orthonormal basis
    c = rot_1 + rot_2
    p = np.cross(rot_1, rot_2)
    d = np.cross(c, p)
    rot_1 = np.dot(c / np.linalg.norm(c, 2) + d / np.linalg.norm(d, 2), 1 / math.sqrt(2))
    rot_2 = np.dot(c / np.linalg.norm(c, 2) - d / np.linalg.norm(d, 2), 1 / math.sqrt(2))
    rot_3 = np.cross(rot_1, rot_2)
    # finally, compute the 3D projection matrix from the model to the current frame
    projection = np.stack((rot_1, rot_2, rot_3, translation)).T
    return np.dot(camera_parameters, projection)

def hex_to_rgb(hex_color):
    """
    Helper function to convert hex strings to RGB
    """
    hex_color = hex_color.lstrip('#')
    h_len = len(hex_color)
    return tuple(int(hex_color[i:i + h_len // 3], 16) for i in range(0, h_len, h_len // 3))

'''
# Command line argument parsing
# NOT ALL OF THEM ARE SUPPORTED YET

parser = argparse.ArgumentParser(description='Augmented reality application')

parser.add_argument('-r','--rectangle', help = 'draw rectangle delimiting target surface on frame', action = 'store_true')
parser.add_argument('-mk','--model_keypoints', help = 'draw model keypoints', action = 'store_true')
parser.add_argument('-fk','--frame_keypoints', help = 'draw frame keypoints', action = 'store_true')
parser.add_argument('-ma','--matches', help = 'draw matches between keypoints', action = 'store_true')

	# TODO jgallostraa -> add support for model specification
	#parser.add_argument('-mo','--model', help = 'Specify model to be projected', action = 'store_true')

args = parser.parse_args()
'''

if __name__ == '__main__':
    main()	

     