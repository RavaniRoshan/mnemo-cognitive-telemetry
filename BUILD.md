# Build & Purpose

## What This Is

A Python framework that records, inspects, and analyzes how AI agents think and make decisions — especially when they use memory.

Think of it as a flight recorder for AI agents.

## Quick Start

```bash
# Requirements: Python 3.9+
# No external dependencies needed — pure Python standard library

# 1. Generate sample agent traces
python -m mnemo.test_agents.simple_coder

# 2. Inspect a trace file
python -m mnemo.telemetry.cli traces/simple_coder_*.jsonl

# 3. Run tests
python -m pytest test_*.py tests/ -v

# 4. Generate a metrics report
python -c "
from mnemo.telemetry.metrics import MetricsAggregator
agg = MetricsAggregator('traces')
report = agg.export_json('metrics_report.json')
print(f'Success rate: {report.aggregate.overall_success_rate}')
"
```

## What It Does

| Feature | What it answers |
|---|---|
| Trace recording | What did the agent see, think, and do? |
| Failure attribution | Why did the agent fail? Which memory or reasoning step caused it? |
| Belief tracking | What does the agent believe? Are those beliefs consistent? |
| Memory replay | What happens if you remove a specific memory from the agent? |
| Metrics | Across many runs, how often does the agent succeed? |

## File Layout

```
mnemo/telemetry/     ← the framework code
traces/              ← agent trace data (JSONL)
test_*.py            ← unit tests
tests/               ← integration tests
```

## No Dependencies

Zero pip installs. Uses only Python standard library (`json`, `uuid`, `os`, `argparse`, `datetime`, `glob`).
