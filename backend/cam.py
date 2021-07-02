from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import numpy as np
# Used when digits are handwritten
from puzzleDetectML import puzzleDetect
# Used when digits are in digital 7 segment format
# from puzzleDetect import puzzleDetect
from mlModel import Model

def get_puzzle_info():
	# Initialize puzzleDetect object
	detect = puzzleDetect()
	# Initialize webcam
	cap = cv2.VideoCapture(0)

	width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

	# While camera is on
	while cap.isOpened():
		# Read frame and resize it to height=300
		ret, frame = cap.read()
		if not(type(frame) is np.ndarray):
			continue
		frame = imutils.resize(frame, height=300)
		# If found puzzle contour from camera view
		cnt = detect.read_puzzle(frame)
		if type(cnt) is np.ndarray:
			# Return highlighted frame
			frame = detect.highlight_puzzle()
			cv2.imshow('frame',frame)
			puzzle_img, tree_search = detect.recognize_puzzle()
			# If something went wrong during puzzle recognition
			# Read frame again
			if tree_search == None and puzzle_img == None:
				continue
			else:
				cv2.imshow('puzzle_img', puzzle_img)
				# Wait for 1 sec and execute next step
				cv2.waitKey(1000)
				cv2.destroyAllWindows()
				return tree_search
		# Hit q to exit
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break			

		cv2.imshow('frame',frame)
	return None
