from mnemo.telemetry.loader import MemoryRead, Reasoning
from mnemo.telemetry.replay import ReplayEngine

def test_replay():
    trace = [
        Reasoning(timestamp=1.0, event_type="reasoning", text="Start", decision="init", confidence=1.0, memory_deps=[]),
        MemoryRead(timestamp=2.0, event_type="memory_read", content="User likes PostgreSQL", category="db_pref", score=0.9),
        Reasoning(timestamp=3.0, event_type="reasoning", text="Check DB", decision="use_postgres", confidence=0.8, memory_deps=["db_pref"]),
        Reasoning(timestamp=4.0, event_type="reasoning", text="Deploy", decision="run_deploy", confidence=0.9, memory_deps=[])
    ]
    
    engine = ReplayEngine(trace)
    
    # Suppress unused memory
    res_noop = engine.suppress_memory("cache_pref")
    assert res_noop.divergence_metric == 0.0
    
    # Suppress used memory
    res_diverge = engine.suppress_memory("db_pref")
    print(f"Original: {res_diverge.original_path}")
    print(f"Suppressed: {res_diverge.suppressed_path}")
    print(f"Divergence: {res_diverge.divergence_metric}")
    
    assert res_diverge.divergence_metric > 0.0
    assert "DIVERGED" in res_diverge.suppressed_path

if __name__ == "__main__":
    test_replay()
