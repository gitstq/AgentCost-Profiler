"""API call tracking module."""

import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum


class APIStatus(Enum):
    """API call status."""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    RETRY = "retry"


@dataclass
class APICall:
    """API call record."""
    provider: str
    model: str
    endpoint: str
    start_time: float
    end_time: float
    duration_ms: float
    status: APIStatus
    tokens_in: int = 0
    tokens_out: int = 0
    error_message: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


class APITracker:
    """
    Track API calls for analysis.
    
    Records timing, tokens, errors, and other metrics for
    all LLM API interactions.
    """
    
    def __init__(self):
        """Initialize API tracker."""
        self._calls: List[APICall] = []
        self._enabled = True
    
    def enable(self) -> None:
        """Enable tracking."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable tracking."""
        self._enabled = False
    
    def record(
        self,
        provider: str,
        model: str,
        endpoint: str,
        duration_ms: float,
        status: APIStatus = APIStatus.SUCCESS,
        tokens_in: int = 0,
        tokens_out: int = 0,
        error_message: Optional[str] = None,
        **metadata
    ) -> None:
        """
        Record an API call.
        
        Args:
            provider: API provider name
            model: Model name
            endpoint: API endpoint
            duration_ms: Call duration in milliseconds
            status: Call status
            tokens_in: Input tokens
            tokens_out: Output tokens
            error_message: Error message if failed
            **metadata: Additional metadata
        """
        if not self._enabled:
            return
        
        call = APICall(
            provider=provider,
            model=model,
            endpoint=endpoint,
            start_time=time.time() - (duration_ms / 1000),
            end_time=time.time(),
            duration_ms=duration_ms,
            status=status,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            error_message=error_message,
            metadata=metadata
        )
        self._calls.append(call)
    
    def get_calls(
        self,
        provider: Optional[str] = None,
        status: Optional[APIStatus] = None
    ) -> List[APICall]:
        """
        Get filtered API calls.
        
        Args:
            provider: Filter by provider
            status: Filter by status
            
        Returns:
            List of API calls
        """
        calls = self._calls
        
        if provider:
            calls = [c for c in calls if c.provider == provider]
        
        if status:
            calls = [c for c in calls if c.status == status]
        
        return calls
    
    def get_statistics(self) -> Dict:
        """Get API call statistics."""
        if not self._calls:
            return {}
        
        total_calls = len(self._calls)
        successful = len([c for c in self._calls if c.status == APIStatus.SUCCESS])
        failed = total_calls - successful
        
        durations = [c.duration_ms for c in self._calls]
        total_tokens = sum(c.tokens_in + c.tokens_out for c in self._calls)
        
        # Group by provider
        by_provider = defaultdict(lambda: {"calls": 0, "tokens": 0, "errors": 0})
        for call in self._calls:
            by_provider[call.provider]["calls"] += 1
            by_provider[call.provider]["tokens"] += call.tokens_in + call.tokens_out
            if call.status != APIStatus.SUCCESS:
                by_provider[call.provider]["errors"] += 1
        
        return {
            "total_calls": total_calls,
            "successful_calls": successful,
            "failed_calls": failed,
            "success_rate": successful / total_calls if total_calls > 0 else 0,
            "avg_duration_ms": sum(durations) / len(durations) if durations else 0,
            "max_duration_ms": max(durations) if durations else 0,
            "min_duration_ms": min(durations) if durations else 0,
            "total_tokens": total_tokens,
            "by_provider": dict(by_provider)
        }
    
    def get_error_summary(self) -> List[Dict]:
        """Get summary of errors."""
        errors = [c for c in self._calls if c.status != APIStatus.SUCCESS]
        
        # Group by error message
        error_groups = defaultdict(list)
        for error in errors:
            key = error.error_message or "Unknown error"
            error_groups[key].append(error)
        
        return [
            {
                "error": error_msg,
                "count": len(calls),
                "providers": list(set(c.provider for c in calls))
            }
            for error_msg, calls in error_groups.items()
        ]
    
    def reset(self) -> None:
        """Clear all tracked calls."""
        self._calls.clear()
