import { CubeStateModel, ValidationResultModel, ScrambleResponseModel } from "../types/cube"

const API_BASE = "http://localhost:8000/api/v1"

export async function fetchCubeState(sessionId: string = "default"): Promise<CubeStateModel> {
  const res = await fetch(`${API_BASE}/cube/state?session_id=${sessionId}`)
  if (!res.ok) throw new Error("Failed to fetch cube state")
  return res.json()
}

export async function resetCubeState(sessionId: string = "default"): Promise<CubeStateModel> {
  const res = await fetch(`${API_BASE}/cube/reset?session_id=${sessionId}`, {
    method: "POST",
  })
  if (!res.ok) throw new Error("Failed to reset cube")
  return res.json()
}

export async function scrambleCubeState(length: number = 20, sessionId: string = "default"): Promise<ScrambleResponseModel> {
  const res = await fetch(`${API_BASE}/cube/scramble?session_id=${sessionId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ length }),
  })
  if (!res.ok) throw new Error("Failed to scramble cube")
  return res.json()
}

export async function sendMove(move: string, sessionId: string = "default"): Promise<CubeStateModel> {
  const res = await fetch(`${API_BASE}/cube/move?session_id=${sessionId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ move }),
  })
  if (!res.ok) throw new Error("Failed to make move")
  return res.json()
}

export async function setFaceletsState(facelets: string, sessionId: string = "default"): Promise<CubeStateModel> {
  const res = await fetch(`${API_BASE}/cube/set-state?session_id=${sessionId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ facelets }),
  })
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}))
    throw new Error(errorData.detail || "Invalid cube configuration")
  }
  return res.json()
}

export async function validateState(facelets?: string, sessionId: string = "default"): Promise<ValidationResultModel> {
  const res = await fetch(`${API_BASE}/cube/validate?session_id=${sessionId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(facelets ? { facelets } : {}),
  })
  if (!res.ok) throw new Error("Validation check failed")
  return res.json()
}

export async function queryKnowledgeRAG(query: string): Promise<any> {
  const res = await fetch(`${API_BASE}/cube/knowledge?q=${encodeURIComponent(query)}`)
  if (!res.ok) throw new Error("Knowledge search failed")
  return res.json()
}
