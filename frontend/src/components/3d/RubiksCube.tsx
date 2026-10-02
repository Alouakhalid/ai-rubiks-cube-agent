import React, { useRef, useMemo, useCallback } from "react"
import { useFrame } from "@react-three/fiber"
import * as THREE from "three"
import { Cubie } from "./Cubie"
import { useCubeState } from "../../hooks/useCubeState"
import { useCubeAnimation } from "../../hooks/useCubeAnimation"

interface ActiveAnimation {
  face: string
  axis: THREE.Vector3
  angleTarget: number
  angleCurrent: number
  cubies: THREE.Object3D[]
  onComplete: () => void
}

export const RubiksCube: React.FC = () => {
  const groupRef = useRef<THREE.Group>(null)
  const pivotRef = useRef<THREE.Group>(null)
  const animationRef = useRef<ActiveAnimation | null>(null)

  const facelets = useCubeState((s) => s.facelets)
  const addMoveToHistory = useCubeState((s) => s.addMoveToHistory)

  const initialPositions = useMemo(() => {
    const coords: [number, number, number][] = []
    for (let x = -1; x <= 1; x++) {
      for (let y = -1; y <= 1; y++) {
        for (let z = -1; z <= 1; z++) {
          if (x === 0 && y === 0 && z === 0) continue
          coords.push([x, y, z])
        }
      }
    }
    return coords
  }, [])

  const executeMove = useCallback((move: string, onComplete: () => void) => {
    if (!groupRef.current || !pivotRef.current) {
      onComplete()
      return
    }

    const face = move[0]
    let angle = -Math.PI / 2
    if (move.endsWith("'")) angle = Math.PI / 2
    else if (move.endsWith("2")) angle = -Math.PI

    let axis = new THREE.Vector3(0, 1, 0)
    let condition = (pos: THREE.Vector3) => Math.round(pos.y) === 1

    if (face === "U") {
      axis = new THREE.Vector3(0, 1, 0)
      condition = (pos) => Math.round(pos.y) === 1
      angle = -angle
    } else if (face === "D") {
      axis = new THREE.Vector3(0, 1, 0)
      condition = (pos) => Math.round(pos.y) === -1
    } else if (face === "L") {
      axis = new THREE.Vector3(1, 0, 0)
      condition = (pos) => Math.round(pos.x) === -1
    } else if (face === "R") {
      axis = new THREE.Vector3(1, 0, 0)
      condition = (pos) => Math.round(pos.x) === 1
      angle = -angle
    } else if (face === "F") {
      axis = new THREE.Vector3(0, 0, 1)
      condition = (pos) => Math.round(pos.z) === 1
      angle = -angle
    } else if (face === "B") {
      axis = new THREE.Vector3(0, 0, 1)
      condition = (pos) => Math.round(pos.z) === -1
    }

    const pivot = pivotRef.current
    const mainGroup = groupRef.current

    pivot.rotation.set(0, 0, 0)
    pivot.position.set(0, 0, 0)

    const targetCubies: THREE.Object3D[] = []
    const worldPos = new THREE.Vector3()

    mainGroup.children.forEach((child) => {
      child.getWorldPosition(worldPos)
      if (condition(worldPos)) {
        targetCubies.push(child)
      }
    })

    targetCubies.forEach((cubie) => {
      pivot.attach(cubie)
    })

    animationRef.current = {
      face,
      axis,
      angleTarget: angle,
      angleCurrent: 0,
      cubies: targetCubies,
      onComplete: () => {
        targetCubies.forEach((cubie) => {
          mainGroup.attach(cubie)
          cubie.position.set(
            Math.round(cubie.position.x),
            Math.round(cubie.position.y),
            Math.round(cubie.position.z)
          )
        })
        pivot.rotation.set(0, 0, 0)
        addMoveToHistory(move)
        onComplete()
      },
    }
  }, [addMoveToHistory])

  useCubeAnimation(executeMove)

  useFrame((_, delta) => {
    const anim = animationRef.current
    if (!anim || !pivotRef.current) return

    const speed = 12
    const step = (anim.angleTarget - anim.angleCurrent) * Math.min(delta * speed, 1)
    anim.angleCurrent += step

    pivotRef.current.rotateOnAxis(anim.axis, step)

    if (Math.abs(anim.angleTarget - anim.angleCurrent) < 0.005) {
      const finalDiff = anim.angleTarget - anim.angleCurrent
      pivotRef.current.rotateOnAxis(anim.axis, finalDiff)
      animationRef.current = null
      anim.onComplete()
    }
  })

  return (
    <>
      <group ref={pivotRef} />
      <group ref={groupRef}>
        {initialPositions.map((pos, idx) => (
          <Cubie key={`${pos[0]}_${pos[1]}_${pos[2]}_${idx}`} position={pos} />
        ))}
      </group>
    </>
  )
}
