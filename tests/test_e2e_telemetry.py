import os
import glob
import json
import unittest
import shutil
from mnemo.test_agents.simple_coder import SimpleCoderAgent
from mnemo.telemetry.loader import TraceLoader
from mnemo.telemetry.attribution import FailureAttributor
from mnemo.telemetry.beliefs import BeliefStateTracker
from mnemo.telemetry.metrics import MetricsAggregator

class TestTelemetryE2E(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        os.makedirs("traces_e2e", exist_ok=True)
        os.makedirs("reports", exist_ok=True)
        os.makedirs("beliefs", exist_ok=True)
        
        # Clear old traces for a clean run
        for f in glob.glob("traces_e2e/*.jsonl"):
            os.remove(f)

    @classmethod
    def tearDownClass(cls):
        # Optional: cleanup. For now, leave to inspect.
        pass

    def test_full_pipeline(self):
        # 1. Record 5 episodes
        agent = SimpleCoderAgent(name="e2e_agent")
        for i in range(5):
            # Force at least one failure to test attribution
            inject_fail = True if i == 0 else False
            agent.run(f"E2E Goal {i}", max_steps=5, inject_failure=inject_fail, use_memory=True)
            
        # Move traces from default 'traces' to 'traces_e2e' to isolate
        for f in glob.glob("traces/e2e_agent_*.jsonl"):
            shutil.move(f, "traces_e2e/")

        traces = glob.glob("traces_e2e/*.jsonl")
        self.assertEqual(len(traces), 5)

        # 2. Analyze & Report loop
        attributor = FailureAttributor()
        
        all_beliefs = []
        
        for trace_file in traces:
            # Load
            loader = TraceLoader(trace_file)
            events = loader.load()
            self.assertTrue(len(events) > 0)
            
            # Attribution (if failed)
            failure_idx = next((i for i, e in enumerate(events) if e.event_type == 'failure'), -1)
            if failure_idx != -1:
                causes = attributor.attribute_failure(events, failure_idx)
                self.assertIsNotNone(causes)
                
            # Beliefs
            tracker = BeliefStateTracker(events)
            extracted = tracker.extract_beliefs()
            all_beliefs.extend(extracted)
            
        # Write beliefs output
        beliefs_out = []
        for b in all_beliefs:
            beliefs_out.append({
                "id": b.belief_id,
                "prop": b.proposition,
                "conf": b.confidence,
                "contradictions": b.contradiction_count
            })
            
        with open("beliefs/extracted.json", "w") as f:
            json.dump(beliefs_out, f)
            
        self.assertTrue(os.path.exists("beliefs/extracted.json"))

        # 3. Metrics Aggregation
        agg = MetricsAggregator("traces_e2e")
        report = agg.export_json("reports/e2e_metrics.json")
        
        self.assertTrue(os.path.exists("reports/e2e_metrics.json"))
        self.assertEqual(report.aggregate.total_traces, 5)
        self.assertTrue(report.aggregate.total_failures >= 1)

if __name__ == "__main__":
    unittest.main()
