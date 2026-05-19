"""Console reporter module using Rich for beautiful terminal output."""

import sys
from typing import Dict, List, Optional, Any
from datetime import datetime


class ConsoleReporter:
    """
    Generate beautiful console reports using Rich.
    
    Falls back to simple text output if Rich is not available.
    """
    
    def __init__(self):
        """Initialize console reporter."""
        self._rich_available = False
        self._console = None
        
        try:
            from rich.console import Console
            from rich.table import Table
            from rich.panel import Panel
            from rich.tree import Tree
            from rich import box
            
            self._console = Console()
            self._rich_available = True
            self._Table = Table
            self._Panel = Panel
            self._Tree = Tree
            self._box = box
        except ImportError:
            pass
    
    def is_rich_available(self) -> bool:
        """Check if Rich is available."""
        return self._rich_available
    
    def report_profiling(self, stats: Dict, bottlenecks: List[Dict]) -> None:
        """
        Report profiling statistics.
        
        Args:
            stats: Profiling statistics
            bottlenecks: List of bottlenecks
        """
        if self._rich_available:
            self._report_profiling_rich(stats, bottlenecks)
        else:
            self._report_profiling_simple(stats, bottlenecks)
    
    def _report_profiling_rich(self, stats: Dict, bottlenecks: List[Dict]) -> None:
        """Rich profiling report."""
        from rich.table import Table
        from rich.panel import Panel
        
        # Title
        self._console.print()
        self._console.print(Panel.fit(
            "[bold blue]📊 Performance Profiling Report[/bold blue]",
            border_style="blue"
        ))
        
        # Statistics table
        table = Table(
            title="Profiling Statistics",
            box=self._box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )
        
        table.add_column("Operation", style="cyan")
        table.add_column("Calls", justify="right")
        table.add_column("Avg (ms)", justify="right")
        table.add_column("Total (ms)", justify="right")
        table.add_column("Memory (MB)", justify="right")
        
        for name, stat in stats.items():
            if name.startswith("metric:"):
                continue
            
            table.add_row(
                name,
                str(stat.get("count", 0)),
                f"{stat.get('avg_duration_ms', 0):.2f}",
                f"{stat.get('total_duration_ms', 0):.2f}",
                f"{stat.get('avg_memory_mb', 0):.2f}"
            )
        
        self._console.print(table)
        
        # Bottlenecks
        if bottlenecks:
            self._console.print()
            self._console.print(Panel.fit(
                "[bold yellow]⚠️ Performance Bottlenecks[/bold yellow]",
                border_style="yellow"
            ))
            
            bottleneck_table = Table(box=self._box.ROUNDED)
            bottleneck_table.add_column("Operation", style="yellow")
            bottleneck_table.add_column("Avg Duration", justify="right")
            bottleneck_table.add_column("Severity", justify="center")
            
            for b in bottlenecks[:10]:
                severity_color = "red" if b["severity"] == "high" else "yellow"
                bottleneck_table.add_row(
                    b["name"],
                    f"{b['avg_duration_ms']:.2f}ms",
                    f"[{severity_color}]{b['severity'].upper()}[/{severity_color}]"
                )
            
            self._console.print(bottleneck_table)
    
    def _report_profiling_simple(self, stats: Dict, bottlenecks: List[Dict]) -> None:
        """Simple text profiling report."""
        print("\n" + "=" * 60)
        print("📊 Performance Profiling Report")
        print("=" * 60)
        
        print("\nProfiling Statistics:")
        print("-" * 60)
        print(f"{'Operation':<30} {'Calls':>8} {'Avg(ms)':>10} {'Total(ms)':>12}")
        print("-" * 60)
        
        for name, stat in stats.items():
            if name.startswith("metric:"):
                continue
            print(f"{name:<30} {stat.get('count', 0):>8} "
                  f"{stat.get('avg_duration_ms', 0):>10.2f} "
                  f"{stat.get('total_duration_ms', 0):>12.2f}")
        
        if bottlenecks:
            print("\n" + "-" * 60)
            print("⚠️ Performance Bottlenecks:")
            print("-" * 60)
            for b in bottlenecks[:10]:
                print(f"  {b['name']}: {b['avg_duration_ms']:.2f}ms ({b['severity']})")
    
    def report_costs(self, costs: List[Dict]) -> None:
        """
        Report cost analysis.
        
        Args:
            costs: List of cost breakdowns
        """
        if not costs:
            print("\nNo cost data available.")
            return
        
        if self._rich_available:
            self._report_costs_rich(costs)
        else:
            self._report_costs_simple(costs)
    
    def _report_costs_rich(self, costs: List[Dict]) -> None:
        """Rich cost report."""
        from rich.table import Table
        from rich.panel import Panel
        
        self._console.print()
        self._console.print(Panel.fit(
            "[bold green]💰 Cost Analysis Report[/bold green]",
            border_style="green"
        ))
        
        table = Table(
            title="Cost Breakdown",
            box=self._box.ROUNDED,
            show_header=True,
            header_style="bold green"
        )
        
        table.add_column("Provider", style="green")
        table.add_column("Model")
        table.add_column("Prompt Cost", justify="right")
        table.add_column("Completion Cost", justify="right")
        table.add_column("Total Cost", justify="right")
        table.add_column("Tokens", justify="right")
        
        total = 0.0
        for cost in costs:
            total += cost.get("total_cost", 0)
            table.add_row(
                cost.get("provider", "unknown"),
                cost.get("model", "unknown"),
                f"${cost.get('prompt_cost', 0):.6f}",
                f"${cost.get('completion_cost', 0):.6f}",
                f"${cost.get('total_cost', 0):.6f}",
                str(cost.get("token_usage", {}).get("total_tokens", 0))
            )
        
        self._console.print(table)
        self._console.print(f"\n[bold]Total Cost: ${total:.6f}[/bold]")
    
    def _report_costs_simple(self, costs: List[Dict]) -> None:
        """Simple text cost report."""
        print("\n" + "=" * 60)
        print("💰 Cost Analysis Report")
        print("=" * 60)
        
        print(f"\n{'Provider':<15} {'Model':<20} {'Cost':>12} {'Tokens':>10}")
        print("-" * 60)
        
        total = 0.0
        for cost in costs:
            total += cost.get("total_cost", 0)
            print(f"{cost.get('provider', 'unknown'):<15} "
                  f"{cost.get('model', 'unknown'):<20} "
                  f"${cost.get('total_cost', 0):>10.6f} "
                  f"{cost.get('token_usage', {}).get('total_tokens', 0):>10}")
        
        print("-" * 60)
        print(f"{'Total Cost:':<36} ${total:>10.6f}")
    
    def report_recommendations(self, recommendations: List[Any]) -> None:
        """
        Report optimization recommendations.
        
        Args:
            recommendations: List of Recommendation objects
        """
        if not recommendations:
            print("\nNo optimization recommendations available.")
            return
        
        if self._rich_available:
            self._report_recommendations_rich(recommendations)
        else:
            self._report_recommendations_simple(recommendations)
    
    def _report_recommendations_rich(self, recommendations: List[Any]) -> None:
        """Rich recommendations report."""
        from rich.panel import Panel
        from rich.tree import Tree
        
        self._console.print()
        self._console.print(Panel.fit(
            "[bold magenta]💡 Optimization Recommendations[/bold magenta]",
            border_style="magenta"
        ))
        
        # Group by priority
        high = [r for r in recommendations if r.priority.value == "high"]
        medium = [r for r in recommendations if r.priority.value == "medium"]
        low = [r for r in recommendations if r.priority.value == "low"]
        
        if high:
            tree = Tree("[red]🔴 High Priority[/red]")
            for rec in high:
                self._add_rec_to_tree(tree, rec)
            self._console.print(tree)
        
        if medium:
            tree = Tree("[yellow]🟡 Medium Priority[/yellow]")
            for rec in medium:
                self._add_rec_to_tree(tree, rec)
            self._console.print(tree)
        
        if low:
            tree = Tree("[green]🟢 Low Priority[/green]")
            for rec in low:
                self._add_rec_to_tree(tree, rec)
            self._console.print(tree)
    
    def _add_rec_to_tree(self, tree: Any, rec: Any) -> None:
        """Add recommendation to tree."""
        branch = tree.add(f"[bold]{rec.title}[/bold]")
        branch.add(f"Type: {rec.type.value}")
        branch.add(f"Description: {rec.description}")
        branch.add(f"Expected Savings: {rec.expected_savings}")
    
    def _report_recommendations_simple(self, recommendations: List[Any]) -> None:
        """Simple text recommendations report."""
        print("\n" + "=" * 60)
        print("💡 Optimization Recommendations")
        print("=" * 60)
        
        # Group by priority
        high = [r for r in recommendations if r.priority.value == "high"]
        medium = [r for r in recommendations if r.priority.value == "medium"]
        low = [r for r in recommendations if r.priority.value == "low"]
        
        if high:
            print("\n🔴 High Priority:")
            for rec in high:
                print(f"\n  📌 {rec.title}")
                print(f"     {rec.description}")
                print(f"     Expected: {rec.expected_savings}")
        
        if medium:
            print("\n🟡 Medium Priority:")
            for rec in medium:
                print(f"\n  📌 {rec.title}")
                print(f"     {rec.description}")
        
        if low:
            print("\n🟢 Low Priority:")
            for rec in low:
                print(f"\n  📌 {rec.title}")
                print(f"     {rec.description}")
    
    def report_summary(
        self,
        profiling_stats: Optional[Dict] = None,
        costs: Optional[List[Dict]] = None,
        recommendations: Optional[List[Any]] = None
    ) -> None:
        """
        Generate comprehensive summary report.
        
        Args:
            profiling_stats: Profiling statistics
            costs: Cost breakdowns
            recommendations: Recommendations
        """
        if self._rich_available:
            from rich.panel import Panel
            self._console.print()
            self._console.print(Panel.fit(
                "[bold cyan]📋 AgentCost-Profiler Summary Report[/bold cyan]",
                subtitle=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                border_style="cyan"
            ))
        else:
            print("\n" + "=" * 60)
            print("📋 AgentCost-Profiler Summary Report")
            print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60)
        
        if profiling_stats:
            bottlenecks = []  # Would be passed from profiler
            self.report_profiling(profiling_stats, bottlenecks)
        
        if costs:
            self.report_costs(costs)
        
        if recommendations:
            self.report_recommendations(recommendations)
