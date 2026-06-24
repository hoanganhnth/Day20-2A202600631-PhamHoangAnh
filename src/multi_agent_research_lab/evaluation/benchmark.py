"""Benchmark skeleton for single-agent vs multi-agent."""

from time import perf_counter
from typing import Callable

from multi_agent_research_lab.core.schemas import BenchmarkMetrics
from multi_agent_research_lab.core.state import ResearchState


Runner = Callable[[str], ResearchState]


def run_benchmark(run_name: str, query: str, runner: Runner) -> tuple[ResearchState, BenchmarkMetrics]:
    """Measure latency and return a placeholder metric object."""

    started = perf_counter()
    state = runner(query)
    latency = perf_counter() - started
    
    # Calculate total cost
    total_cost = 0.0
    for res in state.agent_results:
        if res.metadata.get("cost_usd"):
            total_cost += res.metadata["cost_usd"]

    # Basic heuristic quality score based on answer length and citation presence
    quality_score = 5.0
    if state.final_answer:
        if len(state.final_answer) > 500:
            quality_score += 2.0
        if "http" in state.final_answer or "Source" in state.final_answer:
            quality_score += 3.0

    metrics = BenchmarkMetrics(
        run_name=run_name, 
        latency_seconds=latency,
        estimated_cost_usd=total_cost,
        quality_score=min(10.0, quality_score),
        notes="Automated benchmark run."
    )
    return state, metrics
