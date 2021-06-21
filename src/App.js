import React, {useRef, useState, useEffect, Suspense} from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { useTexture, OrbitControls } from "@react-three/drei";

import {StartButton, ResetButton} from './buttons';

// Initialize squares
// const init_squares = () => {
//   const squares = [...Array(9).keys()];
//   const sqcoor = squares.map((i) => {
//     const x = i % 3;
//     const y = Math.floor(i/3);
//     const coor = [y, x];
//     return coor;
//   });
//   return sqcoor;
// }

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

const Square = (props) => {
  const speed = 0.05;
  const texture = useTexture('images/' + props.number + '.png')
  const mesh = useRef()
  const [hovered, setHover] = useState(false)

  useFrame((state, delta) => {
    if (props.direction && Math.abs(mesh.current.position.x - props.position[0]) < 1.3 && Math.abs(mesh.current.position.y - props.position[1]) < 1.3) {
      switch (props.direction) {
        case 1:
          mesh.current.position.y += speed;
          break;
        case 2:
          mesh.current.position.x += speed;
          break;
        case 3:
          mesh.current.position.y -= speed;
          break;
        case 4:
          mesh.current.position.x -= speed;
          break;
        default:
          break;
      }
    } else if (props.direction) {
      props.setStep(props.step+1)
      props.setSqmoved(true)
    }
  })

  return (
    <mesh position={props.position}
          ref={mesh}
          scale={hovered ? 1.1 : 1}
          onPointerOver={(e) => setHover(true)}
          onPointerOut={(e) => setHover(false)}
    >
      <boxGeometry args={[1, 1, 0.5]}/>
      <meshStandardMaterial attachArray="material" />
      <meshStandardMaterial attachArray="material" />
      <meshStandardMaterial attachArray="material" />
      <meshStandardMaterial attachArray="material" />
      <meshStandardMaterial attachArray="material" map={texture} />
      <meshStandardMaterial attachArray="material" />
    </mesh>
  );
}

const App = (props) => {

  const [start, setStart] = useState(false)
  const [isGoal, setIsGoal] = useState(false)
  const [currentStepNumber, setCurrentStepNumber] = useState(0);
  const [squareMoved, setSquareMoved] = useState(false);
  const [nextTargetSquare, setNextTargetSquare] = useState(props.solution[1]);
  const [currentGame, setCurrentGame] = useState(props.problem);
  let nextMove = nextNumberToMove(currentGame, nextTargetSquare)

  const reset = () => {
    if(isGoal) {
      setStart(false)
      setIsGoal(false)
      setCurrentStepNumber(0)
      setSquareMoved(false)
      setNextTargetSquare(props.solution[1])
      setCurrentGame(props.problem)
      nextMove = nextNumberToMove(currentGame, nextTargetSquare)
    }
  }

  if (squareMoved && start) {
    setCurrentGame(swapSquare(currentGame, nextMove[0]))
    setSquareMoved(false)

    if (!isGoal && currentStepNumber < props.solution.length - 1) {
      setNextTargetSquare(props.solution[currentStepNumber+1])
      // console.log("next step");
    } else if (currentStepNumber === props.solution.length - 1 && !isGoal) {
        // console.log("goal");
        setIsGoal(true)
    }
  } else if (nextMove[0] === -1){
    nextMove = [null, null]
  }

  // For debugging
  // useEffect( () => {
  //   console.log("Current Game Status:");
  //   console.log(currentGame);
  //   console.log("Current step number: " + currentStepNumber);
  //   console.log("Is game over? " + isGoal);
  //   console.log("Is game started? " + start);
  //   console.log("Did square finish moving? " + squareMoved);
  //   console.log("Next Move: " + nextMove);
  //   console.log("Next target square for zero: " + nextTargetSquare);
  // });

  const currentPositions = coordinateToPosition(currentGame);

  return (
    <div className='container'>
      <Canvas className="canvas" camera={{position: [0, 0, 7], fov: 60}}>
        <Suspense fallback={null}>
          <OrbitControls />
          <ambientLight intensity={0.1} />
          <directionalLight color="gray" position={[0, 0, 5]} />

          <StartButton setStart={setStart} start={start} isGoal={isGoal}/>
          <ResetButton reset={reset}/>

          {
            currentPositions.map((position, i) => {
              if (i === nextMove[0] && nextMove[1] && (currentStepNumber < props.solution.length - 1) && start) {
                return (
                  <Square position={position}
                          direction={nextMove[1]}
                          step={currentStepNumber}
                          setStep={setCurrentStepNumber}
                          sqmoved={squareMoved}
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
