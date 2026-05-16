# Mnemo Package Structure

```
mnemo/
├── __init__.py                  # Package root
├── telemetry/                   # Core cognitive telemetry subsystem
│   ├── __init__.py
│   ├── loader.py                # Typed trace deserialization engine
│   ├── recorder.py              # JSONL event recorder
│   ├── replay.py                # Memory ablation & counterfactual simulation
│   ├── attribution.py           # Causal failure root cause analysis
│   ├── beliefs.py               # Belief state extraction & tracking
│   ├── enricher.py              # Semantic trace enrichment (causal edges, impact)
│   ├── metrics.py               # Aggregate metrics computation
│   └── cli.py                   # Terminal-based trace inspector
└── test_agents/                 # Synthetic agent implementations
    ├── __init__.py
    └── simple_coder.py          # Reference agent for trace generation
```
