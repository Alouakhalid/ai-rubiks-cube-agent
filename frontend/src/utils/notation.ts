export const VALID_MOVES = [
  "U", "U'", "U2",
  "D", "D'", "D2",
  "L", "L'", "L2",
  "R", "R'", "R2",
  "F", "F'", "F2",
  "B", "B'", "B2",
]

export function invertMove(move: string): string {
  if (move.endsWith("'")) {
    return move[0]
  }
  if (move.endsWith("2")) {
    return move
  }
  return `${move}'`
}

export function invertMoveSequence(moves: string[]): string[] {
  return [...moves].reverse().map(invertMove)
}
