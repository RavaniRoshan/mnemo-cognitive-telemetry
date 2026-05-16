from mnemo.telemetry.loader import MemoryRead, Reasoning, Action, Outcome, Observation
from mnemo.telemetry.enricher import TraceEnricher

def test_enricher():
    trace = [
        MemoryRead(timestamp=1.0, event_type="memory_read", content="DB is Postgres", category="db", score=1.0),
        Reasoning(timestamp=2.0, event_type="reasoning", text="Deploying database", decision="deploy", confidence=1.0, memory_deps=["db"]),
        Action(timestamp=3.0, event_type="action", action_type="deploy_db", input={}, tool="kube"),
        Outcome(timestamp=4.0, event_type="outcome", success=True, output="ok", error=None, metrics={}),
        Observation(timestamp=5.0, event_type="observation", content="DB is up", context={}),
        Reasoning(timestamp=6.0, event_type="reasoning", text="Deploying app to database", decision="deploy_app", confidence=1.0, memory_deps=[]),
        Action(timestamp=7.0, event_type="action", action_type="deploy_app", input={}, tool="kube")
    ]

    enricher = TraceEnricher(trace)
    enriched = enricher.enrich()

    print(f"Goal Consistency: {enriched.goal_consistency_score}")
    print(f"Causal Edges: {enriched.causal_edges}")
    print(f"Memory Impact: {enriched.memory_impact}")

    assert len(enriched.causal_edges) == 1
    assert enriched.causal_edges[0]["from"] == "step_2"
    assert enriched.causal_edges[0]["to"] == "step_6"
    
    assert len(enriched.memory_impact) == 1
    assert enriched.memory_impact[0]["memory_id"] == "db"
    assert "step_2" in enriched.memory_impact[0]["affected_actions"]
    assert enriched.memory_impact[0]["impact_score"] == 0.5 # 1 out of 2 actions

if __name__ == "__main__":
    test_enricher()
