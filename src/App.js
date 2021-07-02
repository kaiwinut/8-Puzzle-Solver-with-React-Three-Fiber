import * as THREE from 'three';
import React, {useMemo, useRef, useState, Suspense} from 'react';
import { Canvas, useLoader, useFrame } from '@react-three/fiber';
import { useTexture, OrbitControls } from "@react-three/drei";

import {StartButton, ResetButton, ShuffleButton} from './buttons';
import Text from './text';
import Square from './square';

// Global variables
var currentGame; // Current ame state
var currentStepNumber = 0; // Current step number
var nextTargetSquare; // Next target square of blank square
var nextMove; // Moving number and direction

// Coordinates to 3D position
const coordinateToPosition = (coordinates) => {
  let positions = Array(9);
  coordinates.forEach((element, i) => {
    const x = element[1] - 1;
    const y = element[0] - 1;
    const position = [1.3*x, -1.3*y, 0];
    positions[i] = position
  });
  return positions;
}

// Get next number to move from current game state
// and the next target square of blank square
const nextNumberToMove = (currentGame, nextSquare) => {
  let nextMove;
  for (let i = 0; i < currentGame.length; i++) {
    if (currentGame[i][0] === nextSquare[0] && currentGame[i][1] === nextSquare[1]) {
      // Calculate the difference between current square and target square
      const deltaX = currentGame[0][1] - nextSquare[1];
      const deltaY = currentGame[0][0] - nextSquare[0];
      let direction; // 1:top, 2:right, 3:down, 4:left
      switch (deltaX) {
        case -1:
          direction = 4;
          break;
        case 1:
          direction = 2;
          break;
        case 0:
          direction = (deltaY+1) ? 3 : 1;
          break;
        default:
          return[null, null];
      }
      nextMove = [i, direction];
      return nextMove;
    }
  };
}

// After square moved, swap positions of numbers in current game state
const swapSquare = (currentGame, numberToMove) => {
  let updatedGame = currentGame.slice();
  updatedGame[0] = currentGame[numberToMove];
  updatedGame[numberToMove] = currentGame[0];
  return updatedGame;
}

// Current step number plus 1
const addStep = () => {
  currentStepNumber += 1;
}

// Main rendering loop
const App = (props) => {

  // Initialize variables
  const problem = props.problem
  const solution = props.solution
  const [start, setStart] = useState(false)
  const [isGoal, setIsGoal] = useState(false)
  const [squareMoved, setSquareMoved] = useState(false);
  const [currentPositions, setCurrentPositions] = useState(coordinateToPosition(problem))

  // Reset puzzle when reset button is clicked
  const reset = () => {
    if(isGoal || (!start && currentStepNumber===0)) {
      setStart(false)
      setIsGoal(false)
      setSquareMoved(false)
      currentStepNumber = 0;
      currentGame = props.problem;
      nextTargetSquare = props.solution[1];
      nextMove = nextNumberToMove(currentGame, nextTargetSquare)
      setCurrentPositions(coordinateToPosition(currentGame))
    }
  }

  // Generate new puzzle and reset puzzle when shuffle button is clicked
  const generateAndReset = () => {
    if (isGoal || !start) {
      props.generate()
      setStart(false)
      setIsGoal(false)
      setSquareMoved(false)
      currentStepNumber = 0;
      currentGame = props.problem;
      nextTargetSquare = props.solution[1];
      nextMove = nextNumberToMove(currentGame, nextTargetSquare)
      setCurrentPositions(coordinateToPosition(currentGame))
    }
  }

  // Initialize currentGame, nextTargetSquare, nextMove
  if(currentStepNumber === 0) {
    currentGame = props.problem;
    nextTargetSquare = props.solution[1];
    nextMove = nextNumberToMove(currentGame, nextTargetSquare);
  }

  // After number is moved
  if (squareMoved && start) {
    // Add step number and set squareMoved state to false
    addStep();
    setSquareMoved(false)
    // Update current game and current positions
    currentGame = swapSquare(currentGame, nextMove[0]);
    setCurrentPositions(coordinateToPosition(currentGame))
    // while game is not over, update next target square and next move
    if (!isGoal && currentStepNumber < props.solution.length - 1) {
      nextTargetSquare = props.solution[currentStepNumber+1]
      nextMove = nextNumberToMove(currentGame, nextTargetSquare)
    } else if (currentStepNumber === props.solution.length - 1 && !isGoal) {
      // If game is over, set goal state to true
        setIsGoal(true)
    }
  }

  return (
    <div className='container'>
      <Canvas className="canvas" camera={{position: [0, 0, 7], fov: 60}}>
        <Suspense fallback={null}>
          <OrbitControls />
          <ambientLight intensity={0.1} />
          <directionalLight color="gray" position={[0, 0, 5]} />
          <Text position={[-1.7, 2.5, 0]} string={"8-Puzzle!"} />
          <Text position={[-4.5, 1.1, 0]} string={"Steps\nLeft:\n" + (props.solution.length - currentStepNumber - 1)} />
          <StartButton setStart={setStart} start={start} isGoal={isGoal}/>
          <ResetButton reset={reset} />
          <ShuffleButton generateAndReset={generateAndReset} reset={reset}/>
          {
            currentPositions.map((position, i) => {
              // Only render numbers moving
              if (i === nextMove[0] && (currentStepNumber < props.solution.length - 1) && start) {
                return (
                  <Square position={position}
                          direction={nextMove[1]}
                          setSqmoved={setSquareMoved}
                          number={i}/>
                );
              } else if (i !== 0) {
                return (
                  <Square position={position}
                          direction={null}
                          number={i}/>
                );
              }
            })
          }
        </Suspense>
      </Canvas>
    </div>
  )
}

export default App
