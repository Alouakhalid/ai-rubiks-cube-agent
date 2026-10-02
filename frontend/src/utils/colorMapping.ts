import { FaceName, CubeColor } from "../types/cube"

export const FACE_TO_COLOR: Record<FaceName, CubeColor> = {
  U: "white",
  R: "red",
  F: "green",
  D: "yellow",
  L: "orange",
  B: "blue",
}

export const COLOR_TO_HEX: Record<CubeColor, string> = {
  white: "#f8fafc",
  red: "#ef4444",
  green: "#22c55e",
  yellow: "#eab308",
  orange: "#f97316",
  blue: "#3b82f6",
}

export const FACE_TO_HEX: Record<FaceName, string> = {
  U: COLOR_TO_HEX.white,
  R: COLOR_TO_HEX.red,
  F: COLOR_TO_HEX.green,
  D: COLOR_TO_HEX.yellow,
  L: COLOR_TO_HEX.orange,
  B: COLOR_TO_HEX.blue,
}

export const CHAR_TO_COLOR_MAP: Record<string, string> = {
  U: "#f8fafc",
  R: "#ef4444",
  F: "#22c55e",
  D: "#eab308",
  L: "#f97316",
  B: "#3b82f6",
}
