# Contributing to Mnemo

We welcome contributions across the entire cognitive observability stack.

## Areas of Contribution

### Core Framework
- Trace instrumentation APIs
- Event schema extensions
- New analysis modules
- Performance optimization

### Analysis Modules
- Alternative belief extraction strategies
- Advanced failure attribution algorithms
- Memory graph construction
- Causal inference pipelines

### Integrations
- Agent framework adapters (LangChain, AutoGPT, etc.)
- Export targets (OpenTelemetry, Prometheus, DataDog)
- Visualization backends

### Documentation & Testing
- Architecture documentation
- Integration test scenarios
- Benchmark datasets
- Usage examples

## Development Workflow

```bash
# Clone and install
git clone https://github.com/RavaniRoshan/menimo-model.git
cd menimo-model

# Run tests
python -m pytest test_*.py tests/ -v

# Generate traces for manual testing
python -m mnemo.test_agents.simple_coder

# Inspect generated traces
python -m mnemo.telemetry.cli traces/simple_coder_*.jsonl

# Generate metrics report
python -c "
from mnemo.telemetry.metrics import MetricsAggregator
agg = MetricsAggregator('traces')
report = agg.export_json('metrics_report.json')
"
```

## Pull Request Guidelines

1. Include tests for new functionality
2. Maintain backward compatibility with existing trace schemas
3. Add type annotations to all public interfaces
4. Update relevant documentation
5. Run the full test suite before submitting

## Code Style

- Follow PEP 8
- Type annotations required for all function signatures
- Dataclasses preferred for data structures
- Pure functions preferred for analysis logic

## Questions?

Open a discussion or issue on GitHub.
