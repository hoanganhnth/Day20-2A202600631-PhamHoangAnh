"""LangGraph workflow implementation."""

from multi_agent_research_lab.core.state import ResearchState
from langgraph.graph import StateGraph, START, END

from multi_agent_research_lab.agents.supervisor import SupervisorAgent
from multi_agent_research_lab.agents.researcher import ResearcherAgent
from multi_agent_research_lab.agents.analyst import AnalystAgent
from multi_agent_research_lab.agents.writer import WriterAgent
from multi_agent_research_lab.core.config import get_settings


class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph.

    Keep orchestration here; keep agent internals in `agents/`.
    """

    def __init__(self):
        self.settings = get_settings()
        self.supervisor = SupervisorAgent()
        self.researcher = ResearcherAgent()
        self.analyst = AnalystAgent()
        self.writer = WriterAgent()

    def build(self) -> StateGraph:
        """Create a LangGraph graph."""
        workflow = StateGraph(ResearchState)

        workflow.add_node("supervisor", self.supervisor.run)
        workflow.add_node("researcher", self.researcher.run)
        workflow.add_node("analyst", self.analyst.run)
        workflow.add_node("writer", self.writer.run)

        def route(state: ResearchState) -> str:
            if state.iteration >= self.settings.max_iterations:
                return END
            last_route = state.route_history[-1] if state.route_history else "researcher"
            if last_route == "done":
                return END
            return last_route

        workflow.add_edge(START, "supervisor")
        workflow.add_conditional_edges("supervisor", route)
        workflow.add_edge("researcher", "supervisor")
        workflow.add_edge("analyst", "supervisor")
        workflow.add_edge("writer", "supervisor")

        return workflow

    def run(self, state: ResearchState) -> ResearchState:
        """Execute the graph and return final state."""
        workflow = self.build()
        app = workflow.compile()
        
        final_state_dict = app.invoke(state.model_dump())
        return ResearchState(**final_state_dict)
