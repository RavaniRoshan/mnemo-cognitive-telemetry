from dataclasses import dataclass, field
from typing import List, Dict, Set
from mnemo.telemetry.loader import Event, MemoryRead, Reasoning, Action, Outcome, EpisodeStart

@dataclass
class BeliefState:
    belief_id: str
    proposition: str
    confidence: float
    provenance: str
    supporting_episodes: Set[str] = field(default_factory=set)
    contradicting_episodes: Set[str] = field(default_factory=set)
    predicted_outcomes: List[str] = field(default_factory=list)
    observed_outcomes: List[bool] = field(default_factory=list) # True = Success, False = Failure
    contradiction_count: int = 0

class BeliefStateTracker:
    def __init__(self, trace: List[Event]):
        self.trace = trace
        self.beliefs: Dict[str, BeliefState] = {}
        
    def extract_beliefs(self) -> List[BeliefState]:
        current_episode = "unknown"
        active_beliefs: Set[str] = set()
        last_action = None
        
        belief_keywords = ["will", "should", "always", "must"]
        
        for event in self.trace:
            if isinstance(event, EpisodeStart):
                current_episode = event.episode_id
                active_beliefs.clear()
                last_action = None
                
            elif isinstance(event, MemoryRead):
                prop = event.content.strip()
                bid = prop.lower()
                self._add_or_update_belief(bid, prop, event.score, current_episode)
                active_beliefs.add(bid)
                
            elif isinstance(event, Reasoning):
                text_lower = event.text.lower()
                if any(kw in text_lower for kw in belief_keywords):
                    prop = event.text.strip()
                    bid = prop.lower()
                    self._add_or_update_belief(bid, prop, event.confidence, current_episode)
                    active_beliefs.add(bid)
                    
            elif isinstance(event, Action):
                last_action = event
                # Record predictions (actions taken based on active beliefs)
                for bid in active_beliefs:
                    self.beliefs[bid].predicted_outcomes.append(event.action_type)
                    
            elif isinstance(event, Outcome):
                if last_action:
                    success = event.success
                    for bid in active_beliefs:
                        belief = self.beliefs[bid]
                        belief.observed_outcomes.append(success)
                        if success:
                            belief.supporting_episodes.add(current_episode)
                        else:
                            belief.contradicting_episodes.add(current_episode)
                            belief.contradiction_count += 1
                last_action = None
                
        return list(self.beliefs.values())

    def _add_or_update_belief(self, bid: str, prop: str, confidence: float, episode: str):
        if bid not in self.beliefs:
            self.beliefs[bid] = BeliefState(
                belief_id=bid,
                proposition=prop,
                confidence=confidence,
                provenance=episode,
                supporting_episodes=set([episode])
            )
        else:
            # Update confidence (average or max, let's use max for simplicity)
            self.beliefs[bid].confidence = max(self.beliefs[bid].confidence, confidence)
            self.beliefs[bid].supporting_episodes.add(episode)

    def score_belief(self, belief_id: str) -> float:
        if belief_id not in self.beliefs:
            return 0.0
            
        belief = self.beliefs[belief_id]
        total_obs = len(belief.observed_outcomes)
        if total_obs == 0:
            return belief.confidence # fallback to base confidence
            
        successes = sum(1 for obs in belief.observed_outcomes if obs)
        return successes / total_obs
