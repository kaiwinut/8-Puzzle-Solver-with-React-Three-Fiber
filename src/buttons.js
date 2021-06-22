import React, {useState} from 'react';
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
    <mesh position={[3, 1, 0]}
        scale={hovered ? 1.1 : 1}
        onClick={() => props.setStart(!props.start)}
        onPointerOver={(e) => setHover(true)}
        onPointerOut={(e) => setHover(false)}
    >
      <boxGeometry attach="geometry" args={[1, 0.5, 0.5]}/>
      <meshStandardMaterial attachArray="material" color={hovered ? 0xfcdec0:0xe5b299} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xfcdec0:0xe5b299} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xfcdec0:0xe5b299} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xfcdec0:0xe5b299} />
      <meshStandardMaterial attachArray="material" map={texture} color={hovered ? 0xfcdec0:0xe5b299} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xfcdec0:0xe5b299} />
    </mesh>
  );
}

const ResetButton = (props) => {
  const texture = useTexture('images/reset.png')
  const [hovered, setHover] = useState(false);
  return (
    <mesh position={[3, 0, 0]}
        scale={hovered ? 1.1 : 1}
        onClick={props.reset}
        onPointerOver={(e) => setHover(true)}
        onPointerOut={(e) => setHover(false)}
    >
      <boxGeometry attach="geometry" args={[1, 0.5, 0.5]}/>
      <meshStandardMaterial attachArray="material" color={hovered ? 0xfcdec0:0xe5b299} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xfcdec0:0xe5b299} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xfcdec0:0xe5b299} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xfcdec0:0xe5b299} />
      <meshStandardMaterial attachArray="material" map={texture} color={hovered ? 0xfcdec0:0xe5b299} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xfcdec0:0xe5b299} />
    </mesh>
  );
}

const ShuffleButton = (props) => {
  const texture = useTexture('images/shuffle.png')
  const [hovered, setHover] = useState(false);
  const [activate, setActivate] = useState(false);
  const shuffle = () => {
    props.generateAndReset();
    setActivate(true)
  }
  const resetBoard = () => {
    if (activate) {
      props.reset()
      setActivate(false)
    }
  }

  return (
    <mesh position={[3, -1, 0]}
        scale={hovered ? 1.1 : 1}
        onClick={shuffle}
        onPointerMove={resetBoard}
        onPointerOver={(e) => setHover(true)}
        onPointerOut={(e) => setHover(false)}
    >
      <boxGeometry attach="geometry" args={[1, 0.5, 0.5]}/>
      <meshStandardMaterial attachArray="material" color={hovered ? 0xfcdec0:0xe5b299} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xfcdec0:0xe5b299} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xfcdec0:0xe5b299} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xfcdec0:0xe5b299} />
      <meshStandardMaterial attachArray="material" map={texture} color={hovered ? 0xfcdec0:0xe5b299} />
      <meshStandardMaterial attachArray="material" color={hovered ? 0xfcdec0:0xe5b299} />
    </mesh>
  );
}

export {
  StartButton,
  ResetButton,
  ShuffleButton
}
