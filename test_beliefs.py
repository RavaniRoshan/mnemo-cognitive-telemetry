from mnemo.telemetry.loader import EpisodeStart, MemoryRead, Reasoning, Action, Outcome
from mnemo.telemetry.beliefs import BeliefStateTracker

def test_beliefs():
    trace = [
        EpisodeStart(timestamp=1.0, event_type="episode_start", agent_name="agent", episode_id="ep1", start_time="now"),
        MemoryRead(timestamp=2.0, event_type="memory_read", content="User prefers fast api", category="pref", score=0.9),
        Reasoning(timestamp=3.0, event_type="reasoning", text="We must use fast api", decision="deploy", confidence=0.8, memory_deps=[]),
        Action(timestamp=4.0, event_type="action", action_type="deploy_fastapi", input={}, tool="kubectl"),
        Outcome(timestamp=5.0, event_type="outcome", success=True, output="ok", error=None, metrics={}),
        
        EpisodeStart(timestamp=6.0, event_type="episode_start", agent_name="agent", episode_id="ep2", start_time="later"),
        MemoryRead(timestamp=7.0, event_type="memory_read", content="User prefers fast api", category="pref", score=0.9),
        Reasoning(timestamp=8.0, event_type="reasoning", text="We should use fast api", decision="deploy", confidence=0.8, memory_deps=[]),
        Action(timestamp=9.0, event_type="action", action_type="deploy_fastapi", input={}, tool="kubectl"),
        Outcome(timestamp=10.0, event_type="outcome", success=False, output="fail", error="crash", metrics={})
    ]
    
    tracker = BeliefStateTracker(trace)
    beliefs = tracker.extract_beliefs()
    
    print(f"Extracted {len(beliefs)} beliefs.")
    for b in beliefs:
        score = tracker.score_belief(b.belief_id)
        print(f"Belief: '{b.proposition}' | Score: {score:.2f} | Obs: {b.observed_outcomes} | Contradictions: {b.contradiction_count}")
        
    assert len(beliefs) >= 2
    
    # "user prefers fast api" was observed twice: 1 success, 1 failure -> score 0.5
    pref_score = tracker.score_belief("user prefers fast api")
    assert pref_score == 0.5

if __name__ == "__main__":
    test_beliefs()
