import json
import time
import uuid
import os
from datetime import datetime

class TraceRecorder:
    def __init__(self, agent_name: str, log_dir: str = "logs"):
        self.agent_name = agent_name
        self.episode_id = str(uuid.uuid4())
        self.start_time = datetime.utcnow().isoformat()
        
        os.makedirs(log_dir, exist_ok=True)
        self.filepath = os.path.join(log_dir, f"{self.agent_name}_{self.episode_id}.jsonl")
        
        self._write("episode_start", {
            "agent_name": self.agent_name, 
            "episode_id": self.episode_id, 
            "start_time": self.start_time
        })

    def _write(self, event_type: str, data: dict):
        event = {
            "timestamp": time.time(),
            "event_type": event_type,
            "data": data
        }
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event) + '\n')

    def log_observation(self, content: str, context: dict):
        self._write("observation", {"content": content, "context": context})

    def log_action(self, action_type: str, input_data: dict, tool: str):
        self._write("action", {"action_type": action_type, "input": input_data, "tool": tool})

    def log_outcome(self, success: bool, output: str, error: str = None, metrics: dict = None):
        self._write("outcome", {"success": success, "output": output, "error": error, "metrics": metrics or {}})

    def log_memory_read(self, content: str, category: str, score: float):
        self._write("memory_read", {"content": content, "category": category, "score": score})

    def log_reasoning(self, text: str, decision: str, confidence: float, memory_deps: list):
        self._write("reasoning", {"text": text, "decision": decision, "confidence": confidence, "memory_deps": memory_deps})

    def log_failure(self, reason: str, step_number: int):
        self._write("failure", {"reason": reason, "step_number": step_number})

    def log_success(self, final_state: dict):
        self._write("success", {"final_state": final_state})
