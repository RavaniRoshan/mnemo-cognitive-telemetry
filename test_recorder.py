import time
from mnemo.telemetry.recorder import TraceRecorder

def test_speed():
    recorder = TraceRecorder("test_agent")
    start = time.time()
    for i in range(1000):
        recorder.log_observation("test content", {"iteration": i})
    end = time.time()
    print(f"1000 events in {end - start:.4f} seconds")

if __name__ == "__main__":
    test_speed()
