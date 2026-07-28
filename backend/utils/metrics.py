import time
from typing import Dict, Any

class TelemetryTracker:
    """
    yAI Phase 15 Observability Engine.
    Tracks highly granular latency metrics across the request lifecycle.
    """
    def __init__(self):
        self.start_time = time.time()
        self.checkpoints: Dict[str, float] = {}
        self.metrics: Dict[str, float] = {}

    def mark(self, event_name: str):
        """Records a timestamp for a specific event."""
        self.checkpoints[event_name] = time.time()

    def record_delta(self, metric_name: str, start_event: str, end_event: str = None):
        """Computes and stores the latency between two recorded events in ms."""
        start = self.checkpoints.get(start_event, self.start_time)
        end = self.checkpoints.get(end_event, time.time()) if end_event else time.time()
        
        delta_ms = (end - start) * 1000
        self.metrics[metric_name] = round(delta_ms, 2)
        return self.metrics[metric_name]

    def record_duration(self, metric_name: str, duration_sec: float):
        """Directly record a duration."""
        self.metrics[metric_name] = round(duration_sec * 1000, 2)

    def get_metrics(self) -> Dict[str, Any]:
        """Returns the compiled metrics payload."""
        total_time = (time.time() - self.start_time) * 1000
        self.metrics["total_latency"] = round(total_time, 2)
        return self.metrics
