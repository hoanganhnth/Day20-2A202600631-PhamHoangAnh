"""Command-line entrypoint for the lab starter."""

from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel

from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow
from multi_agent_research_lab.observability.logging import configure_logging

app = typer.Typer(help="Multi-Agent Research Lab starter CLI")
console = Console()


def _init() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)


@app.command()
def baseline(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run a minimal single-agent baseline placeholder."""

    _init()
    request = ResearchQuery(query=query)
    state = ResearchState(request=request)
    
    from multi_agent_research_lab.services.llm_client import LLMClient
    from multi_agent_research_lab.services.search_client import SearchClient
    
    # 1. Search
    search = SearchClient()
    sources = search.search(query)
    sources_text = "\n\n".join([f"Source: {s.title} ({s.url})\nContent: {s.snippet}" for s in sources])
    
    # 2. Generate final answer directly
    llm = LLMClient()
    system_prompt = "You are a research assistant. Based on search results, answer the query."
    user_prompt = f"Query: {query}\n\nSearch Results:\n{sources_text}"
    
    response = llm.complete(system_prompt, user_prompt)
    
    state.final_answer = response.content
    console.print(Panel.fit(state.final_answer, title="Single-Agent Baseline"))


@app.command("multi-agent")
def multi_agent(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run the multi-agent workflow skeleton."""

    _init()
    state = ResearchState(request=ResearchQuery(query=query))
    workflow = MultiAgentWorkflow()
    try:
        result = workflow.run(state)
    except StudentTodoError as exc:
        console.print(Panel.fit(str(exc), title="Expected TODO", style="yellow"))
        raise typer.Exit(code=2) from exc
        
    console.print(result.model_dump_json(indent=2))
    
    # Trace Output for Deliverable #2
    from rich.table import Table
    table = Table(title="Execution Trace (Deliverable 2)")
    table.add_column("Step", justify="right", style="cyan", no_wrap=True)
    table.add_column("Agent", style="magenta")
    table.add_column("Action / Route", style="green")
    
    table.add_row("0", "Supervisor", "Started Workflow")
    for i, route in enumerate(result.route_history):
        table.add_row(str(i+1), "Supervisor -> Worker", f"Routed to: [bold]{route}[/bold]")
        if route != "done":
            table.add_row("", route.capitalize(), "Executed Task & Returned to Supervisor")
            
    console.print("\n")
    console.print(table)


if __name__ == "__main__":
    app()
