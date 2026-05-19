"""Performance monitoring module."""

import time
import asyncio
from typing import Dict, Optional, Callable
from dataclasses import dataclass
from contextlib import contextmanager


@dataclass
class PerformanceSnapshot:
    """Performance metrics snapshot."""
    timestamp: float
    cpu_percent: float
    memory_mb: float
    io_read_mb: float
    io_write_mb: float


class PerformanceMonitor:
    """
    Real-time performance monitor.
    
    Monitors CPU, memory, and I/O usage during Agent execution.
    """
    
    def __init__(self, interval: float = 1.0):
        """
        Initialize monitor.
        
        Args:
            interval: Sampling interval in seconds
        """
        self.interval = interval
        self._snapshots: list = []
        self._running = False
        self._task = None
        
        # Try to import psutil
        try:
            import psutil
            self._psutil = psutil
            self._process = psutil.Process()
            self._available = True
        except ImportError:
            self._psutil = None
            self._available = False
    
    def is_available(self) -> bool:
        """Check if monitoring is available."""
        return self._available
    
    async def start(self) -> None:
        """Start monitoring."""
        if not self._available:
            return
            
        self._running = True
        self._task = asyncio.create_task(self._monitor_loop())
    
    async def stop(self) -> None:
        """Stop monitoring."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
    
    async def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self._running:
            snapshot = self._capture_snapshot()
            if snapshot:
                self._snapshots.append(snapshot)
            await asyncio.sleep(self.interval)
    
    def _capture_snapshot(self) -> Optional[PerformanceSnapshot]:
        """Capture a performance snapshot."""
        if not self._available:
            return None
            
        try:
            cpu = self._process.cpu_percent()
            memory = self._process.memory_info().rss / 1024 / 1024
            io_counters = self._process.io_counters()
            
            return PerformanceSnapshot(
                timestamp=time.time(),
                cpu_percent=cpu,
                memory_mb=memory,
                io_read_mb=io_counters.read_bytes / 1024 / 1024,
                io_write_mb=io_counters.write_bytes / 1024 / 1024
            )
        except Exception:
            return None
    
    def get_average_stats(self) -> Dict:
        """Get average statistics."""
        if not self._snapshots:
            return {}
            
        cpu_values = [s.cpu_percent for s in self._snapshots]
        memory_values = [s.memory_mb for s in self._snapshots]
        
        return {
            "avg_cpu_percent": sum(cpu_values) / len(cpu_values),
            "avg_memory_mb": sum(memory_values) / len(memory_values),
            "peak_cpu_percent": max(cpu_values),
            "peak_memory_mb": max(memory_values),
            "samples": len(self._snapshots)
        }
    
    def reset(self) -> None:
        """Clear all snapshots."""
        self._snapshots.clear()
