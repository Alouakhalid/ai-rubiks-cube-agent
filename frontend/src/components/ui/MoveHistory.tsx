import React from "react"
import { History } from "lucide-react"
import { useCubeState } from "../../hooks/useCubeState"

export const MoveHistory: React.FC = () => {
  const moveHistory = useCubeState((s) => s.moveHistory)

  return (
    <div className="glass-panel rounded-2xl p-4 border border-slate-800 flex flex-col space-y-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2 text-slate-300">
          <History className="w-4 h-4 text-slate-400" />
          <h3 className="text-xs font-bold uppercase tracking-wider">Move History</h3>
        </div>
        <span className="text-[11px] font-mono text-slate-500">
          Total: {moveHistory.length}
        </span>
      </div>

      <div className="flex items-center space-x-1.5 overflow-x-auto custom-scrollbar py-1">
        {moveHistory.length === 0 ? (
          <span className="text-xs text-slate-600 font-mono">No moves applied yet.</span>
        ) : (
          moveHistory.slice(-18).map((m, idx) => (
            <span
              key={idx}
              className="px-2 py-1 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono font-bold text-cyan-300 flex-shrink-0"
            >
              {m}
            </span>
          ))
        )}
      </div>
    </div>
  )
}
