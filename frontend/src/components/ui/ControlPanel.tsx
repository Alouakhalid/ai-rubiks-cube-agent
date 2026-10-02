import React, { useState } from "react"
import { Shuffle, RotateCcw, BrainCircuit, Square, Palette, Play } from "lucide-react"
import { scrambleCubeState, resetCubeState, sendMove } from "../../services/api"
import { useCubeState } from "../../hooks/useCubeState"
import { VALID_MOVES } from "../../utils/notation"

interface ControlPanelProps {
  onStartSolve: () => void
  onStopSolve: () => void
  onOpenColorPicker: () => void
  isSolving: boolean
}

export const ControlPanel: React.FC<ControlPanelProps> = ({
  onStartSolve,
  onStopSolve,
  onOpenColorPicker,
  isSolving,
}) => {
  const [loading, setLoading] = useState(false)
  const enqueueMoves = useCubeState((s) => s.enqueueMoves)
  const resetCube = useCubeState((s) => s.reset)
  const isSolved = useCubeState((s) => s.isSolved)

  const handleScramble = async () => {
    try {
      setLoading(true)
      const res = await scrambleCubeState(20)
      enqueueMoves(res.scramble)
    } catch (e) {
    } finally {
      setLoading(false)
    }
  }

  const handleReset = async () => {
    try {
      setLoading(true)
      await resetCubeState()
      resetCube()
    } catch (e) {
    } finally {
      setLoading(false)
    }
  }

  const handleManualMove = async (m: string) => {
    enqueueMoves([m])
    try {
      await sendMove(m)
    } catch (e) {
    }
  }

  return (
    <div className="glass-panel rounded-2xl p-5 border border-slate-800 flex flex-col space-y-4">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800/80">
        <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
          Cube Controls
        </h2>
        <span
          className={`text-xs px-2.5 py-0.5 rounded-full font-mono font-medium ${
            isSolved
              ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
              : "bg-amber-500/10 text-amber-400 border border-amber-500/20"
          }`}
        >
          {isSolved ? "SOLVED" : "SCRAMBLED"}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-2.5">
        <button
          onClick={handleScramble}
          disabled={loading || isSolving}
          className="flex items-center justify-center space-x-2 px-4 py-2.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-700/60 text-slate-200 text-sm font-semibold transition disabled:opacity-50"
        >
          <Shuffle className="w-4 h-4 text-cyan-400" />
          <span>Scramble</span>
        </button>

        <button
          onClick={handleReset}
          disabled={loading || isSolving}
          className="flex items-center justify-center space-x-2 px-4 py-2.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-700/60 text-slate-200 text-sm font-semibold transition disabled:opacity-50"
        >
          <RotateCcw className="w-4 h-4 text-slate-400" />
          <span>Reset</span>
        </button>
      </div>

      <button
        onClick={onOpenColorPicker}
        disabled={loading || isSolving}
        className="w-full flex items-center justify-center space-x-2 px-4 py-2.5 rounded-xl bg-indigo-950/40 hover:bg-indigo-900/50 border border-indigo-700/40 text-indigo-200 text-sm font-semibold transition disabled:opacity-50"
      >
        <Palette className="w-4 h-4 text-indigo-400" />
        <span>Enter Colors (Real Cube)</span>
      </button>

      <div>
        {!isSolving ? (
          <button
            onClick={onStartSolve}
            disabled={loading || isSolved}
            className="w-full flex items-center justify-center space-x-2 px-4 py-3 rounded-xl bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-bold shadow-lg shadow-blue-500/20 transition disabled:opacity-50"
          >
            <BrainCircuit className="w-5 h-5 text-white animate-pulse" />
            <span>AI Solve (Groq Agent)</span>
          </button>
        ) : (
          <button
            onClick={onStopSolve}
            className="w-full flex items-center justify-center space-x-2 px-4 py-3 rounded-xl bg-rose-600/90 hover:bg-rose-500 text-white font-bold shadow-lg shadow-rose-500/20 transition"
          >
            <Square className="w-4 h-4 fill-white" />
            <span>Stop AI Agent</span>
          </button>
        )}
      </div>

      <div className="pt-2">
        <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-2">
          Manual Turns
        </label>
        <div className="grid grid-cols-6 gap-1.5 font-mono text-xs">
          {VALID_MOVES.map((m) => (
            <button
              key={m}
              onClick={() => handleManualMove(m)}
              disabled={isSolving}
              className="py-1.5 rounded-lg bg-slate-900/80 hover:bg-slate-800 border border-slate-800 text-slate-300 font-semibold transition active:scale-95 disabled:opacity-40"
            >
              {m}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
