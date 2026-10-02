import { WsIncomingMessage } from "../types/agent"

export class AgentWebSocket {
  private ws: WebSocket | null = null
  private sessionId: string
  private onMessageCallback: (msg: WsIncomingMessage) => void
  private onStatusChange: (connected: boolean) => void

  constructor(
    sessionId: string = "default",
    onMessage: (msg: WsIncomingMessage) => void,
    onStatusChange: (connected: boolean) => void
  ) {
    self = this as any
    this.sessionId = sessionId
    this.onMessageCallback = onMessage
    this.onStatusChange = onStatusChange
  }

  connect(): void {
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
      return
    }

    const wsUrl = `ws://localhost:8000/api/v1/ws/${this.sessionId}`
    this.ws = new WebSocket(wsUrl)

    this.ws.onopen = () => {
      this.onStatusChange(true)
    }

    this.ws.onclose = () => {
      this.onStatusChange(false)
    }

    this.ws.onerror = () => {
      this.onStatusChange(false)
    }

    this.ws.onmessage = (event) => {
      try {
        const parsed: WsIncomingMessage = JSON.parse(event.data)
        this.onMessageCallback(parsed)
      } catch (e) {
      }
    }
  }

  startSolve(prompt?: string): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ action: "start_solve", prompt }))
    }
  }

  stopSolve(): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ action: "stop_solve" }))
    }
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }
}
