import React, { useState } from "react"
import { Header } from "./components/ui/Header"
import { Scene } from "./components/3d/Scene"
import { ControlPanel } from "./components/ui/ControlPanel"
import { AgentMonitor } from "./components/ui/AgentMonitor"
import { OrientationGuide } from "./components/ui/OrientationGuide"
import { MoveHistory } from "./components/ui/MoveHistory"
import { ColorPickerModal } from "./components/ui/ColorPickerModal"
import { useAgentSocket } from "./hooks/useAgentSocket"
import { useCubeState } from "./hooks/useCubeState"

export const App: React.FC = () => {
  const [isColorPickerOpen, setIsColorPickerOpen] = useState(false)
  const isSolving = useCubeState((s) => s.isSolving)

  const {
    isConnected,
    status,
    statusMessage,
    logs,
    currentMove,
    moveProgress,
    finalExplanation,
    startSolve,
    stopSolve,
  } = useAgentSocket("default")

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-slate-950">
      <Header isConnected={isConnected} />

      <main className="flex-1 relative overflow-hidden">
        <Scene />

        <div className="absolute top-4 left-4 w-80 flex flex-col space-y-4 pointer-events-auto z-10">
          <ControlPanel
            onStartSolve={() => startSolve()}
            onStopSolve={stopSolve}
            onOpenColorPicker={() => setIsColorPickerOpen(true)}
            isSolving={isSolving}
          />
          <MoveHistory />
        </div>

        <div className="absolute top-4 right-4 w-96 flex flex-col space-y-4 pointer-events-auto z-10">
          <AgentMonitor
            status={status}
            statusMessage={statusMessage}
            logs={logs}
            currentMove={currentMove}
            moveProgress={moveProgress}
            finalExplanation={finalExplanation}
          />
          <OrientationGuide />
        </div>
      </main>

      <ColorPickerModal
        isOpen={isColorPickerOpen}
        onClose={() => setIsColorPickerOpen(false)}
      />
    </div>
  )
}
