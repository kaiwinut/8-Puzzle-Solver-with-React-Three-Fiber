import React, {useRef, useState, useEffec} from 'react';
import { useTexture } from "@react-three/drei";

const StartButton = (props) => {
  const textureStart = useTexture('images/start.png')
  const texturePause = useTexture('images/pause.png')
  const textureGoal = useTexture('images/goal.png')
  let texture;
  if (props.isGoal) {
    texture = textureGoal;
  } else if (props.start) {
    texture = texturePause;
  } else {
    texture = textureStart;
  }
  const [hovered, setHover] = useState(false);
  return (
    <mesh position={[3, 0.5, 0]}
        scale={hovered ? 1.1 : 1}
        onClick={() => props.setStart(!props.start)}
        onPointerOver={(e) => setHover(true)}
        onPointerOut={(e) => setHover(false)}
    >
      <boxGeometry attach="geometry" args={[1, 0.5, 0.5]}/>
      <meshStandardMaterial attachArray="material" color={hovered ? 0xb1b1b1:0xf1f1f1} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xb1b1b1:0xf1f1f1} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xb1b1b1:0xf1f1f1} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xb1b1b1:0xf1f1f1} />
      <meshStandardMaterial attachArray="material" map={texture} color={hovered ? 0xb1b1b1:0xf1f1f1} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xb1b1b1:0xf1f1f1} />
    </mesh>
  );
}

const ResetButton = (props) => {
  const texture = useTexture('images/reset.png')
  const [hovered, setHover] = useState(false);
  return (
    <mesh position={[3, -0.5, 0]}
        scale={hovered ? 1.1 : 1}
        onClick={props.reset}
        onPointerOver={(e) => setHover(true)}
        onPointerOut={(e) => setHover(false)}
    >
      <boxGeometry attach="geometry" args={[1, 0.5, 0.5]}/>
      <meshStandardMaterial attachArray="material" color={hovered ? 0xb1b1b1:0xf1f1f1} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xb1b1b1:0xf1f1f1} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xb1b1b1:0xf1f1f1} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xb1b1b1:0xf1f1f1} />
      <meshStandardMaterial attachArray="material" map={texture} color={hovered ? 0xb1b1b1:0xf1f1f1} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xb1b1b1:0xf1f1f1} />
    </mesh>
  );
}

export {
  StartButton,
  ResetButton
}
