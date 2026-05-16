# Telemetry Subsystem — Module Reference

## Module Dependency Graph

```
recorder.py      (no internal dependencies)
     │
     ▼
    JSONL file
     │
     ▼
loader.py        (no internal dependencies)
     │
     ├────────────┬─────────────┬─────────────┐
     ▼            ▼             ▼             ▼
beliefs.py   replay.py   attribution.py  enricher.py
     │            │             │             │
     └────────────┴─────────────┴─────────────┘
                        │
                        ▼
                  metrics.py
                        │
                        ▼
                   JSON Report
                        │
                        ▼
                    cli.py
```

## Module Reference

| Module | File | Dependencies | Purpose |
|---|---|---|---|
| Loader | `loader.py` | — | Typed event deserialization from JSONL |
| Recorder | `recorder.py` | `uuid`, `json`, `os` | Agent-side trace recording to JSONL |
| Replay | `replay.py` | `loader` | Memory ablation divergence analysis |
| Attribution | `attribution.py` | `loader` | Failure root cause with recency scoring |
| Beliefs | `beliefs.py` | `loader` | Belief state extraction and tracking |
| Enricher | `enricher.py` | `loader` | Causal edges, memory impact, goal consistency |
| Metrics | `metrics.py` | `loader`, `beliefs` | Aggregate statistics across trace population |
| CLI | `cli.py` | `loader` | Terminal-based trace visualization |

## Event Type Catalog

All events defined in `loader.py`, consumed by all analysis modules:

| Event | Fields | Emitted By |
|---|---|---|
| `EpisodeStart` | agent_name, episode_id, start_time | Recorder (constructor) |
| `Observation` | content, context | `log_observation()` |
| `MemoryRead` | content, category, score | `log_memory_read()` |
| `Reasoning` | text, decision, confidence, memory_deps | `log_reasoning()` |
| `Action` | action_type, input, tool | `log_action()` |
| `Outcome` | success, output, error, metrics | `log_outcome()` |
| `Failure` | reason, step_number | `log_failure()` |
| `Success` | final_state | `log_success()` |
