import * as THREE from 'three';
import React, {useMemo, useRef, useState, Suspense} from 'react';
import { Canvas, useLoader, useFrame } from '@react-three/fiber';
import { useTexture, OrbitControls } from "@react-three/drei";

import {StartButton, ResetButton, ShuffleButton} from './buttons';
import Text from './text';
import Square from './square';

var currentGame;
var currentStepNumber = 0;
var nextTargetSquare;
var nextMove;

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

const nextNumberToMove = (currentGame, nextSquare) => {
  let nextMove;
  for (let i = 0; i < currentGame.length; i++) {
    if (currentGame[i][0] === nextSquare[0] && currentGame[i][1] === nextSquare[1]) {
      const deltaX = currentGame[0][1] - nextSquare[1];
      const deltaY = currentGame[0][0] - nextSquare[0];
      let direction;
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
      // console.log(nextMove)
      return nextMove; // 1:top, 2:right, 3:down, 4:left
    }
  };
}

const swapSquare = (currentGame, numberToMove) => {
  let updatedGame = currentGame.slice();
  updatedGame[0] = currentGame[numberToMove];
  updatedGame[numberToMove] = currentGame[0];
  return updatedGame;
}

const addStep = () => {
  currentStepNumber += 1;
}

const App = (props) => {

  const problem = props.problem
  const solution = props.solution
  const [start, setStart] = useState(false)
  const [isGoal, setIsGoal] = useState(false)
  const [squareMoved, setSquareMoved] = useState(false);
  const [currentPositions, setCurrentPositions] = useState(coordinateToPosition(problem))

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

  if(currentStepNumber === 0) {
    currentGame = props.problem;
    nextTargetSquare = props.solution[1];
    nextMove = nextNumberToMove(currentGame, nextTargetSquare);
    // setCurrentPositions(coordinateToPosition(currentGame))
  }


  if (squareMoved && start) {
    addStep();
    setSquareMoved(false)

    currentGame = swapSquare(currentGame, nextMove[0]);
    setCurrentPositions(coordinateToPosition(currentGame))

    if (!isGoal && currentStepNumber < props.solution.length - 1) {
      nextTargetSquare = props.solution[currentStepNumber+1]
      nextMove = nextNumberToMove(currentGame, nextTargetSquare)
    } else if (currentStepNumber === props.solution.length - 1 && !isGoal) {
        setIsGoal(true)
    }
  }

  // currentPositions = coordinateToPosition(currentGame);

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
