import random
import time
from mnemo.telemetry.recorder import TraceRecorder

class SimpleCoderAgent:
    def __init__(self, name: str = "simple_coder"):
        self.name = name

    def run(self, goal: str, max_steps: int = 10, inject_failure: bool = False, use_memory: bool = True) -> str:
        recorder = TraceRecorder(self.name, log_dir="traces")
        
        recorder.log_observation(f"Received goal: {goal}", {"env": "test"})
        
        memories = []
        if use_memory:
            # Simulate retrieving a relevant memory
            memory_cat = "language_pref"
            memory_content = "Always use Python for scripts"
            recorder.log_memory_read(memory_content, memory_cat, score=0.95)
            memories.append(memory_cat)
            
            recorder.log_reasoning("I will use Python as requested by memory.", "choose_python", confidence=1.0, memory_deps=memories)
            recorder.log_action("create_file", {"filename": "main.py"}, "fs_tool")
            recorder.log_outcome(True, "File created", metrics={"ms": 10})
        else:
            recorder.log_reasoning("I will use default language JS.", "choose_js", confidence=0.7, memory_deps=[])
            recorder.log_action("create_file", {"filename": "index.js"}, "fs_tool")
            recorder.log_outcome(True, "File created", metrics={"ms": 12})
            
        # Simulate working on the goal
        for step in range(1, random.randint(2, max_steps)):
            recorder.log_observation(f"Looking at file step {step}", {})
            
            decision = f"write_code_block_{step}"
            recorder.log_reasoning(f"Need to implement part {step}", decision, confidence=0.8, memory_deps=memories)
            
            action_type = "edit_file"
            recorder.log_action(action_type, {"lines": 5}, "editor_tool")
            
            if inject_failure and step == 3:
                recorder.log_outcome(False, "", error="SyntaxError: invalid syntax", metrics={})
                recorder.log_failure("Encountered syntax error and gave up", step_number=step*2)
                return recorder.filepath
            else:
                recorder.log_outcome(True, "Code written", metrics={"loc": 5})
                
        recorder.log_success({"status": "completed", "files_edited": 1})
        return recorder.filepath

def generate_traces(count: int = 25):
    agent = SimpleCoderAgent()
    print(f"Generating {count} traces...")
    start_time = time.time()
    
    for i in range(count):
        goal = f"Implement feature {i}"
        # Mix of behaviors
        inject_failure = random.random() < 0.2 # 20% fail rate
        use_memory = random.random() < 0.7 # 70% use memory
        
        agent.run(goal, inject_failure=inject_failure, use_memory=use_memory)
        
    duration = time.time() - start_time
    print(f"Generated {count} traces in {duration:.2f} seconds.")

if __name__ == "__main__":
    generate_traces()
