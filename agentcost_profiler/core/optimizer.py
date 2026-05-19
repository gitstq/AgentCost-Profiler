"""
Optimization engine for AgentCost-Profiler.

Analyzes performance and cost data to provide actionable
optimization recommendations for AI Agents.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class OptimizationType(Enum):
    """Types of optimization recommendations."""
    COST = "cost"
    PERFORMANCE = "performance"
    CACHING = "caching"
    BATCHING = "batching"
    MODEL_SELECTION = "model_selection"
    PROMPT_OPTIMIZATION = "prompt_optimization"


class Priority(Enum):
    """Priority levels for recommendations."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Recommendation:
    """Optimization recommendation."""
    type: OptimizationType
    priority: Priority
    title: str
    description: str
    current_value: Any
    suggested_value: Any
    expected_savings: str
    implementation_difficulty: str  # easy, medium, hard
    code_example: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "type": self.type.value,
            "priority": self.priority.value,
            "title": self.title,
            "description": self.description,
            "current_value": self.current_value,
            "suggested_value": self.suggested_value,
            "expected_savings": self.expected_savings,
            "implementation_difficulty": self.implementation_difficulty,
            "code_example": self.code_example
        }


class Optimizer:
    """
    Optimization engine for AI Agent performance and cost.
    
    Analyzes profiling data and generates actionable recommendations
    for improving efficiency and reducing costs.
    
    Example:
        optimizer = Optimizer()
        
        # Analyze profiling results
        recommendations = optimizer.analyze(
            profiler_stats=profiler.get_statistics(),
            cost_breakdown=cost_data
        )
        
        # Get prioritized recommendations
        high_priority = optimizer.get_priority_recommendations(Priority.HIGH)
    """
    
    def __init__(self):
        """Initialize the optimizer."""
        self._recommendations: List[Recommendation] = []
        self._thresholds = {
            "high_cost_per_call": 0.10,  # $0.10 per call
            "slow_operation_ms": 1000,    # 1 second
            "frequent_call_threshold": 100,  # 100 calls
            "cache_hit_rate_low": 0.3,    # 30% cache hit rate
            "batch_size_small": 5,        # Less than 5 items per batch
        }
    
    def analyze(
        self,
        profiler_stats: Dict,
        cost_breakdown: Optional[List[Dict]] = None,
        custom_metrics: Optional[Dict] = None
    ) -> List[Recommendation]:
        """
        Analyze data and generate recommendations.
        
        Args:
            profiler_stats: Statistics from AgentProfiler
            cost_breakdown: List of cost breakdown dictionaries
            custom_metrics: Optional custom metrics
            
        Returns:
            List of recommendations
        """
        self._recommendations.clear()
        
        # Analyze performance
        self._analyze_performance(profiler_stats)
        
        # Analyze costs
        if cost_breakdown:
            self._analyze_costs(cost_breakdown)
        
        # Analyze custom metrics
        if custom_metrics:
            self._analyze_metrics(custom_metrics)
        
        # Sort by priority
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        self._recommendations.sort(key=lambda x: priority_order[x.priority])
        
        return self._recommendations
    
    def _analyze_performance(self, stats: Dict) -> None:
        """Analyze performance statistics."""
        for name, stat in stats.items():
            if name.startswith("metric:"):
                continue
            
            avg_duration = stat.get("avg_duration_ms", 0)
            count = stat.get("count", 0)
            
            # Check for slow operations
            if avg_duration > self._thresholds["slow_operation_ms"]:
                self._recommendations.append(Recommendation(
                    type=OptimizationType.PERFORMANCE,
                    priority=Priority.HIGH if avg_duration > 5000 else Priority.MEDIUM,
                    title=f"Optimize slow operation: {name}",
                    description=f"Operation '{name}' takes {avg_duration:.0f}ms on average. "
                               f"Consider async processing or caching.",
                    current_value=f"{avg_duration:.0f}ms",
                    suggested_value="< 1000ms",
                    expected_savings="50-80% latency reduction",
                    implementation_difficulty="medium",
                    code_example=self._get_async_example(name)
                ))
            
            # Check for frequent calls
            if count > self._thresholds["frequent_call_threshold"]:
                self._recommendations.append(Recommendation(
                    type=OptimizationType.BATCHING,
                    priority=Priority.MEDIUM,
                    title=f"Consider batching: {name}",
                    description=f"Operation '{name}' is called {count} times. "
                               f"Batching could reduce API calls.",
                    current_value=f"{count} calls",
                    suggested_value=f"{count // 5} batched calls",
                    expected_savings="60-80% API call reduction",
                    implementation_difficulty="medium",
                    code_example=self._get_batching_example()
                ))
    
    def _analyze_costs(self, cost_breakdown: List[Dict]) -> None:
        """Analyze cost data."""
        total_cost = sum(c.get("total_cost", 0) for c in cost_breakdown)
        
        for cost in cost_breakdown:
            provider = cost.get("provider", "unknown")
            model = cost.get("model", "unknown")
            call_cost = cost.get("total_cost", 0)
            
            # Check for expensive calls
            if call_cost > self._thresholds["high_cost_per_call"]:
                self._recommendations.append(Recommendation(
                    type=OptimizationType.MODEL_SELECTION,
                    priority=Priority.HIGH,
                    title=f"Consider cheaper model alternative",
                    description=f"Using {provider}/{model} costs ${call_cost:.4f} per call. "
                               f"Consider using a cheaper model for this use case.",
                    current_value=f"${call_cost:.4f} per call",
                    suggested_value="< $0.01 per call",
                    expected_savings="70-90% cost reduction",
                    implementation_difficulty="easy",
                    code_example=self._get_model_selection_example(provider, model)
                ))
        
        # General cost optimization
        if total_cost > 1.0:  # More than $1 total
            self._recommendations.append(Recommendation(
                type=OptimizationType.COST,
                priority=Priority.MEDIUM,
                title="Implement response caching",
                description=f"Total cost is ${total_cost:.4f}. Implementing caching "
                           f"could significantly reduce repeated API calls.",
                current_value=f"${total_cost:.4f}",
                suggested_value="50-80% reduction",
                expected_savings="50-80% cost reduction",
                implementation_difficulty="medium",
                code_example=self._get_caching_example()
            ))
    
    def _analyze_metrics(self, metrics: Dict) -> None:
        """Analyze custom metrics."""
        # Check cache hit rate if available
        if "cache_hits" in metrics and "cache_misses" in metrics:
            hits = sum(metrics["cache_hits"])
            misses = sum(metrics["cache_misses"])
            total = hits + misses
            
            if total > 0:
                hit_rate = hits / total
                if hit_rate < self._thresholds["cache_hit_rate_low"]:
                    self._recommendations.append(Recommendation(
                        type=OptimizationType.CACHING,
                        priority=Priority.HIGH,
                        title="Improve cache hit rate",
                        description=f"Cache hit rate is only {hit_rate*100:.1f}%. "
                                   f"Consider increasing cache TTL or improving cache keys.",
                        current_value=f"{hit_rate*100:.1f}%",
                        suggested_value="> 70%",
                        expected_savings="40-60% latency and cost reduction",
                        implementation_difficulty="easy",
                        code_example=self._get_cache_improvement_example()
                    ))
    
    def get_recommendations(
        self,
        type_filter: Optional[OptimizationType] = None,
        priority_filter: Optional[Priority] = None
    ) -> List[Recommendation]:
        """
        Get filtered recommendations.
        
        Args:
            type_filter: Filter by optimization type
            priority_filter: Filter by priority
            
        Returns:
            Filtered list of recommendations
        """
        results = self._recommendations
        
        if type_filter:
            results = [r for r in results if r.type == type_filter]
        
        if priority_filter:
            results = [r for r in results if r.priority == priority_filter]
        
        return results
    
    def get_priority_recommendations(self, priority: Priority) -> List[Recommendation]:
        """Get recommendations by priority."""
        return [r for r in self._recommendations if r.priority == priority]
    
    def summary(self) -> str:
        """Generate a text summary of recommendations."""
        if not self._recommendations:
            return "No optimization recommendations available."
        
        lines = ["\n💡 Optimization Recommendations", "=" * 50]
        
        # Group by priority
        for priority in [Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
            recs = self.get_priority_recommendations(priority)
            if recs:
                emoji = "🔴" if priority == Priority.HIGH else "🟡" if priority == Priority.MEDIUM else "🟢"
                lines.append(f"\n{emoji} {priority.value.upper()} Priority ({len(recs)})")
                lines.append("-" * 40)
                
                for rec in recs:
                    lines.append(f"\n📌 {rec.title}")
                    lines.append(f"   Type: {rec.type.value}")
                    lines.append(f"   {rec.description}")
                    lines.append(f"   💰 Expected: {rec.expected_savings}")
                    lines.append(f"   🔧 Difficulty: {rec.implementation_difficulty}")
        
        return "\n".join(lines)
    
    def _get_async_example(self, operation_name: str) -> str:
        """Get async optimization code example."""
        return f'''
# Convert synchronous operation to async
async def {operation_name}(...):
    # Use asyncio for concurrent execution
    results = await asyncio.gather(*[
        async_api_call(item) 
        for item in items
    ])
    return results
'''
    
    def _get_batching_example(self) -> str:
        """Get batching code example."""
        return '''
# Implement batching for API calls
class BatchedAPI:
    def __init__(self, batch_size=10):
        self.batch_size = batch_size
        self.queue = []
    
    async def add(self, item):
        self.queue.append(item)
        if len(self.queue) >= self.batch_size:
            await self.flush()
    
    async def flush(self):
        if self.queue:
            results = await api.batch_call(self.queue)
            self.queue.clear()
            return results
'''
    
    def _get_caching_example(self) -> str:
        """Get caching code example."""
        return '''
# Implement response caching
from functools import lru_cache
import hashlib

class CachedLLM:
    def __init__(self):
        self.cache = {}
    
    def _get_cache_key(self, prompt, **kwargs):
        key = f"{prompt}:{sorted(kwargs.items())}"
        return hashlib.md5(key.encode()).hexdigest()
    
    async def generate(self, prompt, **kwargs):
        cache_key = self._get_cache_key(prompt, **kwargs)
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        response = await self.llm.generate(prompt, **kwargs)
        self.cache[cache_key] = response
        return response
'''
    
    def _get_model_selection_example(self, provider: str, model: str) -> str:
        """Get model selection code example."""
        cheaper_models = {
            "openai": "gpt-4o-mini",
            "anthropic": "claude-3-haiku",
            "google": "gemini-1.5-flash"
        }
        cheaper = cheaper_models.get(provider, "cheaper-model")
        
        return f'''
# Use cheaper model for simpler tasks
MODEL_TIERS = {{
    "complex": "{model}",      # For complex reasoning
    "simple": "{cheaper}"      # For simple tasks
}}

def select_model(task_complexity: str) -> str:
    return MODEL_TIERS.get(task_complexity, MODEL_TIERS["simple"])

# Usage
model = select_model("simple")  # Use cheaper model
response = await llm.generate(prompt, model=model)
'''
    
    def _get_cache_improvement_example(self) -> str:
        """Get cache improvement code example."""
        return '''
# Improve cache effectiveness
import time

class SmartCache:
    def __init__(self, ttl=3600):
        self.cache = {}
        self.ttl = ttl
        self.access_patterns = {}
    
    def get(self, key):
        if key in self.cache:
            item, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                # Update access pattern
                self.access_patterns[key] = self.access_patterns.get(key, 0) + 1
                return item
            else:
                del self.cache[key]
        return None
    
    def set(self, key, value):
        # Only cache frequently accessed items
        if self.access_patterns.get(key, 0) > 2:
            self.cache[key] = (value, time.time())
'''
