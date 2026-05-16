from typing import List, Tuple
from mnemo.telemetry.loader import Event, MemoryRead, Reasoning, Failure

class FailureAttributor:
    def __init__(self, backtrack_steps: int = 10):
        self.backtrack_steps = backtrack_steps

    def attribute_failure(self, trace: List[Event], failure_index: int) -> List[Tuple[str, float]]:
        if failure_index < 0 or failure_index >= len(trace):
            return []
            
        failure_event = trace[failure_index]
        if not isinstance(failure_event, Failure):
            return []

        start_idx = max(0, failure_index - self.backtrack_steps)
        window = trace[start_idx:failure_index]
        
        causes = []
        
        # Collect reasoning steps in window to check memory connections
        reasoning_deps = []
        for event in window:
            if isinstance(event, Reasoning):
                reasoning_deps.extend(event.memory_deps)
                
        for i, event in enumerate(window):
            step_idx = start_idx + i
            distance = failure_index - step_idx
            
            # Recency score: 1.0 for immediate previous, 0.1 for 10 steps back
            recency_score = 1.0 / distance
            
            if isinstance(event, MemoryRead):
                # Connection score: boost if memory was used in subsequent reasoning
                # We assume memory_deps contains categories or content snippets for simplicity
                connection_boost = 0.0
                for dep in reasoning_deps:
                    if dep in event.category or dep in event.content:
                        connection_boost = 0.5
                        break
                        
                final_score = recency_score + connection_boost
                causes.append((f"MemoryRead(step_{step_idx}, cat={event.category})", final_score))
                
            elif isinstance(event, Reasoning):
                # Reasoning directly preceding action has high connection to failure
                final_score = recency_score * 1.5 
                causes.append((f"Reasoning(step_{step_idx}, dec={event.decision[:20]})", final_score))

        # Normalize and sort
        if causes:
            max_score = max(score for _, score in causes)
            if max_score > 0:
                causes = [(desc, round((score / max_score) * 100, 1)) for desc, score in causes]
        
        causes.sort(key=lambda x: x[1], reverse=True)
        return causes[:5]
