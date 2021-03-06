from flask import Flask
from flask import request, make_response, jsonify
from flask_cors import CORS
from treeSearch import *
import ast

# For generatePuzzle()
def tuple_to_2darray(arr):
    newArray = []
    for element in arr:
        x, y = element
        newArray.append([x, y])
    return newArray

app = Flask(__name__, static_folder="./build/static", template_folder="./build")
CORS(app) #Cross Origin Resource Sharing

# Read puzzle from local file
file = './puzzle.txt'
with open(file) as f:
    s = f.readlines()
    puzzle = ast.literal_eval(s[0].strip())
    solution = ast.literal_eval(s[1])

# Used when reading puzzle from camera
@app.route("/getPuzzle", methods=['POST'])
def getPuzzle():
    data = request.get_json()
    text = data['post_text']
    if text == 'ready!':
        response = {'puzzle': puzzle, 'solution': solution}
    return make_response(jsonify(response))

# Used when shuffle button is clicked
# This generates a random puzzle
@app.route("/generatePuzzle", methods=['POST'])
def generatePuzzle():
    data = request.get_json()
    text = data['post_text']
    if text == 'ready!':
        puzzle, solution = A_search(Puzzle(8), None)
        puzzleArr = tuple_to_2darray(puzzle)
        solutionArr = tuple_to_2darray(solution)
        response = {'puzzle': puzzleArr, 'solution': solutionArr}
    return make_response(jsonify(response))

if __name__ == "__main__":
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
