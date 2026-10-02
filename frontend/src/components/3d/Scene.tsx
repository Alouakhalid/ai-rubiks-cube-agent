import React, { Suspense } from "react"
import { Canvas } from "@react-three/fiber"
import { RubiksCube } from "./RubiksCube"
import { Controls } from "./Controls"

export const Scene: React.FC = () => {
  return (
    <div className="w-full h-full relative cursor-grab active:cursor-grabbing">
      <Canvas
        camera={{ position: [4.5, 4.5, 5.5], fov: 45 }}
        shadows
        gl={{ antialias: true, alpha: true }}
      >
        <color attach="background" args={["#020617"]} />
        <ambientLight intensity={0.8} />
        <directionalLight
          position={[10, 15, 10]}
          intensity={1.5}
          castShadow
          shadow-mapSize-width={1024}
          shadow-mapSize-height={1024}
        />
        <directionalLight position={[-10, 10, -10]} intensity={0.6} color="#93c5fd" />
        <directionalLight position={[0, -10, 0]} intensity={0.4} color="#334155" />
        <Suspense fallback={null}>
          <RubiksCube />
        </Suspense>
        <Controls />
      </Canvas>
    </div>
  )
}
