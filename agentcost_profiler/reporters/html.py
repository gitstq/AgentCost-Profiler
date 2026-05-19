"""HTML reporter module."""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path


class HTMLReporter:
    """
    Generate HTML reports for profiling data.
    
    Creates interactive HTML reports with tables and charts.
    """
    
    def __init__(self, title: str = "AgentCost-Profiler Report"):
        """
        Initialize HTML reporter.
        
        Args:
            title: Report title
        """
        self.title = title
    
    def generate(
        self,
        output_path: str,
        profiling_stats: Optional[Dict] = None,
        costs: Optional[List[Dict]] = None,
        recommendations: Optional[List[Any]] = None,
        api_stats: Optional[Dict] = None
    ) -> str:
        """
        Generate HTML report.
        
        Args:
            output_path: Path to save HTML file
            profiling_stats: Profiling statistics
            costs: Cost breakdowns
            recommendations: Recommendations
            api_stats: API statistics
            
        Returns:
            Path to generated HTML file
        """
        html_content = self._build_html(
            profiling_stats,
            costs,
            recommendations,
            api_stats
        )
        
        # Write to file
        Path(output_path).write_text(html_content, encoding='utf-8')
        return output_path
    
    def _build_html(
        self,
        profiling_stats: Optional[Dict],
        costs: Optional[List[Dict]],
        recommendations: Optional[List[Any]],
        api_stats: Optional[Dict]
    ) -> str:
        """Build HTML content."""
        
        css = """
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #f5f7fa;
                color: #333;
                line-height: 1.6;
            }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            header h1 { font-size: 2.5em; margin-bottom: 10px; }
            header p { opacity: 0.9; }
            .section {
                background: white;
                border-radius: 10px;
                padding: 30px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            .section h2 {
                color: #667eea;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #f0f0f0;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #eee;
            }
            th {
                background: #f8f9fa;
                font-weight: 600;
                color: #555;
            }
            tr:hover { background: #f8f9fa; }
            .metric {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                margin: 5px;
                font-size: 0.9em;
            }
            .priority-high { color: #e74c3c; font-weight: bold; }
            .priority-medium { color: #f39c12; font-weight: bold; }
            .priority-low { color: #27ae60; font-weight: bold; }
            .cost-total {
                font-size: 1.5em;
                color: #27ae60;
                font-weight: bold;
                margin-top: 20px;
            }
            .recommendation {
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 15px;
                margin: 10px 0;
                border-radius: 0 5px 5px 0;
            }
            .recommendation h4 { color: #667eea; margin-bottom: 10px; }
            .recommendation p { color: #666; margin-bottom: 5px; }
            .badge {
                display: inline-block;
                padding: 3px 10px;
                border-radius: 3px;
                font-size: 0.8em;
                font-weight: bold;
            }
            .badge-success { background: #d4edda; color: #155724; }
            .badge-warning { background: #fff3cd; color: #856404; }
            .badge-danger { background: #f8d7da; color: #721c24; }
            footer {
                text-align: center;
                padding: 20px;
                color: #999;
                font-size: 0.9em;
            }
        </style>
        """
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    {css}
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 AgentCost-Profiler Report</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>
"""
        
        # Profiling Statistics
        if profiling_stats:
            html += self._build_profiling_section(profiling_stats)
        
        # Cost Analysis
        if costs:
            html += self._build_cost_section(costs)
        
        # API Statistics
        if api_stats:
            html += self._build_api_section(api_stats)
        
        # Recommendations
        if recommendations:
            html += self._build_recommendations_section(recommendations)
        
        html += """
        <footer>
            <p>Generated by AgentCost-Profiler | <a href="https://github.com/gitstq/AgentCost-Profiler">GitHub</a></p>
        </footer>
    </div>
</body>
</html>
"""
        
        return html
    
    def _build_profiling_section(self, stats: Dict) -> str:
        """Build profiling statistics section."""
        html = """
        <div class="section">
            <h2>🔍 Performance Profiling</h2>
            <table>
                <thead>
                    <tr>
                        <th>Operation</th>
                        <th>Calls</th>
                        <th>Avg Duration (ms)</th>
                        <th>Total Duration (ms)</th>
                        <th>Memory (MB)</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for name, stat in stats.items():
            if name.startswith("metric:"):
                continue
            html += f"""
                    <tr>
                        <td>{name}</td>
                        <td>{stat.get('count', 0)}</td>
                        <td>{stat.get('avg_duration_ms', 0):.2f}</td>
                        <td>{stat.get('total_duration_ms', 0):.2f}</td>
                        <td>{stat.get('avg_memory_mb', 0):.2f}</td>
                    </tr>
            """
        
        html += """
                </tbody>
            </table>
        </div>
        """
        return html
    
    def _build_cost_section(self, costs: List[Dict]) -> str:
        """Build cost analysis section."""
        total = sum(c.get("total_cost", 0) for c in costs)
        
        html = """
        <div class="section">
            <h2>💰 Cost Analysis</h2>
            <table>
                <thead>
                    <tr>
                        <th>Provider</th>
                        <th>Model</th>
                        <th>Prompt Cost</th>
                        <th>Completion Cost</th>
                        <th>Total Cost</th>
                        <th>Tokens</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for cost in costs:
            tokens = cost.get("token_usage", {})
            html += f"""
                    <tr>
                        <td>{cost.get('provider', 'unknown')}</td>
                        <td>{cost.get('model', 'unknown')}</td>
                        <td>${cost.get('prompt_cost', 0):.6f}</td>
                        <td>${cost.get('completion_cost', 0):.6f}</td>
                        <td>${cost.get('total_cost', 0):.6f}</td>
                        <td>{tokens.get('total_tokens', 0)}</td>
                    </tr>
            """
        
        html += f"""
                </tbody>
            </table>
            <div class="cost-total">Total Cost: ${total:.6f} USD</div>
        </div>
        """
        return html
    
    def _build_api_section(self, stats: Dict) -> str:
        """Build API statistics section."""
        success_rate = stats.get("success_rate", 0) * 100
        
        html = f"""
        <div class="section">
            <h2>🌐 API Usage Statistics</h2>
            <div style="margin-bottom: 20px;">
                <span class="metric">Total Calls: {stats.get('total_calls', 0)}</span>
                <span class="metric">Success Rate: {success_rate:.1f}%</span>
                <span class="metric">Avg Duration: {stats.get('avg_duration_ms', 0):.2f}ms</span>
                <span class="metric">Total Tokens: {stats.get('total_tokens', 0)}</span>
            </div>
        """
        
        by_provider = stats.get("by_provider", {})
        if by_provider:
            html += """
            <h3>Usage by Provider</h3>
            <table>
                <thead>
                    <tr>
                        <th>Provider</th>
                        <th>Calls</th>
                        <th>Tokens</th>
                        <th>Errors</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for provider, data in by_provider.items():
                html += f"""
                    <tr>
                        <td>{provider}</td>
                        <td>{data.get('calls', 0)}</td>
                        <td>{data.get('tokens', 0)}</td>
                        <td>{data.get('errors', 0)}</td>
                    </tr>
                """
            
            html += """
                </tbody>
            </table>
            """
        
        html += "</div>"
        return html
    
    def _build_recommendations_section(self, recommendations: List[Any]) -> str:
        """Build recommendations section."""
        html = """
        <div class="section">
            <h2>💡 Optimization Recommendations</h2>
        """
        
        for rec in recommendations:
            priority_class = f"priority-{rec.priority.value}"
            html += f"""
            <div class="recommendation">
                <h4>{rec.title} <span class="{priority_class}">[{rec.priority.value.upper()}]</span></h4>
                <p><strong>Type:</strong> {rec.type.value}</p>
                <p>{rec.description}</p>
                <p><strong>Expected Savings:</strong> {rec.expected_savings}</p>
                <p><strong>Implementation:</strong> {rec.implementation_difficulty}</p>
            </div>
            """
        
        html += "</div>"
        return html
