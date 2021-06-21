from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import numpy as np
from mlModel import Model

class puzzleDetect:
	def __init__(self):
		# Number dictionary
		self.NUM_DICT = {
			# top, top-left, top-right, center, bottom-left, bottom-right, bottom
			(1, 0, 1, 1, 1, 0, 1): 2,
			(1, 0, 1, 1, 0, 1, 1): 3,
			(0, 1, 1, 1, 0, 1, 0): 4,
			(1, 1, 0, 1, 0, 1, 1): 5,
			(1, 1, 0, 1, 1, 1, 1): 6,
			(1, 0, 1, 0, 0, 1, 0): 7,
			(1, 1, 1, 1, 1, 1, 1): 8,	
		}
		self.img = None
		self.gray = None
		self.edged = None
		self.puzzleCnt = None
		self.warped = None
		self.thresh = None
		self.model = Model()

	def read_puzzle(self, img):
		# Read Image
		# img = cv2.imread(img_src)
		self.img = img
		### original puzzle image size can't be too small ###
		### Maybe need check image size ###
		self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
		# Blur image and detect edges
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
			if len(approx) == 4 and (arc >= 800 and arc <= 1200):
				self.puzzleCnt = approx
				break
		# threshold the warped image
		# cv2.imshow('edged',self.edged)
		# Return puzzle contour
		(x, y, w, h) = cv2.boundingRect(self.puzzleCnt)
		if (w > 200 and w < 300) and (h > 200 and h < 300) and np.abs(w-h) < 30 and x > 100 and x < 200:
			# print(x, y, w, h)
			return self.puzzleCnt
		else:
			return None

	def highlight_puzzle(self):
		# Check if successfully found puzzle contour by uncommenting this
		text = '8Puzzle!'
		img = cv2.drawContours(self.img, [self.puzzleCnt], -1, (0,0,255), 3)
		if type(self.puzzleCnt) is np.ndarray:
			(x, y, w, h) = cv2.boundingRect(self.puzzleCnt)
			cv2.putText(img, text, (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
		return img

	def recognize_puzzle(self):
		numBoxCnt = self.extract_puzzle(self.puzzleCnt)
		numBoxRecog = self.puzzle_to_dict(numBoxCnt)
		if numBoxRecog == None:
			return None, None
		puzzle_img = self.recognized_img(numBoxCnt, numBoxRecog)
		tree_search = self.convert_puzzle_to_array(numBoxRecog)
		if self.is_solvable(numBoxRecog, tree_search) == False:
			return None, None
		else:
			# print("puzzle dict:",numBoxRecog)
			return puzzle_img, tree_search

	# Execute extract_puzzle after finding puzzle contour
	def extract_puzzle(self, puzzleCnt):
		# Extract puzzle from image
		self.warped = four_point_transform(self.gray, puzzleCnt.reshape(4,2))
		# threshold the warped image
		thresh = cv2.threshold(self.warped, 0, 255, cv2.THRESH_OTSU)[1]
		thresh = cv2.threshold(thresh, 0, 255, cv2.THRESH_BINARY_INV)[1]
		# clean threshold image with morphological operations
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
		self.thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
		# Find contours again, for numbers 
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		numBoxCnt = []
		# Loop over contours to find contours of boxes that contains a number
		for c in cnts:
			# x, y: position of upper-left corner, w: width, h: height
			(x, y, w, h) = cv2.boundingRect(c)
			# Need to modify numbers manually to find right size of numberss
			if w >= 50 and (h >= 50 and h <=100):
				numBoxCnt.append(c)
		# Uncomment this to check if number boxes are found in image
		test_img = cv2.cvtColor(self.thresh, cv2.COLOR_GRAY2BGR)
		for c in numBoxCnt:
			(x, y, w, h) = cv2.boundingRect(c)
			test_img = cv2.rectangle(test_img, (x,y), (x+w,y+h), (0,255,0), 2)
		# cv2.imshow('test', test_img)
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
		return numBoxCnt

	# Execute recognize numbers after extracting puzzle
	def puzzle_to_dict(self, numBoxCnt):
		numBoxRecog = {}
		# Loop over number boxes to extract numbers and recognize
		for i, con in enumerate(numBoxCnt):
			# Name(Position) of this box (tuple)
			box_name = (i//3, i%3)
			# print(box_name)
			# Approximate box shape to square
			arc = cv2.arcLength(con, True)
			approx = cv2.approxPolyDP(con, 0.115*arc, True)
			# Extract box and clean box
			if approx.size != 8:
				return None
			warped_box = four_point_transform(self.thresh, approx.reshape(4,2))
			kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
			warped_box = cv2.morphologyEx(warped_box, cv2.MORPH_OPEN, kernel)
			# Find all contours in box
			cnts = cv2.findContours(warped_box.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
			cnts = imutils.grab_contours(cnts)
			# Loop over contours to find contours of numbers
			c = self.number_contour(box_name,cnts,numBoxRecog)
			# If no contour, enter next loop
			if type(c) is dict:
				continue
			else:
				numBoxRecog = self.recognize_number(box_name, c, warped_box, numBoxRecog)
		return numBoxRecog

	def number_contour(self, box_name, cnts, numBoxRecog):
		if numBoxRecog == None:
			return None
		for c in cnts:
			# x, y: position of upper-left corner, w: width, h: height
			(x, y, w, h) = cv2.boundingRect(c)
			# Need to modify numbers manually to find right size of numberss
			if w >= 10 and (h >= 30 and h <=65): # Check if this is a contour of a number
				return c
		# If no contours of number is found, number is zero
		numBoxRecog[box_name] = 0
		return numBoxRecog

	def recognize_number(self, box_name, c, img, numBoxRecog):
		if numBoxRecog == None or not(type(img) is np.ndarray):
			return None
		# print(img.shape)
		hwin, wwin = img.shape
		(x, y, w, h) = cv2.boundingRect(c)
		test_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
		cv2.rectangle(test_img, (x,y), (x+w,y+h), (0,0,255), 2)
		# cv2.imshow('before resize',test_img)
		# cv2.waitKey(0)
		delta_h = (wwin - x - w) - x
		delta_v = (hwin - y - h) - y
		# print("Delta h:",delta_h)
		# print("Wwin: ",wwin)
		if delta_h >= 0:
			img = img[0:hwin, 0:wwin-delta_h]
		else:
			img = img[0:hwin, -delta_h:wwin]
		hwin, wwin = img.shape
		# print("Wwin:", wwin)
		# print("Delta v:",delta_v)
		# print("Hwin: ",hwin)
		if delta_v >= 0:
			img = img[0:hwin-delta_v, 0:wwin]
		else:
			img = img[-delta_v:hwin, 0:wwin]
		hwin, wwin = img.shape
		# print("Wwin:", wwin)
		# print("Delta v:",delta_v)
		# print("Hwin: ",hwin)
		# cv2.imshow('trimmed',img)
		# cv2.waitKey(0)
		img = cv2.resize(img, (28,28), cv2.INTER_CUBIC)
		# cv2.imshow('resize',img)
		# print(img.size)
		# cv2.waitKey(0)
		number = self.model.predict_number(img)
		numBoxRecog[box_name] = number
		# print(numBoxRecog)
		return numBoxRecog

	# Uncomment this to check boxes and numbers
	def recognized_img(self, numBoxCnt, numBoxRecog):
		test_img = cv2.cvtColor(self.warped, cv2.COLOR_GRAY2BGR)
		for i, c in enumerate(numBoxCnt):
			xt, yt = i//3, i%3
			text = str((xt,yt)) + ':' + str(numBoxRecog[(xt,yt)])
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(test_img, (x,y), (x+w,y+h), (0,0,255), 2)
			cv2.putText(test_img, text, (x+5, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
		return test_img

	def convert_puzzle_to_array(self, puzzle_dict):
		tree_search = []
		sorted_dict = dict(sorted(puzzle_dict.items(), key=lambda x: x[1]))
		for square in sorted_dict:
			tree_search.append(square)
		return tree_search

	def is_solvable(self, numBoxRecog, tree_search):
		if len(tree_search) != 9:
			# print("Not solvable!")
			return False
		counter = [1] * 9
		for key in numBoxRecog:
			if numBoxRecog[key] == 9:
				return False
			counter[numBoxRecog[key]] -= 1
		for value in counter:
			if value != 0:
				# print("Not solvable!")
				return False
		return True

if __name__ == '__main__':
	detect = puzzleDetect()
	img = cv2.imread('archive/0_puzzle3.jpg')
	detect.read_puzzle(img)
	frame = detect.highlight_puzzle()
	cv2.imshow('highlighted_original_img', frame)
	puzzle_img, tree_search = detect.recognize_puzzle()
	cv2.imshow('puzzle_img', puzzle_img)
	print("List for tree search:",tree_search)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
