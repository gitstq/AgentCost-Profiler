"""
Core profiler module for AgentCost-Profiler.

Provides comprehensive performance profiling capabilities for AI Agents,
including execution time tracking, resource usage monitoring, and
bottleneck identification.
"""

import time
import asyncio
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from contextlib import contextmanager
from collections import defaultdict


@dataclass
class ProfileResult:
    """Result container for profiling data."""
    name: str
    start_time: float
    end_time: float
    duration_ms: float
    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": self.duration_ms,
            "cpu_percent": self.cpu_percent,
            "memory_mb": self.memory_mb,
            "metadata": self.metadata
        }


class AgentProfiler:
    """
    Main profiler class for AI Agent performance analysis.
    
    Features:
    - Execution time tracking with nanosecond precision
    - Resource usage monitoring (CPU, Memory)
    - Async/sync function profiling
    - Statistical aggregation
    - Bottleneck identification
    
    Example:
        profiler = AgentProfiler()
        
        # Sync profiling
        with profiler.profile("task_execution"):
            result = agent.execute_task()
        
        # Async profiling
        async with profiler.profile_async("async_task"):
            result = await agent.execute_async()
        
        # Get results
        stats = profiler.get_statistics()
    """
    
    def __init__(self):
        """Initialize the profiler."""
        self._results: List[ProfileResult] = []
        self._active_profiles: Dict[str, float] = {}
        self._custom_metrics: Dict[str, List[float]] = defaultdict(list)
        self._enabled = True
        
    def enable(self) -> None:
        """Enable profiling."""
        self._enabled = True
        
    def disable(self) -> None:
        """Disable profiling."""
        self._enabled = False
        
    @contextmanager
    def profile(self, name: str, **metadata):
        """
        Context manager for profiling a code block.
        
        Args:
            name: Identifier for this profile section
            **metadata: Additional metadata to store with the result
            
        Yields:
            ProfileResult: The profiling result object (updated after completion)
            
        Example:
            with profiler.profile("api_call", endpoint="/chat") as result:
                response = make_api_call()
        """
        if not self._enabled:
            yield None
            return
            
        start_time = time.perf_counter()
        start_process = time.process_time()
        
        # Try to get initial resource usage
        try:
            import psutil
            process = psutil.Process()
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            initial_cpu = process.cpu_percent()
        except ImportError:
            initial_memory = 0.0
            initial_cpu = 0.0
        
        result = ProfileResult(
            name=name,
            start_time=time.time(),
            end_time=0.0,
            duration_ms=0.0,
            metadata=metadata
        )
        
        try:
            yield result
        finally:
            end_time = time.perf_counter()
            end_process = time.process_time()
            
            # Calculate metrics
            result.end_time = time.time()
            result.duration_ms = (end_time - start_time) * 1000
            
            # Get final resource usage
            try:
                import psutil
                process = psutil.Process()
                final_memory = process.memory_info().rss / 1024 / 1024
                result.memory_mb = final_memory - initial_memory
                result.cpu_percent = process.cpu_percent()
            except ImportError:
                pass
            
            self._results.append(result)
    
    @contextmanager
    def profile_async(self, name: str, **metadata):
        """
        Async context manager for profiling async code blocks.
        
        Args:
            name: Identifier for this profile section
            **metadata: Additional metadata to store with the result
            
        Yields:
            ProfileResult: The profiling result object
            
        Example:
            async with profiler.profile_async("async_api_call") as result:
                response = await async_api_call()
        """
        return self.profile(name, **metadata)
    
    def record_metric(self, name: str, value: float) -> None:
        """
        Record a custom metric.
        
        Args:
            name: Metric name
            value: Metric value
        """
        if self._enabled:
            self._custom_metrics[name].append(value)
    
    def get_results(self, name: Optional[str] = None) -> List[ProfileResult]:
        """
        Get profiling results.
        
        Args:
            name: Optional filter by profile name
            
        Returns:
            List of ProfileResult objects
        """
        if name:
            return [r for r in self._results if r.name == name]
        return self._results.copy()
    
    def get_statistics(self) -> Dict[str, Dict]:
        """
        Calculate statistics for all profiled sections.
        
        Returns:
            Dictionary with statistics per profile name
        """
        stats = {}
        
        # Group results by name
        grouped = defaultdict(list)
        for result in self._results:
            grouped[result.name].append(result)
        
        # Calculate statistics
        for name, results in grouped.items():
            durations = [r.duration_ms for r in results]
            memories = [r.memory_mb for r in results if r.memory_mb > 0]
            
            stats[name] = {
                "count": len(results),
                "total_duration_ms": sum(durations),
                "avg_duration_ms": sum(durations) / len(durations),
                "min_duration_ms": min(durations),
                "max_duration_ms": max(durations),
                "avg_memory_mb": sum(memories) / len(memories) if memories else 0,
                "total_memory_mb": sum(memories) if memories else 0
            }
        
        # Add custom metrics statistics
        for metric_name, values in self._custom_metrics.items():
            if values:
                stats[f"metric:{metric_name}"] = {
                    "count": len(values),
                    "avg": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "total": sum(values)
                }
        
        return stats
    
    def identify_bottlenecks(self, threshold_ms: float = 100.0) -> List[Dict]:
        """
        Identify performance bottlenecks.
        
        Args:
            threshold_ms: Duration threshold in milliseconds
            
        Returns:
            List of bottleneck information dictionaries
        """
        bottlenecks = []
        stats = self.get_statistics()
        
        for name, stat in stats.items():
            if name.startswith("metric:"):
                continue
                
            if stat["avg_duration_ms"] > threshold_ms:
                bottlenecks.append({
                    "name": name,
                    "avg_duration_ms": stat["avg_duration_ms"],
                    "max_duration_ms": stat["max_duration_ms"],
                    "call_count": stat["count"],
                    "severity": "high" if stat["avg_duration_ms"] > threshold_ms * 5 else "medium"
                })
        
        # Sort by average duration
        bottlenecks.sort(key=lambda x: x["avg_duration_ms"], reverse=True)
        return bottlenecks
    
    def reset(self) -> None:
        """Clear all profiling data."""
        self._results.clear()
        self._active_profiles.clear()
        self._custom_metrics.clear()
    
    def summary(self) -> str:
        """Generate a text summary of profiling results."""
        stats = self.get_statistics()
        if not stats:
            return "No profiling data available."
        
        lines = ["\n📊 Profiling Summary", "=" * 50]
        
        for name, stat in stats.items():
            if name.startswith("metric:"):
                continue
            lines.append(f"\n🔹 {name}")
            lines.append(f"   Calls: {stat['count']}")
            lines.append(f"   Avg Duration: {stat['avg_duration_ms']:.2f}ms")
            lines.append(f"   Total Duration: {stat['total_duration_ms']:.2f}ms")
            if stat['avg_memory_mb'] > 0:
                lines.append(f"   Avg Memory: {stat['avg_memory_mb']:.2f}MB")
        
        # Bottlenecks
        bottlenecks = self.identify_bottlenecks()
        if bottlenecks:
            lines.append("\n⚠️  Bottlenecks Detected:")
            for b in bottlenecks[:5]:  # Top 5
                lines.append(f"   {b['name']}: {b['avg_duration_ms']:.2f}ms ({b['severity']})")
        
        return "\n".join(lines)
