import argparse
import os
from datetime import datetime
from mnemo.telemetry.loader import (
    TraceLoader, Event, EpisodeStart, Observation, 
    Action, Outcome, MemoryRead, Reasoning, Failure, Success
)

# ANSI Colors
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

def format_time(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime('%H:%M:%S.%f')[:-3]

def inspect_trace(filepath: str):
    loader = TraceLoader(filepath)
    events = loader.load()
    
    print(f"{CYAN}=== Trace Inspection: {filepath} ==={RESET}\n")
    
    for i, event in enumerate(events):
        ts_str = format_time(event.timestamp)
        step = f"[{i:04d}]"
        
        if isinstance(event, EpisodeStart):
            print(f"{step} [{ts_str}] {CYAN}[EPISODE_START]{RESET} Agent: {event.agent_name} | ID: {event.episode_id}")
            
        elif isinstance(event, Observation):
            content_preview = event.content[:60] + ('...' if len(event.content) > 60 else '')
            print(f"{step} [{ts_str}] [OBSERVATION]   {content_preview}")
            
        elif isinstance(event, Action):
            tool = event.tool
            action = event.action_type
            print(f"{step} [{ts_str}] [ACTION]        Tool: {tool} | Action: {action}")
            
        elif isinstance(event, Outcome):
            color = GREEN if event.success else RED
            status = "SUCCESS" if event.success else "ERROR"
            output_preview = event.output[:50] + ('...' if len(event.output) > 50 else '')
            print(f"{step} [{ts_str}] {color}[OUTCOME]{RESET}       {status} | {output_preview}")
            
        elif isinstance(event, MemoryRead):
            content_preview = event.content[:50] + ('...' if len(event.content) > 50 else '')
            print(f"{step} [{ts_str}] {BLUE}[MEMORY_READ]{RESET}   Score: {event.score:.2f} | {content_preview}")
            
        elif isinstance(event, Reasoning):
            decision = event.decision[:50] + ('...' if len(event.decision) > 50 else '')
            print(f"{step} [{ts_str}] {YELLOW}[REASONING]{RESET}     Conf: {event.confidence:.2f} | Dec: {decision}")
            
        elif isinstance(event, Failure):
            reason_preview = event.reason[:60] + ('...' if len(event.reason) > 60 else '')
            print(f"{step} [{ts_str}] {RED}[FAILURE]{RESET}       Step: {event.step_number} | {reason_preview}")
            
        elif isinstance(event, Success):
            print(f"{step} [{ts_str}] {GREEN}[SUCCESS]{RESET}       Final state captured.")
            
        else:
            print(f"{step} [{ts_str}] [{event.event_type.upper()}]")

def main():
    parser = argparse.ArgumentParser(description="Inspect MOSA trace files.")
    parser.add_argument("filepath", help="Path to the .jsonl trace file")
    args = parser.parse_args()
    
    if not os.path.exists(args.filepath):
        print(f"{RED}Error: File {args.filepath} not found.{RESET}")
        return
        
    inspect_trace(args.filepath)

if __name__ == "__main__":
    main()
