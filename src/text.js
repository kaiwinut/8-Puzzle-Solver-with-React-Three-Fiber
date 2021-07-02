import * as THREE from 'three';
import React, {useMemo} from 'react';
import { Canvas, useLoader } from '@react-three/fiber';

const Text = (props) => {

  const font = useLoader(THREE.FontLoader, 'fonts/stencil.json')
  const config = useMemo(
    () => ({
      font,
      size: 0.6,
      height: 0.1,
      curveSegments: 2,
      weight: 'bold',
    }),
    [font]
  )
  return (
      <mesh position={props.position}>
        <textGeometry attach="geometry" args={[props.string, config]} />
        <meshPhongMaterial attach="material" color={0xb4846c} />
      </mesh>
  );
}

export default Text
