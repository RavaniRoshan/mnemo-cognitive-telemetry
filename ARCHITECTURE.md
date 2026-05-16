# Mnemo Architecture

> **Cognitive Observability Infrastructure — System Architecture Document**

---

## 1. High-Level Architecture

Mnemo implements a **pipeline-based cognitive telemetry architecture** with four primary layers:

```
┌──────────────────────────────────────────────────────────────────┐
│                      INGESTION LAYER                              │
│  ┌────────────────┐    ┌────────────────┐    ┌────────────────┐  │
│  │ TraceRecorder  │───▶│   JSONL Log    │───▶│  TraceLoader   │  │
│  │ (agent-side)   │    │   (persistent) │    │  (typed parse) │  │
│  └────────────────┘    └────────────────┘    └────────────────┘  │
├──────────────────────────────────────────────────────────────────┤
│                       ANALYSIS LAYER                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────┐│
│  │  BeliefState │ │   Failure    │ │    Trace     │ │  Replay  ││
│  │   Tracker    │ │  Attributor  │ │   Enricher   │ │  Engine  ││
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────┘│
├──────────────────────────────────────────────────────────────────┤
│                       AGGREGATION LAYER                           │
│  ┌──────────────────────────────────────────────────────────────┐│
│  │                    MetricsAggregator                         ││
│  │    Per-Trace Metrics → Aggregate Statistics → JSON Export    ││
│  └──────────────────────────────────────────────────────────────┘│
├──────────────────────────────────────────────────────────────────┤
│                     PRESENTATION LAYER                            │
│  ┌──────────────────────────────────────────────────────────────┐│
│  │                     CLI Inspector                            ││
│  │   Color-coded trace visualization with ANSI terminal output  ││
│  └──────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Data Model — Cognitive Trace Schema

### 2.1 Event Hierarchy

All events inherit from a base `Event` class with `timestamp` and `event_type` fields:

```
Event (abstract)
├── EpisodeStart    — Agent session boundary
├── Observation     — Environmental perception
├── MemoryRead      — Memory retrieval event
├── Reasoning       — Internal reasoning chain
├── Action          — Tool/environment interaction
├── Outcome         — Action result (Success/Error)
├── Failure         — Terminal failure condition
└── Success         — Successful terminal state
```

### 2.2 Action-Outcome Coupling

Actions are linked to their resulting outcomes at parse time:

```
Action ──next_outcome──▶ Outcome
```

This enables causal chain traversal without requiring temporal index scanning.

### 2.3 Episode Segmentation

Traces are segmented into logical `Episode` boundaries via `EpisodeStart` markers:

```
Episode {
    agent_name: str
    episode_id: UUID
    start_time: ISO-8601
    events: List[Event]
}
```

---

## 3. Core Components

### 3.1 TraceRecorder

**File:** `mnemo/telemetry/recorder.py`

The ingestion entry point. Instrumentation facade that agents call during execution.

**Design:**
- Append-only JSONL writer (no in-memory buffering)
- UUID-based episode identification
- Structured event schema with type discrimination
- Configurable log directory routing

**Event emission sequence:**
```
recorder.log_observation(content, context)
recorder.log_memory_read(content, category, score)
recorder.log_reasoning(text, decision, confidence, memory_deps)
recorder.log_action(action_type, input_data, tool)
recorder.log_outcome(success, output, error, metrics)
recorder.log_failure(reason, step_number)
recorder.log_success(final_state)
```

### 3.2 TraceLoader

**File:** `mnemo/telemetry/loader.py`

Event deserialization and structural linking engine.

**Responsibilities:**
- JSONL line-by-line parsing
- Typed event reconstruction via `_parse_event()` discriminator
- Action→Outcome linkage in linear pass
- Episode boundary detection and aggregation

**Parse flow:**
```
Raw JSONL → json.loads(line) → _parse_event() → typed Event object
                                                     ↓
                                             _link_actions_to_outcomes()
                                                     ↓
                                             _build_episodes()
```

### 3.3 BeliefStateTracker

**File:** `mnemo/telemetry/beliefs.py`

Cognitive belief extraction and verification system.

**Algorithm:**
1. Scan trace for belief-indicative keywords (`will`, `should`, `always`, `must`) in `Reasoning` events
2. Extract proposition text as belief identifier
3. Initialize `BeliefState` with confidence from source event
4. Track all subsequent `Action` events as predictions driven by active beliefs
5. Link `Outcome` events back to beliefs — successes reinforce, failures increment contradiction count
6. Score belief reliability as `successes / total_observations`

**BeliefState data structure:**
```
BeliefState {
    belief_id: str
    proposition: str
    confidence: float
    provenance: str (episode_id)
    supporting_episodes: Set[str]
    contradicting_episodes: Set[str]
    predicted_outcomes: List[str]
    observed_outcomes: List[bool]
    contradiction_count: int
}
```

### 3.4 FailureAttributor

**File:** `mnemo/telemetry/attribution.py`

Root cause analysis engine for agent failures.

**Attribution algorithm:**
1. Locate `Failure` event at `failure_index`
2. Define analysis window: `[failure_index - N, failure_index)` where `N = backtrack_steps`
3. Within window, score each event:

   ```
   recency_score = 1.0 / distance_from_failure
   
   if MemoryRead:
       connection_boost = 0.5 if category/content in subsequent reasoning
       final_score = recency_score + connection_boost
   
   if Reasoning:
       final_score = recency_score * 1.5
   ```

4. Normalize scores to percentage scale (0–100)
5. Sort descending, return top-5 contributory factors

### 3.5 ReplayEngine

**File:** `mnemo/telemetry/replay.py`

Counterfactual memory ablation simulator.

**Operation:**
1. Accept target `memory_id` for suppression
2. Walk trace sequentially
3. When `MemoryRead` matches `memory_id`, flag divergence
4. All subsequent `Reasoning` decisions either follow original path or produce `"DIVERGED"`
5. Cascading flag: once a single reasoning step diverges, all future steps automatically diverge
6. Compute divergence metric: `divergent_decisions / total_decisions`

**Output:**
```
ReplayResult {
    original_path: List[str]      — Actual decision sequence
    suppressed_path: List[str]    — Counterfactual decision sequence
    divergence_metric: float      — 0.0 (identical) to 1.0 (fully divergent)
}
```

### 3.6 TraceEnricher

**File:** `mnemo/telemetry/enricher.py`

Semantic enrichment pipeline that adds inferred structure to raw traces.

**Enrichment outputs:**
- **Causal Edges:** Heuristic link from each action to its predecessor (causality_strength: 0.8)
- **Memory Impact Matrix:** For each memory, the set of action indices it influenced, plus an `impact_score = actions_influenced / total_actions`
- **Goal Consistency Score:** Jaccard similarity between consecutive reasoning texts, scaled to `[0.5, 1.0]` range

**EnrichedTrace structure:**
```
EnrichedTrace {
    events: List[Event]
    causal_edges: List[Dict{from, to, causality_strength}]
    memory_impact: List[Dict{memory_id, affected_actions, impact_score}]
    goal_consistency_score: float
}
```

### 3.7 MetricsAggregator

**File:** `mnemo/telemetry/metrics.py`

Population-level statistics engine.

**Computation pipeline:**
1. Glob all `*.jsonl` files in traces directory
2. For each file: load, extract per-trace metrics
3. Aggregate across population

**TraceMetrics (per-trace):**
```
TraceMetrics {
    episode_id: str
    success: bool
    total_steps: int
    memory_read_count: int
    failure_step: int
    contradiction_incidents: int
}
```

**AggregateMetrics (population):**
```
AggregateMetrics {
    total_traces: int
    overall_success_rate: float
    avg_steps_to_success: float
    avg_memory_reads: float
    total_failures: int
    total_contradictions: int
}
```

### 3.8 CLI Inspector

**File:** `mnemo/telemetry/cli.py`

Terminal-based trace visualization tool with ANSI color-coded event rendering.

| Event Type | Color | Identifier |
|---|---|---|
| EpisodeStart | Cyan | `EPISODE_START` |
| Observation | Default | `OBSERVATION` |
| MemoryRead | Blue | `MEMORY_READ` |
| Reasoning | Yellow | `REASONING` |
| Action | Default | `ACTION` |
| Outcome (Success) | Green | `OUTCOME` |
| Outcome (Error) | Red | `OUTCOME` |
| Failure | Red | `FAILURE` |
| Success | Green | `SUCCESS` |

---

## 4. Data Flow — End-to-End

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Agent       │    │  File System │    │  Analysis    │
│  Execution   │───▶│  (JSONL)     │───▶│  Pipeline    │
└──────────────┘    └──────────────┘    └──────────────┘
                                              │
                                   ┌──────────┼──────────┐
                                   ▼          ▼          ▼
                              Attribution  Beliefs   Enrichment
                                   │          │          │
                                   └──────────┼──────────┘
                                              ▼
                                        MetricsAggregator
                                              │
                                              ▼
                                         JSON Report
                                              │
                                              ▼
                                         CLI Viewer
```

---

## 5. Design Decisions

| Decision | Rationale |
|---|---|
| **JSONL over JSON** | Append-friendly, streaming-capable, no reparse overhead |
| **Typed event hierarchy** | Pattern matching via `isinstance()` for clean dispatch |
| **Action-Outcome linking** | Enables O(1) causal chain traversal without index scans |
| **Keyword-based belief extraction** | Lightweight alternative to LLM-based extraction for MVP |
| **Linear replay simulation** | Avoids full cognitive simulation complexity in v1 |
| **Recency-weighted attribution** | Simple but effective proxy for causal proximity |
| **Jaccard goal consistency** | Token-overlap proxy for semantic coherence |
