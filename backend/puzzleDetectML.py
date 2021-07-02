### puzzleDetectML.py is used to recognize handwritten puzzles
### To rezognize puzzles containing 7-segment numbers, use puzzleDetect.py

from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import numpy as np

# Trained neural network model used to recognize handwritten numbers.
from mlModel import Model

# puzzleDetect class contains functions that reads 8-puzzle
# from frame and functions that recognizes it
class puzzleDetect:
	def __init__(self):
		# Original frame
		self.img = None
		# Gray scaled frame
		self.gray = None
		# Edged frame using Canny
		self.edged = None
		# Contour of 8-puzzle
		self.puzzleCnt = None
		# 8-puzzle extracted from original frame
		self.warped = None
		# Threshold image of 8-puzzle
		self.thresh = None
		# Neural network model used to recognize handwritten numbers
		self.model = Model()

	# Read frame from camera
	# If frame contains 8-puzzle, return contour of puzzle. Else return None.
	def read_puzzle(self, img):
		# Store original frame in self.img
		self.img = img
		# Turn original frame to gray scale and store gray scaled image in self.gray
		self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
		# Blur image (robust to noise) and detect edges
		blurred = cv2.GaussianBlur(self.img, (3,3), 0)
		self.edged = cv2.Canny(blurred, 100, 200)
		# Find contours in edged image and sort them by size
		cnts = cv2.findContours(self.edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		cnts.sort(key=cv2.contourArea, reverse=True)
		# Loop over all contours and find the target puzzle
		for c in cnts:
			# acrLength: the length of contour surrounding area
			arc = cv2.arcLength(c, True)
			# approximate contour as polygon, the smaller the second argument, the more angles
			approx = cv2.approxPolyDP(c, 0.1*arc, True)
			# Larger contours are place at the front of the array (by sorting)
			# This assures that we find the puzzle before looping over any other contours
			if len(approx) == 4 and (arc >= 800 and arc <= 1200):
				self.puzzleCnt = approx
				break
		# Check if contour is actually the contour of puzzle
		# If yes, return puzzle contour
		(x, y, w, h) = cv2.boundingRect(self.puzzleCnt)
		# Puzzle contour should have at certain size and should be at the center of the frame
		if (w > 200 and w < 300) and (h > 200 and h < 300) and np.abs(w-h) < 30 and x > 100 and x < 200:
			return self.puzzleCnt
		else:
			return None

	# Show red box surrounding puzzle on original frame
	def highlight_puzzle(self):
		# Show text around highlight box
		text = '8Puzzle!'
		img = cv2.drawContours(self.img, [self.puzzleCnt], -1, (0,0,255), 3)
		if type(self.puzzleCnt) is np.ndarray:
			(x, y, w, h) = cv2.boundingRect(self.puzzleCnt)
			cv2.putText(img, text, (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
		return img

	# Main function used to recognize puzzle
	def recognize_puzzle(self):
		# Extract puzzle from gray scaled frame and 
		# return contours of smaller boxes containing numbers
		numBoxCnt = self.extract_puzzle(self.puzzleCnt)
		# Recognize numbers from smaller number boxes
		numBoxRecog = self.puzzle_to_dict(numBoxCnt)
		# If something went wrong during recognition, return None
		if numBoxRecog == None:
			return None, None
		# Puzzle image used to check if recognition is correct
		puzzle_img = self.recognized_img(numBoxCnt, numBoxRecog)
		# Puzzle array which will be passed to tree search function
		tree_search = self.convert_puzzle_to_array(numBoxRecog)
		# If recognized puzzle is not solvable, return None
		# Else return puzzle image and puzzle array
		if self.is_solvable(numBoxRecog, tree_search) == False:
			return None, None
		else:
			return puzzle_img, tree_search

	# Extract puzzle from original frame using puzzle contour
	# return contours of smaller boxes containing number
	def extract_puzzle(self, puzzleCnt):
		# Extract puzzle from image
		self.warped = four_point_transform(self.gray, puzzleCnt.reshape(4,2))
		# Threshold the warped image
		thresh = cv2.threshold(self.warped, 0, 255, cv2.THRESH_OTSU)[1]
		thresh = cv2.threshold(thresh, 0, 255, cv2.THRESH_BINARY_INV)[1]
		# Clean threshold image with morphological operations
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
		self.thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
		# Find contours again, for number boxes
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		numBoxCnt = []
		# Loop over contours to find contours of boxes that contains a number
		for c in cnts:
			# x, y: position of upper-left corner, w: width, h: height
			(x, y, w, h) = cv2.boundingRect(c)
			# Need to modify numbers manually to find right size of number boxes
			if w >= 50 and (h >= 50 and h <=100):
				numBoxCnt.append(c)
		
		# Uncomment this to check if number boxes are found in image
		# test_img = cv2.cvtColor(self.thresh, cv2.COLOR_GRAY2BGR)
		# for c in numBoxCnt:
		# 	(x, y, w, h) = cv2.boundingRect(c)
		# 	test_img = cv2.rectangle(test_img, (x,y), (x+w,y+h), (0,255,0), 2)
		# cv2.imshow('test', test_img)

		# Sort boxes from left to right, top to bottom
		def sort_box(box):
			(x,y,w,h) = cv2.boundingRect(box)
			if y < h/3:
				y = 0
			elif 2*h/3 < y and y < 4*h/3:
				y = 300
			else:
				y = 600
			return x + y
		numBoxCnt.sort(key=lambda box: sort_box(box))

		# Return contour of number boxes
		return numBoxCnt

	# Loop over number boxes, recognize numbers and return a 
	# dictionary that stores the position of each number
	def puzzle_to_dict(self, numBoxCnt):
		numBoxRecog = {}
		# Loop over number boxes to extract numbers and recognize
		for i, con in enumerate(numBoxCnt):
			# Name(Position) of this box (tuple)
			box_name = (i//3, i%3)
			# Approximate box shape to square, if box is not square, return None
			arc = cv2.arcLength(con, True)
			approx = cv2.approxPolyDP(con, 0.115*arc, True)
			if approx.size != 8:
				return None
			# Extract box and clean box
			warped_box = four_point_transform(self.thresh, approx.reshape(4,2))
			kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
			warped_box = cv2.morphologyEx(warped_box, cv2.MORPH_OPEN, kernel)
			# Find all contours in box
			cnts = cv2.findContours(warped_box.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
			cnts = imutils.grab_contours(cnts)
			# Loop over contours to find contours of numbers
			c = self.number_contour(box_name,cnts,numBoxRecog)
			# If no contour, number is 0
			# then enter next loop
			if type(c) is dict:
				continue
			else:
				# If there is a contour, recognize the number
				numBoxRecog = self.recognize_number(box_name, c, warped_box, numBoxRecog)
		return numBoxRecog

	# Check if contour is contour of nunber
	def number_contour(self, box_name, cnts, numBoxRecog):
		if numBoxRecog == None:
			return None
		for c in cnts:
			# x, y: position of upper-left corner, w: width, h: height
			(x, y, w, h) = cv2.boundingRect(c)
			# Need to modify numbers manually to find right size of numbers
			# Check if this is a contour of a number
			if w >= 10 and (h >= 30 and h <=65):
				return c
		# If no contours of number is found, number is zero
		numBoxRecog[box_name] = 0
		return numBoxRecog

	# Resize number image and recognize number
	def recognize_number(self, box_name, c, img, numBoxRecog):
		if numBoxRecog == None or not(type(img) is np.ndarray):
			return None
		# Center the number
		hwin, wwin = img.shape
		(x, y, w, h) = cv2.boundingRect(c)
		delta_h = (wwin - x - w) - x
		delta_v = (hwin - y - h) - y
		if delta_h >= 0:
			img = img[0:hwin, 0:wwin-delta_h]
		else:
			img = img[0:hwin, -delta_h:wwin]
		hwin, wwin = img.shape
		if delta_v >= 0:
			img = img[0:hwin-delta_v, 0:wwin]
		else:
			img = img[-delta_v:hwin, 0:wwin]
		hwin, wwin = img.shape
		# Resize image to apply neural network model
		img = cv2.resize(img, (28,28), cv2.INTER_CUBIC)
		# Predict number with neural network model 
		number = self.model.predict_number(img)
		numBoxRecog[box_name] = number
		# Return puzzle dictionary
		return numBoxRecog

	# Show results of recognition
	def recognized_img(self, numBoxCnt, numBoxRecog):
		test_img = cv2.cvtColor(self.warped, cv2.COLOR_GRAY2BGR)
		for i, c in enumerate(numBoxCnt):
			xt, yt = i//3, i%3
			# Name (Position) of box : the number inside
			text = str((xt,yt)) + ':' + str(numBoxRecog[(xt,yt)])
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(test_img, (x,y), (x+w,y+h), (0,0,255), 2)
			cv2.putText(test_img, text, (x+5, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
		return test_img

	# Convert puzzle dictionary to puzzle array
	# Index of puzzle array is the number, value is the position
	def convert_puzzle_to_array(self, puzzle_dict):
		tree_search = []
		sorted_dict = dict(sorted(puzzle_dict.items(), key=lambda x: x[1]))
		for square in sorted_dict:
			tree_search.append(square)
		return tree_search

	# Check if puzzle recognized is correct 
	def is_solvable(self, numBoxRecog, tree_search):
		# If puzzle array doesn't have a length of 9,
		# puzzle is incorrect
		if len(tree_search) != 9:
			return False
		counter = [1] * 9
		# If puzzle array doesn't contain numbers 1-8,
		# puzzle is incorrect
		for key in numBoxRecog:
			if numBoxRecog[key] == 9:
				return False
			counter[numBoxRecog[key]] -= 1
		for value in counter:
			if value != 0:
				return False
		# Else puzzle is correct
		return True
