# Mnemo — Cognitive Observability Infrastructure for LLM Agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Agent Telemetry](https://img.shields.io/badge/domain-agent--telemetry-brightgreen)](#)
[![Research Stage](https://img.shields.io/badge/status-research--prototype-orange)](#)

**Mnemo** is a first-of-its-kind **cognitive observability and telemetry framework** purpose-built for memory-augmented LLM agents. It provides deep instrumentation, trace analysis, failure attribution, belief tracking, and replay simulation for persistent agent cognition systems.

> **From stateless prompt chaining → observable, memory-aware cognitive architecture.**

---

## Why Mnemo?

Existing agent frameworks treat LLMs as stateless sequence predictors with ad-hoc logging. **Mnemo changes that.**

| Problem | Mnemo Solution |
|---|---|
| Agent decisions are opaque black boxes | Full **typed event trace** with causal edge inference |
| Memory influence is unmeasurable | **Memory impact scoring** per decision step |
| Failures are logged but not diagnosed | **Causal failure attribution** with recency-weighted backtracking |
| Agent "beliefs" drift silently | **Belief state tracking** with contradiction detection |
| Memory ablation effects are unknown | **Replay engine** with divergence metrics |
| No standardized telemetry format | **Unified cognitive trace schema** (8 event types) |

---

## Core Capabilities

### 🧬 Cognitive Trace Architecture

A strongly-typed event schema capturing the full agent cognition lifecycle:

```
EpisodeStart → Observation → MemoryRead → Reasoning → Action → Outcome
                                                                    ↓
                                                            Failure / Success
```

Eight canonical event types instrument every atomic cognitive operation — from environmental observation through memory retrieval, reasoning, action execution, and outcome evaluation.

### 🔍 Failure Attribution Engine

When an agent fails, Mnemo backtracks through the cognitive trace to identify root causes:

- **Recency-weighted scoring** — temporally proximate events receive higher attribution weight
- **Memory dependency linking** — connects failure events to the specific memory retrievals and reasoning steps that preceded them
- **Normalized causation ranking** — returns the top-K contributory factors with percentage confidence scores

### 🧠 Belief State Tracker

Extracts and tracks agent belief states across episodes:

- **Keyword-aware proposition extraction** — identifies declarative beliefs from reasoning text
- **Outcome-based reinforcement** — beliefs are strengthened or contradicted by subsequent action outcomes
- **Confidence scoring** — dynamic belief confidence derived from empirical success ratios
- **Contradiction monitoring** — tracks when agent actions contradict stated beliefs

### 🔄 Memory Replay & Ablation Analysis

Simulate counterfactual scenarios by suppressing specific memories:

- **Divergence metric computation** — quantifies decision path changes when memories are ablated
- **Cascading divergence detection** — identifies when a single suppressed memory causes downstream decision cascades
- **Comparative trace visualization** — original vs. suppressed decision paths side-by-side

### 📊 Aggregate Metrics & Observability

End-to-end trace aggregation for population-level insights:

| Metric | Description |
|---|---|
| Success Rate | Overall agent task completion ratio |
| Memory Utilization | Memory read frequency across episodes |
| Contradiction Incidence | Belief contradiction events per trace |
| Failure Distribution | Failure step distribution across episodes |
| Goal Consistency Score | Semantic coherence of reasoning across steps |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Mnemo Framework                          │
├─────────────┬───────────────┬──────────────┬────────────────┤
│  Recorder   │   Loader      │   Analyzers  │   Reporting    │
│  (JSONL     │  (Typed       │  ┌─────────┐ │  (Aggregator,  │
│   ingestion)│   deserialize)│  │Beliefs  │ │   CLI, JSON    │
│             │               │  │Attrib.  │ │   export)      │
│             │               │  │Enricher │ │                │
│             │               │  │Replay   │ │                │
│             │               │  └─────────┘ │                │
└─────────────┴───────────────┴──────────────┴────────────────┘
```

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/RavaniRoshan/menimo-model.git
cd menimo-model

# Generate sample agent traces
python -m mnemo.test_agents.simple_coder

# Inspect a trace
python -m mnemo.telemetry.cli traces/simple_coder_*.jsonl

# Run the full test suite
python -m pytest test_*.py tests/ -v

# Generate aggregate metrics report
python -c "
from mnemo.telemetry.metrics import MetricsAggregator
agg = MetricsAggregator('traces')
report = agg.export_json('metrics_report.json')
print(f'Success rate: {report.aggregate.overall_success_rate}')
"
```

---

## Project Structure

```
mnemo-model/
├── mnemo/                          # Core framework
│   ├── telemetry/                  # Cognitive telemetry subsystem
│   │   ├── loader.py               # Typed trace deserialization
│   │   ├── recorder.py             # JSONL trace recorder
│   │   ├── replay.py               # Memory ablation replay engine
│   │   ├── attribution.py          # Causal failure attribution
│   │   ├── beliefs.py              # Belief state tracking
│   │   ├── enricher.py             # Trace enrichment & causal edges
│   │   ├── metrics.py              # Aggregate metrics computation
│   │   └── cli.py                  # Interactive trace inspector
│   └── test_agents/                # Synthetic agent implementations
│       └── simple_coder.py         # Reference agent for trace generation
├── tests/                          # Integration & end-to-end tests
├── traces/                         # Generated agent trace data
├── reports/                        # Metrics export artifacts
├── beliefs/                        # Extracted belief state dumps
├── agent.md                        # MOSA system specification
└── GEMINI.md                       # Gemini integration notes
```

---

## Use Cases

- **Agent Framework Developers** — instrument your agents with standardized cognitive telemetry
- **AI Observability Engineers** — build dashboards on top of Mnemo's trace and metrics pipelines
- **LLM Researchers** — study memory influence patterns, belief drift, and failure modes
- **Agent Infrastructure Teams** — integrate Mnemo as the observability layer in production agent deployments

---

## License

MIT

---

## Citation

```bibtex
@software{mnemo2024,
  author = {RavaniRoshan},
  title = {Mnemo: Cognitive Observability Infrastructure for LLM Agents},
  year = {2024},
  url = {https://github.com/RavaniRoshan/menimo-model}
}
```
