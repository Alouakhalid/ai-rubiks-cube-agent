import React from "react"
import { Cpu, Zap, BookOpen } from "lucide-react"

interface HeaderProps {
  isConnected: boolean
}

export const Header: React.FC<HeaderProps> = ({ isConnected }) => {
  return (
    <header className="h-16 px-6 glass-panel border-b border-slate-800 flex items-center justify-between z-20">
      <div className="flex items-center space-x-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-400 flex items-center justify-center shadow-lg shadow-blue-500/20">
          <Cpu className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
            AI Rubik's Cube Agent
            <span className="text-xs px-2 py-0.5 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 font-mono">
              Qwen + Cohere RAG
            </span>
          </h1>
          <p className="text-xs text-slate-400">Deterministic Engine + Groq Qwen 2.5 32B + Cohere Rerank</p>
        </div>
      </div>

      <div className="flex items-center space-x-3">
        <div className="hidden sm:flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-900/60 border border-slate-800 text-xs text-slate-300">
          <BookOpen className="w-3.5 h-3.5 text-cyan-400" />
          <span className="font-mono text-slate-400">RAG:</span>
          <span className="font-semibold text-cyan-300">Cohere v3.5</span>
        </div>

        <div className="hidden sm:flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-900/60 border border-slate-800 text-xs text-slate-300">
          <Zap className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
          <span className="font-mono text-slate-400">Groq:</span>
          <span className="font-semibold text-slate-200">Qwen 2.5 32B</span>
        </div>

        <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-900/60 border border-slate-800 text-xs">
          <span
            className={`w-2 h-2 rounded-full ${
              isConnected ? "bg-emerald-400 animate-pulse" : "bg-rose-500"
            }`}
          />
          <span className="font-mono text-slate-400">
            {isConnected ? "Engine Sync" : "Connecting..."}
          </span>
        </div>
      </div>
    </header>
  )
}
