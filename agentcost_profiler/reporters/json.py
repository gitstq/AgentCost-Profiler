"""JSON reporter module."""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path


class JSONReporter:
    """
    Generate JSON reports for programmatic consumption.
    
    Useful for integration with other tools and CI/CD pipelines.
    """
    
    def __init__(self):
        """Initialize JSON reporter."""
        pass
    
    def generate(
        self,
        output_path: str,
        profiling_stats: Optional[Dict] = None,
        costs: Optional[List[Dict]] = None,
        recommendations: Optional[List[Any]] = None,
        api_stats: Optional[Dict] = None,
        bottlenecks: Optional[List[Dict]] = None
    ) -> str:
        """
        Generate JSON report.
        
        Args:
            output_path: Path to save JSON file
            profiling_stats: Profiling statistics
            costs: Cost breakdowns
            recommendations: Recommendations
            api_stats: API statistics
            bottlenecks: Bottlenecks list
            
        Returns:
            Path to generated JSON file
        """
        report = {
            "metadata": {
                "tool": "AgentCost-Profiler",
                "version": "1.0.0",
                "generated_at": datetime.now().isoformat()
            },
            "profiling": profiling_stats or {},
            "costs": costs or [],
            "api_statistics": api_stats or {},
            "bottlenecks": bottlenecks or [],
            "recommendations": []
        }
        
        # Convert recommendations
        if recommendations:
            report["recommendations"] = [
                rec.to_dict() if hasattr(rec, 'to_dict') else rec
                for rec in recommendations
            ]
        
        # Write to file
        Path(output_path).write_text(
            json.dumps(report, indent=2, default=str),
            encoding='utf-8'
        )
        
        return output_path
    
    def generate_summary(
        self,
        output_path: str,
        total_cost: float,
        total_calls: int,
        avg_latency_ms: float,
        recommendations_count: int
    ) -> str:
        """
        Generate a summary JSON for CI/CD integration.
        
        Args:
            output_path: Output file path
            total_cost: Total cost
            total_calls: Total API calls
            avg_latency_ms: Average latency
            recommendations_count: Number of recommendations
            
        Returns:
            Path to generated file
        """
        summary = {
            "summary": {
                "total_cost_usd": round(total_cost, 6),
                "total_api_calls": total_calls,
                "average_latency_ms": round(avg_latency_ms, 2),
                "recommendations_count": recommendations_count,
                "generated_at": datetime.now().isoformat()
            },
            "thresholds": {
                "cost_alert": total_cost > 1.0,
                "latency_alert": avg_latency_ms > 1000,
                "calls_alert": total_calls > 100
            }
        }
        
        Path(output_path).write_text(
            json.dumps(summary, indent=2),
            encoding='utf-8'
        )
        
        return output_path
