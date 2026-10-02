import { useEffect, useState, useRef, useCallback } from "react"
import { AgentWebSocket } from "../services/websocket"
import { AgentLogEntry, AgentStatusType, WsIncomingMessage } from "../types/agent"
import { useCubeState } from "./useCubeState"

export function useAgentSocket(sessionId: string = "default") {
  const [isConnected, setIsConnected] = useState(false)
  const [status, setStatus] = useState<AgentStatusType>("IDLE")
  const [statusMessage, setStatusMessage] = useState("AI Agent Standby")
  const [logs, setLogs] = useState<AgentLogEntry[]>([])
  const [currentMove, setCurrentMove] = useState<string | null>(null)
  const [moveProgress, setMoveProgress] = useState({ current: 0, total: 0 })
  const [finalExplanation, setFinalExplanation] = useState<string | null>(null)

  const socketRef = useRef<AgentWebSocket | null>(null)
  const enqueueMoves = useCubeState((s) => s.enqueueMoves)
  const setIsSolving = useCubeState((s) => s.setIsSolving)
  const setFacelets = useCubeState((s) => s.setFacelets)

  const handleMessage = useCallback((msg: WsIncomingMessage) => {
    const timestamp = new Date().toLocaleTimeString()
    const id = Math.random().toString(36).substring(2, 9)

    if (msg.type === "status") {
      if (msg.status) setStatus(msg.status as AgentStatusType)
      if (msg.message) setStatusMessage(msg.message)
      if (msg.state) setFacelets(msg.state)

      setLogs((prev) => [
        ...prev,
        { id, timestamp, type: "status", message: msg.message },
      ])
    } else if (msg.type === "tool_call") {
      setStatus("PLANNING")
      setStatusMessage(`Calling tool: ${msg.tool}`)
      setLogs((prev) => [
        ...prev,
        {
          id,
          timestamp,
          type: "tool_call",
          tool: msg.tool,
          data: msg.args,
          message: `Invoking tool: ${msg.tool}`,
        },
      ])
    } else if (msg.type === "tool_result") {
      setLogs((prev) => [
        ...prev,
        {
          id,
          timestamp,
          type: "tool_result",
          tool: msg.tool,
          data: msg.result,
          message: `Received result from: ${msg.tool}`,
        },
      ])
    } else if (msg.type === "move") {
      setStatus("EXECUTING")
      if (msg.move) {
        setCurrentMove(msg.move)
        enqueueMoves([msg.move])
      }
      if (msg.move_index && msg.total_moves) {
        setMoveProgress({ current: msg.move_index, total: msg.total_moves })
        setStatusMessage(`Executing move: ${msg.move} (${msg.move_index}/${msg.total_moves})`)
      }
    } else if (msg.type === "final") {
      setStatus("COMPLETED")
      setIsSolving(false)
      setCurrentMove(null)
      if (msg.message) {
        setStatusMessage(msg.message)
        setFinalExplanation(msg.message)
      }
      setLogs((prev) => [
        ...prev,
        { id, timestamp, type: "final", message: msg.message },
      ])
    }
  }, [enqueueMoves, setFacelets, setIsSolving])

  useEffect(() => {
    const ws = new AgentWebSocket(sessionId, handleMessage, setIsConnected)
    socketRef.current = ws
    ws.connect()

    return () => {
      ws.disconnect()
    }
  }, [sessionId, handleMessage])

  const startSolve = useCallback((prompt?: string) => {
    if (socketRef.current) {
      setIsSolving(true)
      setStatus("INITIALIZING")
      setStatusMessage("Connecting to Groq AI brain...")
      setLogs([])
      setFinalExplanation(null)
      socketRef.current.startSolve(prompt)
    }
  }, [setIsSolving])

  const stopSolve = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.stopSolve()
      setIsSolving(false)
      setStatus("STOPPED")
      setStatusMessage("AI Solve stopped by user.")
    }
  }, [setIsSolving])

  return {
    isConnected,
    status,
    statusMessage,
    logs,
    currentMove,
    moveProgress,
    finalExplanation,
    startSolve,
    stopSolve,
  }
}
