import os
import glob
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from mnemo.telemetry.loader import TraceLoader, Outcome, MemoryRead, Failure, Action
from mnemo.telemetry.beliefs import BeliefStateTracker

@dataclass
class TraceMetrics:
    episode_id: str
    success: bool
    total_steps: int
    memory_read_count: int
    failure_step: int
    contradiction_incidents: int

@dataclass
class AggregateMetrics:
    total_traces: int
    overall_success_rate: float
    avg_steps_to_success: float
    avg_memory_reads: float
    total_failures: int
    total_contradictions: int

@dataclass
class MetricsReport:
    aggregate: AggregateMetrics
    per_trace: List[TraceMetrics]

class MetricsAggregator:
    def __init__(self, traces_dir: str):
        self.traces_dir = traces_dir

    def aggregate(self) -> MetricsReport:
        trace_files = glob.glob(os.path.join(self.traces_dir, "*.jsonl"))
        
        per_trace_metrics = []
        
        for filepath in trace_files:
            loader = TraceLoader(filepath)
            events = loader.load()
            if not events:
                continue
                
            # Extract basic stats
            episode_id = os.path.basename(filepath).replace(".jsonl", "")
            steps = len(events)
            
            memory_reads = sum(1 for e in events if isinstance(e, MemoryRead))
            
            success = False
            for e in reversed(events):
                if isinstance(e, Outcome) and e.success:
                    success = True
                    break
                    
            failure_step = -1
            for i, e in enumerate(events):
                if isinstance(e, Failure):
                    failure_step = e.step_number
                    break
                    
            # Compute contradictions via BeliefStateTracker
            tracker = BeliefStateTracker(events)
            tracker.extract_beliefs()
            contradictions = sum(b.contradiction_count for b in tracker.beliefs.values())
            
            per_trace_metrics.append(TraceMetrics(
                episode_id=episode_id,
                success=success,
                total_steps=steps,
                memory_read_count=memory_reads,
                failure_step=failure_step,
                contradiction_incidents=contradictions
            ))
            
        # Aggregate
        total = len(per_trace_metrics)
        if total == 0:
            agg = AggregateMetrics(0, 0.0, 0.0, 0.0, 0, 0)
            return MetricsReport(agg, [])
            
        successes = [m for m in per_trace_metrics if m.success and m.failure_step == -1]
        overall_success_rate = len(successes) / total
        
        avg_steps = sum(m.total_steps for m in successes) / len(successes) if successes else 0.0
        avg_memory = sum(m.memory_read_count for m in per_trace_metrics) / total
        
        total_failures = sum(1 for m in per_trace_metrics if m.failure_step != -1)
        total_contradictions = sum(m.contradiction_incidents for m in per_trace_metrics)
        
        agg = AggregateMetrics(
            total_traces=total,
            overall_success_rate=round(overall_success_rate, 2),
            avg_steps_to_success=round(avg_steps, 2),
            avg_memory_reads=round(avg_memory, 2),
            total_failures=total_failures,
            total_contradictions=total_contradictions
        )
        
        return MetricsReport(aggregate=agg, per_trace=per_trace_metrics)

    def export_json(self, output_path: str):
        report = self.aggregate()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(report), f, indent=2)
        return report
