# Test Agents

Reference agent implementations used for trace generation and integration testing.

## SimpleCoderAgent

A minimal agent that simulates a coding workflow with memory-augmented decision making.

**Behavior:**
- Retrieves a memory (`"Always use Python for scripts"`) influencing language choice
- Generates code files through simulated edit operations
- Supports configurable failure injection (20% default failure rate)
- Supports configurable memory utilization (70% default)

**Trace generation:**
```bash
# Generate 25 random agent traces
python -m mnemo.test_agents.simple_coder

# Generated traces written to ./traces/simple_coder_*.jsonl
```

**Designed for testing:**
- Trace recording pipeline
- Belief extraction (memory preference → belief)
- Failure attribution (injected syntax errors)
- Metrics aggregation (mixed success/failure population)
