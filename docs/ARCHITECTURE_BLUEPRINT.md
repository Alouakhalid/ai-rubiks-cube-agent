# AI Rubik's Cube Agent — Technical Architecture Blueprint

## 1. Project Overview
The **AI Rubik's Cube Agent** is an interactive 3D web application where users can manipulate, scramble, or input real-world Rubik's Cube states, and an AI Agent powered by the **Groq API** analyzes the cube state and orchestrates its solution.

### Core Philosophy
* **Cube Engine as Single Source of Truth:** The LLM does not simulate or calculate permutations in its latent weights.
* **Deterministic Tool Delegation:** Mathematical solving is handled by Herbert Kociemba's Two-Phase Algorithm exposed as a first-class agent tool.
* **Agent as Cognitive Orchestrator:** The Groq-powered agent is responsible for task planning, validation auditing, tool selection, move-by-move execution supervision, and human-readable pedagogical explanations.

---

## 2. Core Requirements

### Functional Requirements
1. **Mode A (Manual 3D Manipulation):** Full 3D mouse/touch interaction allowing arbitrary Singmaster face turns (U, U', D, D', L, L', R, R', F, F', B, B').
2. **Mode B (Random Scramble):** Server-side generation of valid scrambles (15-25 moves) with smooth 3D animation and state synchronization.
3. **Mode C (Physical Color Entry):** Guided 6-face color picker with orientation stabilization (White UP, Green FRONT) and mathematical validity checks.
4. **Agentic Tool Calling:** Groq LLM uses structured tool calls (get_cube_state, validate_cube, solve_cube_algorithmic, apply_moves) to solve the cube.
5. **Real-Time Streaming:** WebSocket protocol delivers agent thoughts, status transitions, and move queues to the client with sub-second latency.
6. **Execution Control:** Immediate abort/cancel functionality that safely halts the agent and leaves the cube in a consistent state.

### Non-Functional Requirements
* **Frame Rate:** Consistent 60 FPS 3D rendering using Three.js and React Three Fiber.
* **Solver Latency:** Sub-100ms algorithmic solution generation.
* **Inference Latency:** 300-500+ tokens/sec using Groq LPU hardware.
* **State Parity:** Zero divergence between the client-side Three.js scene graph and the backend Cube Engine state.

---

## 3. High-Level Architecture

```
+-----------------------------------------------------------------------------------+
|                                  CLIENT BROWSER                                   |
|                                                                                   |
|  +---------------------------+   +-------------------+   +---------------------+  |
|  |     3D WebGL Canvas       |   |    UI Controls    |   | Color Input Modal   |  |
|  |  (React Three Fiber/Drei) |   |  (Scramble/Solve) |   |  (Guided 6 Faces)   |  |
|  +-------------+-------------+   +---------+---------+   +----------+----------+  |
|                ^                           |                        |             |
|                |                           v                        v             |
|                |              +------------------------------------------+        |
|                +--------------+         Zustand / Cube State Store       |        |
|                               +--------------------+---------------------+        |
+----------------------------------------------------|------------------------------+
                                                     | HTTP / WebSocket
                                                     v
+-----------------------------------------------------------------------------------+
|                                 FASTAPI BACKEND                                   |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                              API Gateway / Routers                          |  |
|  |       [REST: /api/v1/cube]                     [WebSocket: /api/v1/ws]      |  |
|  +---------------------+---------------------------------------+---------------+  |
|                        |                                       |                  |
|                        v                                       v                  |
|  +-------------------------------------+   +-----------------------------------+  |
|  |         Session Manager             |   |        Agent Orchestrator         |  |
|  |   (In-Memory Active Cube States)    |   |     (ReAct Loop / LangGraph)      |  |
|  +---------------------+---------------+   +-------------------+---------------+  |
|                        |                                       |                  |
|                        |       Tool Execution Pipeline         |                  |
|                        +-------------------+-------------------+                  |
|                                            |                                      |
|                                            v                                      |
|                        +---------------------------------------+                  |
|                        |             Tool Registry             |                  |
|                        +-----+-------------------+-------+-----+                  |
|                              |                   |       |                        |
|                              v                   v       v                        |
|                     +-----------------+  +-----------+  +--------------------+    |
|                     |   Cube Engine   |  | Validator |  |  Kociemba Solver   |    |
|                     +-----------------+  +-----------+  +--------------------+    |
+-----------------------------------------------------------------------------------+
                                             ^
                                             | Groq Tool Calling
                                             v
                              +-----------------------------+
                              |      Groq Cloud API         |
                              |  (llama-3.3-70b-versatile)  |
                              +-----------------------------+
```

---

## 4. Component Architecture

### Frontend (React + TypeScript)
* **Scene.tsx:** Sets up Three.js perspective camera, dynamic studio lighting, soft shadows, and orbit controls with dampening.
* **RubiksCube.tsx:** Renders 26 physical cubie meshes, handles rotation animation groups, and translates backend state into 3D orientations.
* **Cubie.tsx:** Represents a single 1x1x1 piece with rounded chamfers, black plastic body, and 6 face materials.
* **Controls.tsx:** Floating glassmorphic HUD hosting Scramble, Solve, Reset, and Manual Move actions.
* **ColorPickerModal.tsx:** Interactive unwrapped net for entering physical cube colors face by face.
* **AgentMonitor.tsx:** Observability terminal displaying current agent activity, move queue, latency metrics, and natural language explanations.

### Backend (FastAPI + Python)
* **CubeEngine:** Object-oriented representation of the 3x3x3 cube maintaining exact piece permutation and orientation arrays.
* **CubeValidator:** Implements group theory parity checks (permutation parity, edge orientation sum, corner orientation sum).
* **KociembaSolver:** High-performance deterministic solver producing optimal or near-optimal solutions (<= 20 moves).
* **AgentOrchestrator:** Execution supervisor managing conversations with Groq, executing requested tools, and enforcing safeguards.
* **GroqClient:** Thread-safe wrapper handling retries, backoff, and tool-call schema serialization for Groq's API.
* **WebSocketHub:** Manages real-time bidirectional messaging, client heartbeat, and graceful cancellation.

---

## 5. Agent Architecture

### Design Philosophy
The AI Agent operates strictly under an **Augmented Determinism** paradigm:
* The LLM does not compute moves by itself.
* The LLM operates as an **Orchestrator and Explainer**:
  1. It inspects the current cube state via `get_cube_state`.
  2. It validates the state via `validate_cube` to detect impossible configurations.
  3. It invokes `solve_cube_algorithmic` to obtain the mathematically minimal solution.
  4. It iterates through moves or batches them via `apply_moves`.
  5. It synthesizes beginner-friendly explanations of each solve phase.

### Context Management
* **System Prompt:** Injects strict guidelines enforcing tool usage, preventing hallucinated move notations, and setting a professional, educational tone.
* **Sliding Window:** Move logs and historical outputs are summarized once length exceeds 10 turns to conserve Groq token context and maintain rapid response cycles.

---

## 6. Cube Engine Architecture

### State Representation
The cube state is maintained using two complementary models:

1. **Facelet Model (Singmaster 54-String):**
   * Standard ordering: `U1..U9 R1..R9 F1..F9 D1..D9 L1..L9 B1..B9`.
   * Colors represented as standard face identifiers: `U` (White), `R` (Red), `F` (Green), `D` (Yellow), `L` (Orange), `B` (Blue).
   * Compatible with standard Kociemba algorithms.

2. **Permutation & Orientation Model:**
   * **8 Corners:** Tracked as permutation (0..7) and orientation (0, 1, 2) where orientation represents clockwise twist relative to the U/D axis.
   * **12 Edges:** Tracked as permutation (0..11) and orientation (0, 1) where orientation represents flip relative to the reference slice.
   * **6 Fixed Centers:** Absolute spatial references establishing coordinate axes.

### Parity Laws & Invariants
Before attempting any solve, the engine enforces the 4 fundamental Rubik's Cube invariants:
1. **Sticker Distribution:** Exactly 9 stickers of each of the 6 colors.
2. **Edge Flip Parity:** sum(edge_orientation[i]) mod 2 == 0
3. **Corner Twist Parity:** sum(corner_orientation[i]) mod 3 == 0
4. **Permutation Parity:** sgn(corner_permutation) == sgn(edge_permutation)

---

## 7. Solver Architecture

### Comparison of Approaches

| Approach | Speed | Move Count | Reliability | Feasibility in LLM Context |
| :--- | :--- | :--- | :--- | :--- |
| **Pure LLM Generation** | ~1-3s | 40-100+ (invalid) | Extremely Low (<5%) | Inviable (hallucinates impossible states) |
| **IDA* (Breadth Search)** | Variable | Optimal (15-20) | High | Memory intensive, slow for deep scrambles |
| **Kociemba Two-Phase** | **<50ms** | **Near-Optimal (<= 20)**| **100% Deterministic**| **Ideal (fast, compact, production-ready)** |

### Selected Strategy: Herbert Kociemba Two-Phase Algorithm
* **Phase 1:** Reduces the arbitrary cube state to the subgroup G1 = <U, D, R2, L2, F2, B2>.
* **Phase 2:** Solves the cube completely within G1 using only quarter turns of U/D and half turns of R, L, F, B.
* **Integration:** Embedded directly into the Python backend using the battle-tested `kociemba` library, providing sub-50ms execution.

---

## 8. Groq Integration

### Groq LPU Advantage
By deploying the Agent Orchestrator over the Groq LPU, the system achieves generation speeds exceeding 300 tokens per second.

### Architecture Specifications
* **Default Model:** `llama-3.3-70b-versatile`.
* **Temperature:** `0.0` (zero randomness to guarantee deterministic JSON tool calls).
* **API Key Security:** Key is strictly loaded into backend environment (`GROQ_API_KEY`) and never passed to the client.
* **Infinite Loop Prevention:** Orchestrator implements an explicit `MAX_AGENT_TURNS = 10` safeguard.

---

## 9. Tool Calling Architecture

All tools are exposed to Groq via strict JSON Schema function definitions:
* `get_cube_state()`: Returns 54-facelet representation, scramble depth, and solved status.
* `validate_cube()`: Performs group theory parity checks to ensure physical solvability.
* `solve_cube_algorithmic(max_length)`: Calculates the mathematically optimal solution sequence using the Kociemba solver.
* `apply_moves(moves)`: Applies a sequence of Singmaster moves to the internal Cube Engine.
* `check_solved()`: Checks if all 6 faces have uniform colors.

---

## 10. 3D Frontend Architecture

### Graphics Pipeline (React Three Fiber + Drei)
* **Mesh Construction:** 26 individual `Cubie` meshes arranged in a 3D coordinate grid x, y, z in {-1, 0, 1} (excluding (0,0,0)).
* **Material & Lighting:** MeshStandardMaterial with physical roughness (0.25) and metalness (0.05). Rounded box buffers. Studio lighting setup.

### Rotation & Animation Mechanism
To execute a face turn (e.g., R):
1. Identify all 9 cubies satisfying x = 1.
2. Temporarily reparent these 9 cubies to a virtual Three.js `PivotGroup` centered at (0,0,0).
3. Interpolate the pivot's quaternion around the X-axis by -pi/2 radians using cubic ease (250ms duration).
4. Update world matrices, reparent to main cube scene, round positions to nearest cardinal integers, update internal state.

---

## 11. User Interaction Modes

### Mode A: Manual 3D Manipulation
* Raycast picking on facelets, vector projection to deduce rotation axis, instant parity synchronization.

### Mode B: Random Scramble
* Generates 20-move non-canceling sequence, animates at 100ms intervals, enables AI Solve.

### Mode C: Physical Cube Color Input
* Step-by-step 6-face wizard with physical orientation anchor.

---

## 12. Color Input Workflow & Orientation Guide

### Spatial Reference Anchor
* **UP:** White Face (pointing toward the ceiling)
* **FRONT:** Green Face (pointing directly at the user)
* **RIGHT:** Red Face
* **BACK:** Blue Face
* **LEFT:** Orange Face
* **DOWN:** Yellow Face

```
                      +---------------+
                      |   UP (White)  |
                      +---------------+
+---------------+     +---------------+     +---------------+     +---------------+
|  LEFT (Orange)| --> | FRONT (Green) | --> |  RIGHT (Red)  | --> |  BACK (Blue)  |
+---------------+     +---------------+     +---------------+     +---------------+
                      +---------------+
                      | DOWN (Yellow) |
                      +---------------+
```

---

## 13. AI Solve Workflow

```
[User clicks "AI Solve"]
        |
        v
[Frontend emits WebSocket frame: START_SOLVE]
        |
        v
[Backend Orchestrator locks session state]
        |
        v
[Orchestrator invokes Groq with system prompt & tool definitions]
        |
        +---> [Groq calls: get_cube_state()]
        v
[Groq calls: validate_cube()]
        v
[Groq calls: solve_cube_algorithmic()]
        v
[Groq calls: apply_moves(["U", "R2", ...])]
        |
        +---> [Backend streams move-by-move events to WebSocket]
                    |
                    v
        [Frontend enqueues moves in 3D Animation Queue]
                    |
                    v
[Agent calls check_solved() -> returns solved: true]
        |
        v
[Groq outputs summary explanation of the solve phases]
        |
        v
[Frontend triggers "Cube Solved" celebration animation]
```

---

## 14. Data Flow Diagrams

### A. Manual Cube Manipulation
```
User Drag on Facelet
        |
  [Three.js Raycaster] ---> Compute Normal & Drag Vector
        |
  [Client Animation] -----> Rotate 9 Cubies in PivotGroup (250ms)
        |
  [HTTP POST /api/v1/cube/move]
        |
  [Backend CubeEngine] ---> Apply Move Matrix -> Return new state hash
```

### B. Random Scramble Flow
```
User clicks "Scramble"
        |
  [HTTP POST /api/v1/cube/scramble]
        |
  [Backend Engine] -------> Generates 20-move non-redundant sequence
        |                   Applies to internal state
        v
  Returns { moves: ["R", "U'", ...], state: "..." }
        |
  [Client Queue] ---------> Plays moves at 100ms intervals
```

### C. Color Input Flow
```
User clicks 54 stickers in Modal
        |
  [HTTP POST /api/v1/cube/set-state]
        |
  [Backend Validator] ----> 1. Count checks (9 per color)
                            2. Orientation parity sum check
                            3. Permutation parity check
        |
  [Valid]   --------------> Update state -> Sync 3D canvas -> Enable Solve
  [Invalid] --------------> Return 422 with precise explanation
```

### D. AI Solving Flow
```
Frontend WS                Backend Server                Groq API
    |                             |                          |
    |---- { action: "solve" } --->|                          |
    |                             |---- chat.completions --->|
    |                             |<--- tool_call: solve ----|
    |                             |                          |
    |                             |-- [Kociemba Solver]      |
    |                             |-- returns solution moves |
    |                             |                          |
    |                             |---- tool_result -------->|
    |                             |<--- tool_call: apply --->|
    |<--- { move: "R", idx: 1 } --|                          |
    |<--- { move: "U'", idx: 2} --|                          |
    |             ...             |                          |
    |<--- { status: "solved" } ---|<--- "Cube is solved" ----|
```

---

## 15. Backend Structure

```
backend/
├── app/
│   ├── main.py                  # FastAPI application entrypoint & lifespan
│   ├── config.py                # Pydantic BaseSettings (Groq key, CORS, ports)
│   ├── agent/
│   │   ├── orchestrator.py      # ReAct Agent loop, turn enforcement, loop break
│   │   └── prompts.py           # System prompts, role instructions, examples
│   ├── api/
│   │   └── v1/
│   │       ├── cube_router.py   # REST: /state, /move, /scramble, /set-state
│   │       ├── agent_router.py  # REST: /solve/sync fallback
│   │       └── ws_router.py     # WebSocket: /ws/solve (streaming moves & state)
│   ├── cube/
│   │   ├── constants.py         # Singmaster notations, facelet index maps, colors
│   │   ├── models.py            # Pydantic schemas (CubeState, MoveRequest, etc.)
│   │   ├── engine.py            # Permutation arrays, transition tables, move logic
│   │   └── validator.py         # Group theory parity checks & error diagnostics
│   ├── solver/
│   │   ├── base.py              # Abstract solver interface
│   │   └── kociemba_solver.py   # Kociemba 2-phase algorithm wrapper
│   ├── tools/
│   │   ├── registry.py          # JSON schema builder & tool dispatcher
│   │   └── cube_tools.py        # Concrete tool implementations
│   └── services/
│       ├── groq_client.py       # Groq API client with exponential retries
│       └── session_manager.py   # Active cube state memory store by session ID
├── tests/
│   ├── test_cube_engine.py      # Unit tests for moves, reversibility, centers
│   ├── test_validator.py        # Unit tests for invalid stickers & parity flips
│   ├── test_solver.py           # Unit tests for Kociemba solver outputs
│   ├── test_tools.py            # Unit tests for tool calling interfaces
│   ├── test_agent.py            # Mocked agent execution & loop break tests
│   └── test_api.py              # FastAPI TestClient endpoint integration tests
├── requirements.txt
└── Dockerfile
```

---

## 16. Frontend Structure

```
frontend/
├── public/
│   └── index.html               # HTML5 canvas container
├── src/
│   ├── main.tsx                 # React DOM root
│   ├── App.tsx                  # Main layout, HUD overlay, 3D viewport
│   ├── index.css                # TailwindCSS base styles
│   ├── components/
│   │   ├── 3d/
│   │   │   ├── Scene.tsx        # Canvas, lighting, camera, environment
│   │   │   ├── RubiksCube.tsx   # 26 cubies assembly & animation coordinator
│   │   │   ├── Cubie.tsx        # Individual 1x1x1 beveled mesh with 6 materials
│   │   │   └── Controls.tsx     # Arcball / OrbitControls integration
│   │   └── ui/
│   │       ├── Header.tsx           # Logo, connection status, theme
│   │       ├── ControlPanel.tsx     # Scramble, Solve, Reset, Undo actions
│   │       ├── ColorPickerModal.tsx # 6-face physical cube input net
│   │       ├── OrientationGuide.tsx # 3D orientation mini-compass (U=White, F=Green)
│   │       ├── AgentMonitor.tsx     # Terminal showing agent logs, metrics, tokens
│   │       └── MoveHistory.tsx      # Chronological move ribbon
│   ├── hooks/
│   │   ├── useCubeState.ts      # Zustand state store for local cube state
│   │   ├── useAgentSocket.ts    # WebSocket connection & message parsing hook
│   │   └── useCubeAnimation.ts  # Animation queue manager & easing curves
│   ├── services/
│   │   ├── api.ts               # Axios / Fetch client for REST endpoints
│   │   └── websocket.ts         # Resilient WebSocket connection manager
│   ├── types/
│   │   ├── cube.ts              # Facelet, Color, Move, State interfaces
│   │   └── agent.ts             # Agent status, log entry, WebSocket message types
│   └── utils/
│       ├── notation.ts          # Move parsing, inverse move computation
│       └── colorMapping.ts      # Singmaster colors to hex color constants
├── package.json
├── tsconfig.json
├── vite.config.ts
└── Dockerfile
```

---

## 17. Database Decision

* **Decision:** In-Memory Session Store with optional Redis adapter. No relational database for core MVP.
* **Reason:** Cube state is 54 characters. In-memory storage gives sub-millisecond response times.

---

## 18. Security

1. **API Key Isolation:** GROQ_API_KEY resides strictly in backend environment variables.
2. **Tool Whitelisting:** Agent can only execute registered, Pydantic-validated tool calls.
3. **Execution Guardrails:** Hard limit of 10 agent turns prevents infinite loops.
4. **Input Sanitization:** Move validator rejects any command not matching Singmaster grammar.

---

## 19. Testing Strategy

* **Unit Tests:** Parity checks, move reversibility (R then R'), 4x rotations (U^4 = I), Superflip verification.
* **Solver Tests:** 500 random scrambles solved and verified.
* **Agent Tests:** Mocked Groq responses verifying tool execution order.
* **3D Synchronization:** Verifying Three.js mesh orientation matches backend state hashes.

---

## 20. Observability

* Structured JSON logging in backend.
* Safe status events over WebSocket (no raw chain-of-thought leaked).
* Telemetry metrics: latency (ms), token usage, solve depth, TPS.

---

## 21. Technology Stack

* **Frontend:** React 19, TypeScript, Three.js, React Three Fiber, Drei, TailwindCSS, Zustand.
* **Backend:** Python 3.11+, FastAPI, Pydantic v2, Kociemba, Groq SDK.
* **AI Model:** Groq `llama-3.3-70b-versatile`.
* **Deployment:** Docker & Docker Compose.

---

## 22. One-Agent vs Multi-Agent Analysis

* **Verdict:** Single Orchestrator Agent is superior.
* Multi-agent adds significant latency (3-8s vs 500ms), 4x token costs, and unnecessary points of failure for a problem with deterministic mathematical solutions.

---

## 23. Development Roadmap

* **Phase 1:** Deterministic Domain Core (Engine, Validator, Kociemba Solver).
* **Phase 2:** Backend REST & WebSocket Services (FastAPI, Session Manager, Tools).
* **Phase 3:** 3D WebGL Visualization (R3F Canvas, Cubies, Quaternion Rotation).
* **Phase 4:** User Interaction & Guided Color Entry Wizard.
* **Phase 5:** Groq Agentic Orchestration & Streaming Execution.
* **Phase 6:** End-to-End Hardening, UI Polish, Testing & Deployment.

---

## 24. MVP Scope
* 3D Rubik's Cube with smooth face rotations.
* Valid random scrambler.
* Guided 6-face physical color input with parity detection.
* Groq-powered single-agent orchestrator with tool calling.
* Herbert Kociemba deterministic solver.
* WebSocket move streaming.
* Agent observability HUD.

---

## 25. Future Features
* Computer vision cube scanner (webcam input).
* Pedagogical CFOP / Beginner tutor.
* Speedcubing smart-timer with TPS analytics.

---

## 26. Risks and Technical Challenges
* Client/server desynchronization (mitigated with state hashes).
* Quaternion numerical drift in 3D (mitigated with cardinal integer snapping).
* Groq rate limits (mitigated with exponential backoff and direct algorithmic fallback).

---

## 27. Final Recommended Architecture
A decoupled Deterministic-Agentic Hybrid architecture with React Three Fiber frontend, FastAPI backend, Kociemba solver, and Groq `llama-3.3-70b-versatile` orchestrator.
