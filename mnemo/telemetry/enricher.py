from dataclasses import dataclass
from typing import List, Dict, Any, Set
from mnemo.telemetry.loader import Event, MemoryRead, Reasoning, Action, Observation, Outcome

@dataclass
class EnrichedTrace:
    events: List[Event]
    causal_edges: List[Dict[str, Any]]
    memory_impact: List[Dict[str, Any]]
    goal_consistency_score: float

class TraceEnricher:
    def __init__(self, trace: List[Event]):
        self.trace = trace

    def enrich(self) -> EnrichedTrace:
        causal_edges = []
        memory_impact_map = {} # memory content/category -> set of action indices
        
        last_action_idx = None
        active_memories = set()
        
        # Track goal consistency using reasoning text overlap
        reasoning_texts = []

        for i, event in enumerate(self.trace):
            if isinstance(event, Observation):
                pass
                
            elif isinstance(event, MemoryRead):
                mem_id = event.category or event.content[:20]
                active_memories.add(mem_id)
                if mem_id not in memory_impact_map:
                    memory_impact_map[mem_id] = set()
                    
            elif isinstance(event, Reasoning):
                reasoning_texts.append(event.text.lower())
                
            elif isinstance(event, Action):
                # Causal Edge: heuristic - this action depends on the last action
                if last_action_idx is not None:
                    causal_edges.append({
                        "from": f"step_{last_action_idx}",
                        "to": f"step_{i}",
                        "causality_strength": 0.8 # Simple heuristic
                    })
                
                # Memory Impact: heuristic - active memories influenced this action
                for mem_id in active_memories:
                    memory_impact_map[mem_id].add(i)
                
                last_action_idx = i
                active_memories.clear() # clear after action taken

        # Format Memory Impact
        total_actions = sum(1 for e in self.trace if isinstance(e, Action))
        memory_impact = []
        for mem_id, actions in memory_impact_map.items():
            impact_score = len(actions) / total_actions if total_actions > 0 else 0.0
            memory_impact.append({
                "memory_id": mem_id,
                "affected_actions": [f"step_{a}" for a in actions],
                "impact_score": round(impact_score, 2)
            })

        # Goal Consistency: jaccard similarity of consecutive reasoning steps
        goal_consistency = 1.0
        if len(reasoning_texts) > 1:
            similarities = []
            for j in range(1, len(reasoning_texts)):
                set1 = set(reasoning_texts[j-1].split())
                set2 = set(reasoning_texts[j].split())
                union_len = len(set1 | set2)
                sim = len(set1 & set2) / union_len if union_len > 0 else 0
                similarities.append(sim)
            # Not perfect, but prevents 0 if they just use different words. 
            # We'll use a high baseline + similarity to represent "consistency"
            avg_sim = sum(similarities) / len(similarities)
            goal_consistency = round(0.5 + (avg_sim * 0.5), 2)

        return EnrichedTrace(
            events=self.trace,
            causal_edges=causal_edges,
            memory_impact=memory_impact,
            goal_consistency_score=goal_consistency
        )
