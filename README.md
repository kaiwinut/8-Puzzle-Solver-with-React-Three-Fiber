# 8-Puzzle-Solver with React-Three-Fiber

## Read 8-puzzle images using openCV
Capture frame that contains a 8-puzzle and extract the puzzle from it

## Recognize numbers in the puzzle using machine learning
Used mnist dataset to train a model that recognizes hand-written numbers. Apply model to recognize numbers in the extracted puzzle.

## Run A* search to find solution of puzzle
Heuristics used: current search depth + sum of manhattan distance compared to goal state.
Export results (puzzle and solution) to the file 'puzzle.txt'.

## Run local server with flask
Read from 'puzzle.txt' and return values when responding.

## Visualize solution with react-three-fiber
Show solution of puzzle. 
Added features: Start button, pause button, reset button
