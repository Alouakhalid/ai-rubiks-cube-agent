export type AgentStatusType = "IDLE" | "INITIALIZING" | "OBSERVING" | "PLANNING" | "EXECUTING" | "COMPLETED" | "STOPPED" | "ERROR"

export interface AgentLogEntry {
  id: string
  timestamp: string
  turn?: number
  type: "status" | "tool_call" | "tool_result" | "move" | "final"
  tool?: string
  message?: string
  data?: any
}

export interface WsIncomingMessage {
  type: "status" | "tool_call" | "tool_result" | "move" | "final" | "pong"
  status?: string
  message?: string
  tool?: string
  args?: any
  result?: any
  move?: string
  move_index?: number
  total_moves?: number
  state?: string
  is_solved?: boolean
  moves?: string[]
}
