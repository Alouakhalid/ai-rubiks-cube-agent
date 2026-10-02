import React, { useState } from "react"
import { X, CheckCircle2, AlertTriangle, ArrowRight, ArrowLeft } from "lucide-react"
import { setFaceletsState } from "../../services/api"
import { useCubeState } from "../../hooks/useCubeState"

interface ColorPickerModalProps {
  isOpen: boolean
  onClose: () => void
}

const FACES_ORDER = ["U", "F", "R", "B", "L", "D"]

const FACE_LABELS: Record<string, string> = {
  U: "UP Face (Top - White Center)",
  F: "FRONT Face (Front - Green Center)",
  R: "RIGHT Face (Right - Red Center)",
  B: "BACK Face (Back - Blue Center)",
  L: "LEFT Face (Left - Orange Center)",
  D: "DOWN Face (Bottom - Yellow Center)",
}

const PALETTE: { key: string; name: string; hex: string }[] = [
  { key: "U", name: "White", hex: "#f8fafc" },
  { key: "R", name: "Red", hex: "#ef4444" },
  { key: "F", name: "Green", hex: "#22c55e" },
  { key: "D", name: "Yellow", hex: "#eab308" },
  { key: "L", name: "Orange", hex: "#f97316" },
  { key: "B", name: "Blue", hex: "#3b82f6" },
]

export const ColorPickerModal: React.FC<ColorPickerModalProps> = ({ isOpen, onClose }) => {
  const [currentFaceIndex, setCurrentFaceIndex] = useState(0)
  const [selectedPalette, setSelectedPalette] = useState("U")
  const [stickers, setStickers] = useState<Record<string, string[]>>({
    U: Array(9).fill("U"),
    R: Array(9).fill("R"),
    F: Array(9).fill("F"),
    D: Array(9).fill("D"),
    L: Array(9).fill("L"),
    B: Array(9).fill("B"),
  })
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const setFacelets = useCubeState((s) => s.setFacelets)

  if (!isOpen) return null

  const activeFace = FACES_ORDER[currentFaceIndex]

  const handleStickerClick = (index: number) => {
    if (index === 4) return

    setStickers((prev) => {
      const nextArr = [...prev[activeFace]]
      nextArr[index] = selectedPalette
      return { ...prev, [activeFace]: nextArr }
    })
    setErrorMessage(null)
  }

  const build54FaceletString = (): string => {
    return [
      stickers.U.join(""),
      stickers.R.join(""),
      stickers.F.join(""),
      stickers.D.join(""),
      stickers.L.join(""),
      stickers.B.join(""),
    ].join("")
  }

  const handleValidateAndApply = async () => {
    setIsSubmitting(true)
    setErrorMessage(null)
    const fullString = build54FaceletString()

    try {
      const res = await setFaceletsState(fullString)
      setFacelets(res.facelets, res.is_solved)
      onClose()
    } catch (err: any) {
      setErrorMessage(err.message || "Invalid cube configuration")
    } finally {
      setIsSubmitting(false)
    }
  }

  const colorCounts: Record<string, number> = { U: 0, R: 0, F: 0, D: 0, L: 0, B: 0 }
  Object.values(stickers).forEach((faceArr) => {
    faceArr.forEach((col) => {
      if (colorCounts[col] !== undefined) colorCounts[col]++
    })
  })

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
      <div className="glass-panel-glow rounded-3xl w-full max-w-xl p-6 relative border border-slate-700/60 shadow-2xl flex flex-col space-y-5">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              Physical Cube Color Transcription
            </h3>
            <p className="text-xs text-slate-400">Step {currentFaceIndex + 1} of 6: {FACE_LABELS[activeFace]}</p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex flex-col items-center space-y-4">
          <div className="grid grid-cols-3 gap-2 p-3 bg-slate-900/90 rounded-2xl border border-slate-800 shadow-inner">
            {stickers[activeFace].map((col, idx) => {
              const hex = PALETTE.find((p) => p.key === col)?.hex || "#1e293b"
              const isCenter = idx === 4

              return (
                <button
                  key={idx}
                  onClick={() => handleStickerClick(idx)}
                  disabled={isCenter}
                  style={{ backgroundColor: hex }}
                  className={`w-14 h-14 rounded-xl border border-slate-900/50 shadow-md transition transform active:scale-95 flex items-center justify-center font-bold text-xs ${
                    col === "U" || col === "D" ? "text-slate-900" : "text-white"
                  } ${isCenter ? "cursor-not-allowed opacity-90 ring-2 ring-blue-500/50" : "hover:ring-2 hover:ring-white/60"}`}
                >
                  {isCenter ? "CENTER" : ""}
                </button>
              )
            })}
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-slate-400">Select Paint:</span>
            <div className="flex items-center gap-2">
              {PALETTE.map((p) => (
                <button
                  key={p.key}
                  onClick={() => setSelectedPalette(p.key)}
                  style={{ backgroundColor: p.hex }}
                  className={`w-7 h-7 rounded-lg border border-slate-700 transition ${
                    selectedPalette === p.key ? "ring-2 ring-cyan-400 scale-110" : "opacity-80"
                  }`}
                  title={p.name}
                />
              ))}
            </div>
          </div>

          <div className="grid grid-cols-6 gap-2 w-full pt-1 text-[11px] font-mono">
            {PALETTE.map((p) => {
              const cnt = colorCounts[p.key] || 0
              const isOk = cnt === 9
              return (
                <div
                  key={p.key}
                  className={`p-1.5 rounded-lg border text-center ${
                    isOk
                      ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-400"
                      : "bg-slate-900 border-slate-800 text-slate-400"
                  }`}
                >
                  <span className="block font-semibold">{p.name}</span>
                  <span>{cnt}/9</span>
                </div>
              )
            })}
          </div>
        </div>

        {errorMessage && (
          <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 flex-shrink-0 text-rose-400" />
            <span>{errorMessage}</span>
          </div>
        )}

        <div className="flex items-center justify-between pt-2 border-t border-slate-800">
          <button
            onClick={() => setCurrentFaceIndex((prev) => Math.max(prev - 1, 0))}
            disabled={currentFaceIndex === 0}
            className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 text-xs font-semibold disabled:opacity-30"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Prev Face</span>
          </button>

          {currentFaceIndex < 5 ? (
            <button
              onClick={() => setCurrentFaceIndex((prev) => Math.min(prev + 1, 5))}
              className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold"
            >
              <span>Next Face</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          ) : (
            <button
              onClick={handleValidateAndApply}
              disabled={isSubmitting}
              className="flex items-center space-x-1.5 px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow-lg shadow-emerald-500/20"
            >
              <CheckCircle2 className="w-4 h-4" />
              <span>Validate & Apply</span>
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
