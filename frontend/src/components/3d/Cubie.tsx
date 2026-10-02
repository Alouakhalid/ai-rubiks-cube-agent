import React, { useMemo } from "react"
import * as THREE from "three"

interface CubieProps {
  position: [number, number, number]
  colors?: {
    right?: string
    left?: string
    top?: string
    bottom?: string
    front?: string
    back?: string
  }
}

const BODY_COLOR = "#0f172a"

export const Cubie: React.FC<CubieProps> = ({ position, colors = {} }) => {
  const materials = useMemo(() => {
    const cRight = colors.right || (position[0] === 1 ? "#ef4444" : BODY_COLOR)
    const cLeft = colors.left || (position[0] === -1 ? "#f97316" : BODY_COLOR)
    const cTop = colors.top || (position[1] === 1 ? "#f8fafc" : BODY_COLOR)
    const cBottom = colors.bottom || (position[1] === -1 ? "#eab308" : BODY_COLOR)
    const cFront = colors.front || (position[2] === 1 ? "#22c55e" : BODY_COLOR)
    const cBack = colors.back || (position[2] === -1 ? "#3b82f6" : BODY_COLOR)

    const mat = (col: string) =>
      new THREE.MeshStandardMaterial({
        color: col,
        roughness: 0.18,
        metalness: 0.05,
      })

    return [
      mat(cRight),
      mat(cLeft),
      mat(cTop),
      mat(cBottom),
      mat(cFront),
      mat(cBack),
    ]
  }, [position, colors])

  return (
    <mesh position={position} material={materials} castShadow receiveShadow>
      <boxGeometry args={[0.96, 0.96, 0.96]} />
    </mesh>
  )
}
