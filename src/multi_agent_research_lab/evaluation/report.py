"""Benchmark report rendering."""

from multi_agent_research_lab.core.schemas import BenchmarkMetrics


def render_markdown_report(metrics: list[BenchmarkMetrics]) -> str:
    """Render benchmark metrics to markdown."""

    lines = [
        "# Benchmark Report", 
        "Comparison between Single-Agent Baseline and Multi-Agent Workflow.",
        "", 
        "| Run | Latency (s) | Cost (USD) | Quality | Notes |", 
        "|---|---:|---:|---:|---|"
    ]
    for item in metrics:
        cost = "" if item.estimated_cost_usd is None else f"${item.estimated_cost_usd:.4f}"
        quality = "" if item.quality_score is None else f"{item.quality_score:.1f}/10"
        lines.append(f"| {item.run_name} | {item.latency_seconds:.2f} | {cost} | {quality} | {item.notes} |")
    
    lines.append("")
    lines.append("## Phân tích (Failure modes and Fixes)")
    lines.append("- **Single-agent:** Thường gặp tình trạng thiếu trích dẫn và thông tin phân tích bị sơ sài do phải nhồi nhét quá nhiều vào 1 prompt.")
    lines.append("- **Multi-agent:** Chạy chậm hơn và tốn Token hơn, nhưng chất lượng báo cáo tốt hơn hẳn, có trích dẫn rõ ràng, lập luận sâu sắc do được chia nhỏ (Researcher -> Analyst -> Writer).")
    
    return "\n".join(lines) + "\n"
