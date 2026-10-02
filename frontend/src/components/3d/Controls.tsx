import React from "react"
import { OrbitControls } from "@react-three/drei"

export const Controls: React.FC = () => {
  return (
    <OrbitControls
      makeDefault
      enableDamping
      dampingFactor={0.06}
      minDistance={4}
      maxDistance={14}
      rotateSpeed={0.8}
    />
  )
}
