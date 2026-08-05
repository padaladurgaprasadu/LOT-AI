"""
LOT AI Production Performance Monitor Module.

This module tracks engine latency, token efficiency, and API rate limits.
Provides real-time performance snapshots and bottleneck identification.
"""
import time
import threading
from collections import defaultdict, deque
from typing import Dict, List

from backend.utils.logger import get_logger

logger = get_logger(__name__)

def inject_performance_prompt(system_prompt: str) -> str:
    """
    Injects performance-related instructions into the system prompt.
    """
    perf_instructions = (
        "\n\n[System Performance Directive]\n"
        "Ensure your responses are concise and optimized for fast processing. "
        "Avoid unnecessary verbosity to minimize token usage and latency."
    )
    return system_prompt + perf_instructions

class PerformanceMonitor:
    """Singleton performance monitor for LOT AI."""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(PerformanceMonitor, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        with self._lock:
            if not getattr(self, '_initialized', False):
                self._latencies: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
                self._token_usage: Dict[str, Dict[str, float]] = defaultdict(
                    lambda: {"input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0}
                )
                self._api_calls: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))
                # Configurable API limits per minute
                self._api_limits: Dict[str, int] = {"openai": 500, "anthropic": 500, "gemini": 500} 
                self._initialized = True
                logger.info("PerformanceMonitor initialized.")

    def record_latency(self, engine_name: str, latency_ms: float) -> None:
        """Records latency for a specific engine."""
        with self._lock:
            self._latencies[engine_name].append(latency_ms)
            logger.debug(f"Recorded latency for {engine_name}: {latency_ms}ms")

    def record_token_usage(self, engine_name: str, input_tokens: int, output_tokens: int, cost_usd: float) -> None:
        """Records token usage and cost for a specific engine."""
        with self._lock:
            usage = self._token_usage[engine_name]
            usage["input_tokens"] += input_tokens
            usage["output_tokens"] += output_tokens
            usage["cost_usd"] += cost_usd
            logger.debug(f"Recorded token usage for {engine_name}: +{input_tokens} in, +{output_tokens} out, +${cost_usd:.4f}")

    def record_api_call(self, provider: str) -> None:
        """Records an API call and checks against rate limits (throttle if >90%)."""
        now = time.time()
        with self._lock:
            calls = self._api_calls[provider]
            # Remove calls older than 60 seconds
            while calls and now - calls[0] > 60:
                calls.popleft()
            
            calls.append(now)
            
            call_count = len(calls)
            limit = self._api_limits.get(provider, 1000)
            
            if call_count > limit * 0.9:
                logger.warning(
                    f"API rate limit approaching for {provider}: {call_count}/{limit} calls per minute. "
                    "Auto-throttling active."
                )
                # Auto-throttle by sleeping slightly to ease load
                time.sleep(0.5)

    def get_dashboard(self) -> dict:
        """Returns a comprehensive performance snapshot."""
        now = time.time()
        dashboard = {
            "engines": {},
            "totals": {
                "input_tokens": 0,
                "output_tokens": 0,
                "cost_usd": 0.0
            },
            "api_health": {}
        }
        
        with self._lock:
            # Aggregate engine stats
            for engine, latencies in self._latencies.items():
                lats = list(latencies)
                if not lats:
                    continue
                
                avg_lat = sum(lats) / len(lats)
                sorted_lats = sorted(lats)
                # Ensure we have at least one latency reading for p95
                idx = int(len(sorted_lats) * 0.95)
                # Cap the index to the length of the list minus one
                idx = min(idx, len(sorted_lats) - 1)
                p95_lat = sorted_lats[idx]
                
                # Arbitrary threshold for healthy vs degraded (e.g., 2000ms)
                health = "Healthy" if avg_lat < 2000 else "Degraded"
                
                dashboard["engines"][engine] = {
                    "avg_latency_ms": avg_lat,
                    "p95_latency_ms": p95_lat,
                    "health": health
                }
            
            # Aggregate token stats
            for engine, usage in self._token_usage.items():
                dashboard["totals"]["input_tokens"] += usage["input_tokens"]
                dashboard["totals"]["output_tokens"] += usage["output_tokens"]
                dashboard["totals"]["cost_usd"] += usage["cost_usd"]
                
            # Aggregate API stats
            for provider, calls in self._api_calls.items():
                # Cleanup old calls
                while calls and now - calls[0] > 60:
                    calls.popleft()
                
                cpm = len(calls)
                limit = self._api_limits.get(provider, 1000)
                status = "Warning" if cpm > limit * 0.9 else "OK"
                
                dashboard["api_health"][provider] = {
                    "calls_per_minute": cpm,
                    "limit_per_minute": limit,
                    "status": status
                }
                
        return dashboard

    def get_bottleneck_report(self) -> list:
        """Identifies and returns the slowest engines sorted by average latency."""
        bottlenecks = []
        with self._lock:
            for engine, latencies in self._latencies.items():
                lats = list(latencies)
                if not lats:
                    continue
                avg_lat = sum(lats) / len(lats)
                bottlenecks.append({
                    "engine": engine,
                    "avg_latency_ms": avg_lat
                })
        
        # Sort so highest latency is first
        bottlenecks.sort(key=lambda x: x["avg_latency_ms"], reverse=True)
        return bottlenecks
