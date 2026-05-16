from dataclasses import dataclass
from typing import List
from mnemo.telemetry.loader import Event, MemoryRead, Reasoning

@dataclass
class ReplayResult:
    original_path: List[str]
    suppressed_path: List[str]
    divergence_metric: float

class ReplayEngine:
    def __init__(self, trace: List[Event]):
        self.trace = trace

    def suppress_memory(self, memory_id: str) -> ReplayResult:
        original_path = []
        suppressed_path = []
        
        suppressed_active = False
        cascading_divergence = False
        
        for event in self.trace:
            if isinstance(event, MemoryRead):
                # Match by category or content
                if memory_id in event.category or memory_id in event.content:
                    suppressed_active = True
                    
            elif isinstance(event, Reasoning):
                original_path.append(event.decision)
                
                depends_on_suppressed = any(memory_id in str(dep) for dep in event.memory_deps)
                
                if cascading_divergence:
                    suppressed_path.append("DIVERGED")
                elif suppressed_active and depends_on_suppressed:
                    suppressed_path.append("DIVERGED")
                    cascading_divergence = True  # Subsequent actions cascade
                else:
                    suppressed_path.append(event.decision)
                    
        if not original_path:
            metric = 0.0
        else:
            diff_count = sum(1 for o, s in zip(original_path, suppressed_path) if o != s)
            metric = diff_count / len(original_path)
            
        return ReplayResult(
            original_path=original_path, 
            suppressed_path=suppressed_path, 
            divergence_metric=round(metric, 2)
        )
