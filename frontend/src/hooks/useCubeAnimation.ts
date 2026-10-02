import { useEffect, useRef } from "react"
import { useCubeState } from "./useCubeState"

export function useCubeAnimation(onExecuteMove: (move: string, onComplete: () => void) => void) {
  const pendingMoves = useCubeState((s) => s.pendingMoves)
  const dequeueMove = useCubeState((s) => s.dequeueMove)
  const isAnimatingRef = useRef(false)

  useEffect(() => {
    if (isAnimatingRef.current || pendingMoves.length === 0) {
      return
    }

    const nextMove = dequeueMove()
    if (!nextMove) return

    isAnimatingRef.current = true

    onExecuteMove(nextMove, () => {
      isAnimatingRef.current = false
    })
  }, [pendingMoves, dequeueMove, onExecuteMove])
}
