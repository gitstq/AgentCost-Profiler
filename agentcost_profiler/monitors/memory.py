"""Memory monitoring module."""

import sys
import gc
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class MemoryInfo:
    """Memory usage information."""
    rss_mb: float
    vms_mb: float
    percent: float
    objects_count: int


class MemoryMonitor:
    """
    Memory usage monitor.
    
    Tracks memory consumption and helps identify memory leaks.
    """
    
    def __init__(self):
        """Initialize memory monitor."""
        try:
            import psutil
            self._psutil = psutil
            self._process = psutil.Process()
            self._available = True
        except ImportError:
            self._psutil = None
            self._available = False
        
        self._baseline = None
    
    def is_available(self) -> bool:
        """Check if memory monitoring is available."""
        return self._available
    
    def capture(self) -> Optional[MemoryInfo]:
        """Capture current memory state."""
        if not self._available:
            return self._fallback_capture()
        
        try:
            mem_info = self._process.memory_info()
            mem_percent = self._process.memory_percent()
            
            return MemoryInfo(
                rss_mb=mem_info.rss / 1024 / 1024,
                vms_mb=mem_info.vms / 1024 / 1024,
                percent=mem_percent,
                objects_count=len(gc.get_objects())
            )
        except Exception:
            return self._fallback_capture()
    
    def _fallback_capture(self) -> MemoryInfo:
        """Fallback memory capture without psutil."""
        # Get approximate memory from sys
        return MemoryInfo(
            rss_mb=0.0,
            vms_mb=0.0,
            percent=0.0,
            objects_count=len(gc.get_objects())
        )
    
    def set_baseline(self) -> None:
        """Set baseline memory for comparison."""
        self._baseline = self.capture()
    
    def get_delta(self) -> Optional[Dict]:
        """Get memory change from baseline."""
        if self._baseline is None:
            return None
        
        current = self.capture()
        if current is None:
            return None
        
        return {
            "rss_delta_mb": current.rss_mb - self._baseline.rss_mb,
            "vms_delta_mb": current.vms_mb - self._baseline.vms_mb,
            "objects_delta": current.objects_count - self._baseline.objects_count
        }
    
    def force_gc(self) -> Dict:
        """Force garbage collection and return stats."""
        gc.collect()
        return {
            "gc_generations": gc.get_count(),
            "objects_count": len(gc.get_objects())
        }
    
    def check_leak(self, threshold_mb: float = 50.0) -> bool:
        """
        Check for potential memory leak.
        
        Args:
            threshold_mb: Threshold in MB
            
        Returns:
            True if potential leak detected
        """
        delta = self.get_delta()
        if delta is None:
            return False
        
        return delta["rss_delta_mb"] > threshold_mb
