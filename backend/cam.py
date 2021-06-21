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
	detect = puzzleDetect()
	cap = cv2.VideoCapture(0)

	width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

	while cap.isOpened():
		# If found puzzle contour from camera view
		ret, frame = cap.read()
		if not(type(frame) is np.ndarray):
			continue
		frame = imutils.resize(frame, height=300)
		cnt = detect.read_puzzle(frame)
		if type(cnt) is np.ndarray:
			# print("Found puzzle!")
			# Return highlighted frame
			frame = detect.highlight_puzzle()
			cv2.imshow('frame',frame)
			puzzle_img, tree_search = detect.recognize_puzzle()
			if tree_search == None and puzzle_img == None:
				continue
			else:
				cv2.imshow('puzzle_img', puzzle_img)
				# print("List for tree search:",tree_search)
				cv2.waitKey(1000)
				cv2.destroyAllWindows()
				return tree_search

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break			

		cv2.imshow('frame',frame)
	return None
