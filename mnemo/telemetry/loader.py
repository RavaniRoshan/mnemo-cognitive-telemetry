import json
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class Event:
    timestamp: float
    event_type: str

@dataclass
class EpisodeStart(Event):
    agent_name: str
    episode_id: str
    start_time: str

@dataclass
class Observation(Event):
    content: str
    context: Dict[str, Any]

@dataclass
class Outcome(Event):
    success: bool
    output: str
    error: Optional[str]
    metrics: Dict[str, Any]

@dataclass
class Action(Event):
    action_type: str
    input: Dict[str, Any]
    tool: str
    next_outcome: Optional[Outcome] = None

@dataclass
class MemoryRead(Event):
    content: str
    category: str
    score: float

@dataclass
class Reasoning(Event):
    text: str
    decision: str
    confidence: float
    memory_deps: list

@dataclass
class Failure(Event):
    reason: str
    step_number: int

@dataclass
class Success(Event):
    final_state: Dict[str, Any]

@dataclass
class Episode:
    agent_name: str
    episode_id: str
    start_time: str
    events: List[Event]

class TraceLoader:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._events: List[Event] = []
        self._episodes: List[Episode] = []

    def load(self) -> List[Event]:
        return self.load_trace(self.filepath)

    def load_trace(self, filepath: str = None) -> List[Event]:
        target_path = filepath or self.filepath
        events = []
        with open(target_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                raw = json.loads(line)
                events.append(self._parse_event(raw))
        
        self._events = events
        self._link_actions_to_outcomes(events)
        self._build_episodes(events)
        return self._events

    def _parse_event(self, raw: dict) -> Event:
        ts = raw.get('timestamp', 0.0)
        etype = raw.get('event_type', 'unknown')
        data = raw.get('data', {})
        
        if etype == 'episode_start':
            return EpisodeStart(ts, etype, data.get('agent_name', ''), data.get('episode_id', ''), data.get('start_time', ''))
        elif etype == 'observation':
            return Observation(ts, etype, data.get('content', ''), data.get('context', {}))
        elif etype == 'action':
            return Action(ts, etype, data.get('action_type', ''), data.get('input', {}), data.get('tool', ''))
        elif etype == 'outcome':
            return Outcome(ts, etype, data.get('success', False), data.get('output', ''), data.get('error'), data.get('metrics', {}))
        elif etype == 'memory_read':
            return MemoryRead(ts, etype, data.get('content', ''), data.get('category', ''), data.get('score', 0.0))
        elif etype == 'reasoning':
            return Reasoning(ts, etype, data.get('text', ''), data.get('decision', ''), data.get('confidence', 0.0), data.get('memory_deps', []))
        elif etype == 'failure':
            return Failure(ts, etype, data.get('reason', ''), data.get('step_number', 0))
        elif etype == 'success':
            return Success(ts, etype, data.get('final_state', {}))
        else:
            return Event(ts, etype)

    def _link_actions_to_outcomes(self, events: List[Event]):
        last_action = None
        for event in events:
            if isinstance(event, Action):
                last_action = event
            elif isinstance(event, Outcome) and last_action:
                last_action.next_outcome = event
                last_action = None

    def _build_episodes(self, events: List[Event]):
        current_episode = None
        episodes = []
        for event in events:
            if isinstance(event, EpisodeStart):
                if current_episode:
                    episodes.append(current_episode)
                current_episode = Episode(
                    agent_name=event.agent_name,
                    episode_id=event.episode_id,
                    start_time=event.start_time,
                    events=[event]
                )
            elif current_episode:
                current_episode.events.append(event)
        
        if current_episode:
            episodes.append(current_episode)
            
        self._episodes = episodes

    def get_episodes(self) -> List[Episode]:
        return self._episodes
