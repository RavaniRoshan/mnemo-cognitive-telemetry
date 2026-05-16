import os
from mnemo.telemetry.recorder import TraceRecorder
from mnemo.telemetry.loader import TraceLoader, Action, Outcome

def test_loader():
    recorder = TraceRecorder("test_loader_agent", log_dir="test_logs")
    recorder.log_action("db_query", {"query": "SELECT *"}, "sql_tool")
    recorder.log_outcome(True, "results", metrics={"time": 10})
    
    loader = TraceLoader(recorder.filepath)
    events = loader.load()
    
    assert len(events) == 3 # start, action, outcome
    assert isinstance(events[1], Action)
    assert isinstance(events[2], Outcome)
    
    action = events[1]
    assert action.next_outcome is not None
    assert action.next_outcome.success is True
    assert action.next_outcome.output == "results"
    
    episodes = loader.get_episodes()
    assert len(episodes) == 1
    assert episodes[0].agent_name == "test_loader_agent"
    assert len(episodes[0].events) == 3
    print("TraceLoader test passed!")

if __name__ == "__main__":
    test_loader()
