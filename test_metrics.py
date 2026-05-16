import json
from mnemo.telemetry.metrics import MetricsAggregator

def test_metrics():
    aggregator = MetricsAggregator("traces")
    report = aggregator.export_json("metrics_report.json")
    
    agg = report.aggregate
    print(f"Total Traces: {agg.total_traces}")
    print(f"Overall Success Rate: {agg.overall_success_rate * 100}%")
    print(f"Average Steps to Success: {agg.avg_steps_to_success}")
    print(f"Average Memory Reads: {agg.avg_memory_reads}")
    print(f"Total Failures: {agg.total_failures}")
    
    assert agg.total_traces > 0
    with open("metrics_report.json", "r") as f:
        data = json.load(f)
        assert "aggregate" in data
        assert "per_trace" in data

if __name__ == "__main__":
    test_metrics()
