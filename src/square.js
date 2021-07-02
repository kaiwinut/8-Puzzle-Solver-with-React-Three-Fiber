import React, {useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { useTexture } from "@react-three/drei";

const Square = (props) => {
  const speed = 0.03;
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
      <meshStandardMaterial attachArray="material" color={0xfcdec0}/>
      <meshStandardMaterial attachArray="material" color={0xfcdec0}/>
      <meshStandardMaterial attachArray="material" color={0xfcdec0}/>
      <meshStandardMaterial attachArray="material" color={0xfcdec0}/>
      <meshStandardMaterial attachArray="material" map={texture} color={0xfcdec0}/>
      <meshStandardMaterial attachArray="material" color={0xfcdec0}/>
    </mesh>
  );
}

export default Square
