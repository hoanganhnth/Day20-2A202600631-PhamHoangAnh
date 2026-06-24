"""Analyst agent implementation."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.core.schemas import AgentName, AgentResult


class AnalystAgent(BaseAgent):
    """Turns research notes into structured insights."""

    name = "analyst"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.analysis_notes`."""
        
        if not state.research_notes:
            state.analysis_notes = "No research notes to analyze."
            return state

        llm = LLMClient()
        
        system_prompt = (
            "You are a critical analyst. Your task is to extract key claims, compare viewpoints, "
            "and flag weak evidence from the provided research notes. Present your analysis clearly."
        )
        
        user_prompt = f"Research Notes:\n{state.research_notes}"
        
        response = llm.complete(system_prompt, user_prompt)
        
        state.analysis_notes = response.content
        
        state.agent_results.append(AgentResult(
            agent=AgentName.ANALYST,
            content=response.content,
            metadata={"cost_usd": response.cost_usd, "input_tokens": response.input_tokens, "output_tokens": response.output_tokens}
        ))
        
        return state
