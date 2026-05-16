from mnemo.telemetry.loader import MemoryRead, Reasoning, Failure, Action
from mnemo.telemetry.attribution import FailureAttributor

def test_attributor():
    # Fake trace
    trace = [
        MemoryRead(timestamp=1.0, event_type="memory_read", content="Bad old config", category="config", score=0.9),
        Action(timestamp=2.0, event_type="action", action_type="read_file", input={}, tool="fs"),
        Reasoning(timestamp=3.0, event_type="reasoning", text="using config", decision="deploy", confidence=0.8, memory_deps=["config"]),
        Action(timestamp=4.0, event_type="action", action_type="deploy", input={}, tool="kube"),
        Failure(timestamp=5.0, event_type="failure", reason="Crash", step_number=4)
    ]
    
    attr = FailureAttributor(backtrack_steps=5)
    causes = attr.attribute_failure(trace, failure_index=4)
    
    print("Failure Causes:")
    for desc, score in causes:
        print(f"- {desc}: {score}%")
        
    assert len(causes) > 0
    assert "Reasoning" in causes[0][0] or "MemoryRead" in causes[0][0]

if __name__ == "__main__":
    test_attributor()
