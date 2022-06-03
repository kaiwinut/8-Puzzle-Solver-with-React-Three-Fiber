# 8-Puzzle-Solver with React-Three-Fiber

<img src="https://github.com/kaiwinut/8-Puzzle-Solver-with-React-Three-Fiberblob/main/demo.gif" width="500" alt="demo" />

## How to run the code
Run the 'main.py' file in the backend folder with Python3. Add --camera option after 'python3 main.py' to run in camera (or webcam) mode. For testing purpose, add --random option to generate random puzzles without the need to turn the camera on. If no options or both options are specified, an exception will be raised.

### Read 8-puzzle images using openCV
Capture frame that contains a 8-puzzle and extract the puzzle from it. 

### Recognize numbers in the puzzle using machine learning
Used mnist dataset to train a model that recognizes hand-written numbers. Apply model to recognize numbers in the extracted puzzle.

### Run A* search to find solution of puzzle
Heuristics used: current search depth and the sum of manhattan distance compared to goal state
Results (puzzle and solution) are exported to the file 'puzzle.txt'.

### Run local server with flask
Read from 'puzzle.txt' and return values when responding to localhost:5000/getPuzzle port. When shuffle button is pressed, post to localhost:5000/generatePuzzle port and request response, which will be a randomly generated 8-puzzle in this case.

### Visualize solution with react-three-fiber
Show solution of puzzle. 
Features: Start button, pause button, reset button, shuffle button, Steps countdown
Start button / Pause button: Start visulaization / Pause visualization
Reset button: Available when visualization is completed
Shuffle button: Generate random 8-puzzle
