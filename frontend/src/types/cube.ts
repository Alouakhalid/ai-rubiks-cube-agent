export type FaceName = "U" | "R" | "F" | "D" | "L" | "B"

export type CubeColor = "white" | "red" | "green" | "yellow" | "orange" | "blue"

export interface CubeStateModel {
  facelets: string
  is_solved: boolean
  move_history: string[]
  scramble_sequence?: string | null
}

export interface ValidationResultModel {
  is_valid: boolean
  message: string
  details?: Record<string, any>
}

export interface SolutionResponseModel {
  solution: string[]
  move_count: number
  explanation?: string | null
}

export interface ScrambleResponseModel {
  scramble: string[]
  scramble_string: string
  state: string
  is_solved: boolean
}
