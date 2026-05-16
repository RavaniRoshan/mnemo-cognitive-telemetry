# Test Suite

## Test Files

| File | Type | Coverage |
|---|---|---|
| `tests/test_e2e_telemetry.py` | Integration | End-to-end recording→loading→analysis→metrics pipeline |
| `test_loader.py` | Unit | Trace deserialization, event typing, episode segmentation |
| `test_recorder.py` | Unit | Event recording, file I/O, schema conformance |
| `test_replay.py` | Unit | Memory ablation, divergence computation |
| `test_attribution.py` | Unit | Failure backtracking, scoring, result ordering |
| `test_beliefs.py` | Unit | Belief extraction, confidence scoring, contradiction tracking |
| `test_enricher.py` | Unit | Causal edges, memory impact, goal consistency |
| `test_metrics.py` | Unit | Per-trace metrics, aggregation, JSON export |

## Running Tests

```bash
# Full suite
python -m pytest test_*.py tests/ -v

# Specific module
python -m pytest test_beliefs.py -v --tb=short

# With coverage
python -m pytest test_*.py tests/ --cov=mnemo.telemetry -v
```

## Test Data

- `traces/` — Generated agent traces (used by unit tests)
- `traces_e2e/` — End-to-end test traces
- `test_logs/` — Loader-specific test fixtures
- `reports/` — Expected metrics output artifacts
