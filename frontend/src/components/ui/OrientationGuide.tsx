import React from "react"
import { Compass } from "lucide-react"

export const OrientationGuide: React.FC = () => {
  return (
    <div className="glass-panel rounded-2xl p-4 border border-slate-800 flex flex-col space-y-3">
      <div className="flex items-center space-x-2 text-slate-300">
        <Compass className="w-4 h-4 text-cyan-400" />
        <h3 className="text-xs font-bold uppercase tracking-wider">Spatial Orientation Guide</h3>
      </div>

      <p className="text-xs text-slate-400 leading-relaxed">
        Hold the physical cube firmly facing you:
      </p>

      <div className="grid grid-cols-3 gap-2 text-xs font-mono">
        <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800 flex flex-col items-center">
          <span className="text-[10px] text-slate-500 uppercase">UP (Top)</span>
          <span className="w-3.5 h-3.5 rounded-full bg-white border border-slate-600 my-1" />
          <span className="font-semibold text-white">White (U)</span>
        </div>

        <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800 flex flex-col items-center">
          <span className="text-[10px] text-slate-500 uppercase">FRONT (Face)</span>
          <span className="w-3.5 h-3.5 rounded-full bg-emerald-500 my-1" />
          <span className="font-semibold text-emerald-400">Green (F)</span>
        </div>

        <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800 flex flex-col items-center">
          <span className="text-[10px] text-slate-500 uppercase">RIGHT</span>
          <span className="w-3.5 h-3.5 rounded-full bg-rose-500 my-1" />
          <span className="font-semibold text-rose-400">Red (R)</span>
        </div>

        <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800 flex flex-col items-center">
          <span className="text-[10px] text-slate-500 uppercase">LEFT</span>
          <span className="w-3.5 h-3.5 rounded-full bg-orange-500 my-1" />
          <span className="font-semibold text-orange-400">Orange (L)</span>
        </div>

        <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800 flex flex-col items-center">
          <span className="text-[10px] text-slate-500 uppercase">DOWN (Base)</span>
          <span className="w-3.5 h-3.5 rounded-full bg-amber-400 my-1" />
          <span className="font-semibold text-amber-300">Yellow (D)</span>
        </div>

        <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800 flex flex-col items-center">
          <span className="text-[10px] text-slate-500 uppercase">BACK</span>
          <span className="w-3.5 h-3.5 rounded-full bg-blue-500 my-1" />
          <span className="font-semibold text-blue-400">Blue (B)</span>
        </div>
      </div>
    </div>
  )
}
