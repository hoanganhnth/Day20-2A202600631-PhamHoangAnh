"""Writer agent implementation."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.core.schemas import AgentName, AgentResult


class WriterAgent(BaseAgent):
    """Produces final answer from research and analysis notes."""

    name = "writer"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.final_answer`."""
        
        llm = LLMClient()
        
        system_prompt = (
            f"You are a professional technical writer creating a report for {state.request.audience}. "
            "Synthesize a clear, structured response using the provided research and analysis notes. "
            "Include inline citations based on the sources provided if applicable."
        )
        
        user_prompt = (
            f"Original Query: {state.request.query}\n\n"
            f"Research Notes:\n{state.research_notes or 'None'}\n\n"
            f"Analysis Notes:\n{state.analysis_notes or 'None'}"
        )
        
        response = llm.complete(system_prompt, user_prompt)
        
        state.final_answer = response.content
        
        state.agent_results.append(AgentResult(
            agent=AgentName.WRITER,
            content=response.content,
            metadata={"cost_usd": response.cost_usd, "input_tokens": response.input_tokens, "output_tokens": response.output_tokens}
        ))
        
        return state
