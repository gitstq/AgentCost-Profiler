"""
Command-line interface for AgentCost-Profiler.

Provides a user-friendly CLI for profiling AI Agent performance
and analyzing costs.
"""

import argparse
import sys
import asyncio
from pathlib import Path
from typing import Optional

from .core.profiler import AgentProfiler
from .core.cost_calculator import CostCalculator, TokenUsage, Provider
from .core.optimizer import Optimizer
from .monitors.api_tracker import APITracker
from .reporters.console import ConsoleReporter
from .reporters.html import HTMLReporter
from .reporters.json import JSONReporter


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="agentcost-profiler",
        description="🚀 AgentCost-Profiler: AI Agent Performance & Cost Optimization Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Profile a Python script
  agentcost-profiler profile -- python my_agent.py
  
  # Calculate cost for token usage
  agentcost-profiler cost --provider openai --model gpt-4 --prompt-tokens 1000 --completion-tokens 500
  
  # Compare costs across models
  agentcost-profiler compare --prompt-tokens 1000 --completion-tokens 500
  
  # Generate HTML report
  agentcost-profiler report --profiling-data stats.json --output report.html
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Profile command
    profile_parser = subparsers.add_parser(
        "profile",
        help="Profile execution of a command or script"
    )
    profile_parser.add_argument(
        "--output", "-o",
        help="Output file for profiling data (JSON)"
    )
    profile_parser.add_argument(
        "--html",
        help="Generate HTML report"
    )
    profile_parser.add_argument(
        "command_args",
        nargs=argparse.REMAINDER,
        help="Command to profile (prefix with --)"
    )
    
    # Cost command
    cost_parser = subparsers.add_parser(
        "cost",
        help="Calculate API call cost"
    )
    cost_parser.add_argument(
        "--provider", "-p",
        choices=[p.value for p in Provider],
        default="openai",
        help="LLM provider"
    )
    cost_parser.add_argument(
        "--model", "-m",
        required=True,
        help="Model name"
    )
    cost_parser.add_argument(
        "--prompt-tokens", "-pt",
        type=int,
        required=True,
        help="Number of prompt tokens"
    )
    cost_parser.add_argument(
        "--completion-tokens", "-ct",
        type=int,
        default=0,
        help="Number of completion tokens"
    )
    
    # Compare command
    compare_parser = subparsers.add_parser(
        "compare",
        help="Compare costs across different models"
    )
    compare_parser.add_argument(
        "--prompt-tokens", "-pt",
        type=int,
        required=True,
        help="Number of prompt tokens"
    )
    compare_parser.add_argument(
        "--completion-tokens", "-ct",
        type=int,
        default=0,
        help="Number of completion tokens"
    )
    
    # Report command
    report_parser = subparsers.add_parser(
        "report",
        help="Generate report from profiling data"
    )
    report_parser.add_argument(
        "--profiling-data",
        help="Path to profiling data JSON"
    )
    report_parser.add_argument(
        "--cost-data",
        help="Path to cost data JSON"
    )
    report_parser.add_argument(
        "--output", "-o",
        required=True,
        help="Output file path"
    )
    report_parser.add_argument(
        "--format", "-f",
        choices=["html", "json"],
        default="html",
        help="Output format"
    )
    
    # Demo command
    subparsers.add_parser(
        "demo",
        help="Run a demo profiling session"
    )
    
    # Version
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    return parser


def cmd_cost(args) -> int:
    """Handle cost command."""
    calculator = CostCalculator()
    
    provider = Provider(args.provider)
    usage = TokenUsage(
        prompt_tokens=args.prompt_tokens,
        completion_tokens=args.completion_tokens
    )
    
    try:
        cost = calculator.calculate(provider, args.model, usage)
        
        print(f"\n💰 Cost Calculation")
        print("=" * 50)
        print(f"Provider: {cost.provider}")
        print(f"Model: {cost.model}")
        print(f"Prompt Tokens: {cost.token_usage.prompt_tokens}")
        print(f"Completion Tokens: {cost.token_usage.completion_tokens}")
        print(f"\nPrompt Cost: ${cost.prompt_cost:.6f}")
        print(f"Completion Cost: ${cost.completion_cost:.6f}")
        print(f"Total Cost: ${cost.total_cost:.6f} {cost.currency}")
        
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_compare(args) -> int:
    """Handle compare command."""
    calculator = CostCalculator()
    
    usage = TokenUsage(
        prompt_tokens=args.prompt_tokens,
        completion_tokens=args.completion_tokens
    )
    
    # Compare popular models
    models = [
        (Provider.OPENAI, "gpt-4o"),
        (Provider.OPENAI, "gpt-4o-mini"),
        (Provider.ANTHROPIC, "claude-3-sonnet"),
        (Provider.ANTHROPIC, "claude-3-haiku"),
        (Provider.GOOGLE, "gemini-1.5-pro"),
        (Provider.GOOGLE, "gemini-1.5-flash"),
    ]
    
    results = calculator.compare_costs(usage, models)
    
    print(f"\n💰 Cost Comparison ({args.prompt_tokens} prompt + {args.completion_tokens} completion tokens)")
    print("=" * 70)
    print(f"{'Rank':<6} {'Provider':<12} {'Model':<20} {'Cost':>12} {'Savings':>12}")
    print("-" * 70)
    
    baseline_cost = results[0].total_cost if results else 0
    
    for i, cost in enumerate(results, 1):
        savings = ((baseline_cost - cost.total_cost) / baseline_cost * 100) if baseline_cost > 0 else 0
        print(f"{i:<6} {cost.provider:<12} {cost.model:<20} "
              f"${cost.total_cost:>10.6f} {savings:>10.1f}%")
    
    return 0


def cmd_report(args) -> int:
    """Handle report command."""
    import json
    
    profiling_stats = None
    costs = None
    
    if args.profiling_data:
        with open(args.profiling_data) as f:
            data = json.load(f)
            profiling_stats = data.get("profiling", {})
    
    if args.cost_data:
        with open(args.cost_data) as f:
            data = json.load(f)
            costs = data.get("costs", [])
    
    if args.format == "html":
        reporter = HTMLReporter()
        reporter.generate(args.output, profiling_stats, costs)
        print(f"HTML report generated: {args.output}")
    else:
        reporter = JSONReporter()
        reporter.generate(args.output, profiling_stats, costs)
        print(f"JSON report generated: {args.output}")
    
    return 0


def cmd_demo(args) -> int:
    """Run a demo profiling session."""
    import time
    import random
    
    print("\n🚀 AgentCost-Profiler Demo")
    print("=" * 50)
    print("Running simulated AI Agent profiling session...\n")
    
    # Initialize components
    profiler = AgentProfiler()
    calculator = CostCalculator()
    tracker = APITracker()
    optimizer = Optimizer()
    reporter = ConsoleReporter()
    
    # Simulate some operations
    operations = [
        ("api_call_openai", "openai", "gpt-4o", 1000, 500),
        ("api_call_claude", "anthropic", "claude-3-sonnet", 800, 400),
        ("data_processing", None, None, 0, 0),
        ("api_call_openai", "openai", "gpt-4o-mini", 500, 200),
        ("cache_lookup", None, None, 0, 0),
    ]
    
    costs = []
    
    for op_name, provider, model, prompt_tok, completion_tok in operations:
        # Profile the operation
        with profiler.profile(op_name):
            time.sleep(random.uniform(0.1, 0.5))  # Simulate work
            
            # Track API call
            if provider:
                duration = random.uniform(200, 800)
                tracker.record(
                    provider=provider,
                    model=model,
                    endpoint="/v1/chat/completions",
                    duration_ms=duration,
                    tokens_in=prompt_tok,
                    tokens_out=completion_tok
                )
                
                # Calculate cost
                try:
                    p = Provider(provider)
                    usage = TokenUsage(prompt_tok, completion_tok)
                    cost = calculator.calculate(p, model, usage)
                    costs.append(cost.to_dict())
                except ValueError:
                    pass
    
    # Get statistics
    stats = profiler.get_statistics()
    api_stats = tracker.get_statistics()
    
    # Generate recommendations
    optimizer.analyze(stats, costs)
    recommendations = optimizer.get_recommendations()
    
    # Generate report
    reporter.report_summary(stats, costs, recommendations)
    
    print("\n✅ Demo completed!")
    
    return 0


def main(args: Optional[list] = None) -> int:
    """Main entry point."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if not parsed_args.command:
        parser.print_help()
        return 0
    
    # Route to appropriate command
    commands = {
        "cost": cmd_cost,
        "compare": cmd_compare,
        "report": cmd_report,
        "demo": cmd_demo,
    }
    
    handler = commands.get(parsed_args.command)
    if handler:
        return handler(parsed_args)
    else:
        print(f"Unknown command: {parsed_args.command}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
