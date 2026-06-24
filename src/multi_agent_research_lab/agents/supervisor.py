"""Supervisor / router implementation."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState


class SupervisorAgent(BaseAgent):
    """Decides which worker should run next and when to stop."""

    name = "supervisor"

    def run(self, state: ResearchState) -> ResearchState:
        """Update `state.route_history` with the next route."""
        
        # Simple rule-based routing:
        # If no research notes, route to researcher.
        # If research notes exist but no analysis, route to analyst.
        # If both exist but no final answer, route to writer.
        # Else, done.
        
        next_route = "done"
        
        if not state.research_notes:
            next_route = "researcher"
        elif not state.analysis_notes:
            next_route = "analyst"
        elif not state.final_answer:
            next_route = "writer"

        state.record_route(next_route)
        return state
