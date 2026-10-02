import { create } from "zustand"

const SOLVED_STATE = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

interface CubeStore {
  facelets: string
  isSolved: boolean
  moveHistory: string[]
  pendingMoves: string[]
  isScrambling: boolean
  isSolving: boolean
  setFacelets: (facelets: string, isSolved?: boolean) => void
  addMoveToHistory: (move: string) => void
  enqueueMoves: (moves: string[]) => void
  dequeueMove: () => string | undefined
  setIsScrambling: (val: boolean) => void
  setIsSolving: (val: boolean) => void
  reset: () => void
}

export const useCubeState = create<CubeStore>((set, get) => ({
  facelets: SOLVED_STATE,
  isSolved: true,
  moveHistory: [],
  pendingMoves: [],
  isScrambling: false,
  isSolving: false,

  setFacelets: (facelets, isSolved) =>
    set({
      facelets,
      isSolved: isSolved !== undefined ? isSolved : facelets === SOLVED_STATE,
    }),

  addMoveToHistory: (move) =>
    set((state) => ({
      moveHistory: [...state.moveHistory, move],
    })),

  enqueueMoves: (moves) =>
    set((state) => ({
      pendingMoves: [...state.pendingMoves, ...moves],
    })),

  dequeueMove: () => {
    const moves = get().pendingMoves
    if (moves.length === 0) return undefined
    const [first, ...rest] = moves
    set({ pendingMoves: rest })
    return first
  },

  setIsScrambling: (val) => set({ isScrambling: val }),
  setIsSolving: (val) => set({ isSolving: val }),

  reset: () =>
    set({
      facelets: SOLVED_STATE,
      isSolved: true,
      moveHistory: [],
      pendingMoves: [],
      isScrambling: false,
      isSolving: false,
    }),
}))
