import React, { useRef, useEffect } from "react"
import { Terminal, BrainCircuit, CheckCircle, ShieldAlert, BookOpen } from "lucide-react"
import { AgentLogEntry, AgentStatusType } from "../../types/agent"

interface AgentMonitorProps {
  status: AgentStatusType
  statusMessage: string
  logs: AgentLogEntry[]
  currentMove: string | null
  moveProgress: { current: number; total: number }
  finalExplanation: string | null
}

export const AgentMonitor: React.FC<AgentMonitorProps> = ({
  status,
  statusMessage,
  logs,
  currentMove,
  moveProgress,
  finalExplanation,
}) => {
  const terminalEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [logs])

  const getStatusColor = () => {
    switch (status) {
      case "EXECUTING":
        return "bg-cyan-500/20 text-cyan-400 border-cyan-500/30"
      case "PLANNING":
        return "bg-purple-500/20 text-purple-400 border-purple-500/30"
      case "COMPLETED":
        return "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
      case "STOPPED":
        return "bg-amber-500/20 text-amber-400 border-amber-500/30"
      case "ERROR":
        return "bg-rose-500/20 text-rose-400 border-rose-500/30"
      default:
        return "bg-slate-800 text-slate-400 border-slate-700"
    }
  }

  return (
    <div className="glass-panel rounded-2xl p-5 border border-slate-800 flex flex-col space-y-4 h-full">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <Terminal className="w-4 h-4 text-blue-400" />
          <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
            Agent Telemetry & Logs
          </h2>
        </div>
        <span
          className={`text-xs px-2.5 py-0.5 rounded-full font-mono font-semibold border ${getStatusColor()}`}
        >
          {status}
        </span>
      </div>

      <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800/80 flex flex-col space-y-2">
        <div className="flex items-center justify-between text-xs">
          <span className="text-slate-400">Current Action:</span>
          {currentMove && (
            <span className="px-2 py-0.5 rounded bg-blue-600/30 border border-blue-500/40 text-blue-300 font-mono font-bold">
              Move: {currentMove}
            </span>
          )}
        </div>
        <p className="text-xs text-slate-200 font-mono leading-relaxed line-clamp-2">
          {statusMessage}
        </p>

        {moveProgress.total > 0 && (
          <div className="space-y-1 pt-1">
            <div className="flex justify-between text-[11px] font-mono text-slate-400">
              <span>Progress</span>
              <span>
                {moveProgress.current} / {moveProgress.total} moves
              </span>
            </div>
            <div className="w-full h-1.5 rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-blue-500 to-cyan-400 transition-all duration-150"
                style={{
                  width: `${(moveProgress.current / moveProgress.total) * 100}%`,
                }}
              />
            </div>
          </div>
        )}
      </div>

      <div className="flex-1 bg-slate-950/80 rounded-xl p-3 border border-slate-900 overflow-y-auto max-h-56 custom-scrollbar font-mono text-[11px] space-y-2">
        {logs.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-slate-600 space-y-1">
            <BrainCircuit className="w-6 h-6 opacity-40" />
            <span>Agent idle. Click "AI Solve" to trigger ReAct loop.</span>
          </div>
        ) : (
          logs.map((log) => (
            <div key={log.id} className="space-y-0.5">
              <div className="flex items-center space-x-2 text-[10px] text-slate-500">
                <span>[{log.timestamp}]</span>
                <span className="uppercase text-slate-400">[{log.type}]</span>
              </div>
              <p
                className={`${
                  log.type === "tool_call"
                    ? "text-cyan-400"
                    : log.type === "tool_result"
                    ? "text-indigo-300"
                    : log.type === "final"
                    ? "text-emerald-400 font-bold"
                    : "text-slate-300"
                }`}
              >
                {log.message || JSON.stringify(log.data)}
              </p>
            </div>
          ))
        )}
        <div ref={terminalEndRef} />
      </div>

      {finalExplanation && (
        <div className="p-3 rounded-xl bg-emerald-950/20 border border-emerald-500/30 text-emerald-200 text-xs flex flex-col space-y-1.5">
          <div className="flex items-center space-x-1.5 text-emerald-400 font-bold">
            <BookOpen className="w-4 h-4" />
            <span>Agent Solution Notes (RAG Verified):</span>
          </div>
          <p className="text-xs leading-relaxed text-emerald-200/90 font-mono">
            {finalExplanation}
          </p>
        </div>
      )}
    </div>
  )
}
