import numpy as np
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
from puzzleDetect import *
from cam import *
from treeSearch import *
from mlModel import Model
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--camera", action="store_true", help="read puzzle from camera")
parser.add_argument("--random", action="store_true", help="generate random puzzles")
args = parser.parse_args()

if args.camera and not(args.random) :
	print("Turn on camera mode...")
	puzzle = get_puzzle_info()
elif args.random and not(args.camera):
	print("Turn on random mode...")
	puzzle = None
else:
	raise Exception('Choose one and only one option: --camera or --random!')

puzzle, solution = A_search(Puzzle(8), puzzle)

def tuple_to_2darray(arr):
	newArray = []
	for element in arr:
		x, y = element
		newArray.append([x, y])
	return newArray

puzzleArr = tuple_to_2darray(puzzle)
solutionArr = tuple_to_2darray(solution)

PATH = 'puzzle.txt'
s = str(puzzleArr) + '\n' + str(solutionArr)

with open(PATH, mode='w') as f:
	f.write(s)

# not recommened but works
os.system('python3 server.py')
