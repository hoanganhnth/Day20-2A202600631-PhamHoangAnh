"""Researcher agent implementation."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.services.search_client import SearchClient
from multi_agent_research_lab.core.schemas import AgentName, AgentResult


class ResearcherAgent(BaseAgent):
    """Collects sources and creates concise research notes."""

    name = "researcher"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.sources` and `state.research_notes`."""
        
        # 1. Search for information
        search_client = SearchClient()
        sources = search_client.search(state.request.query, max_results=state.request.max_sources)
        state.sources.extend(sources)

        # 2. Compile notes using LLM
        llm = LLMClient()
        sources_text = "\n\n".join([f"Source: {s.title} ({s.url})\nContent: {s.snippet}" for s in sources])
        
        system_prompt = (
            "You are an expert researcher. "
            "Based on the provided search results, extract the most relevant facts, statistics, "
            "and insights to answer the user's query. Be concise and objective."
        )
        
        user_prompt = f"Query: {state.request.query}\n\nSearch Results:\n{sources_text}"
        
        response = llm.complete(system_prompt, user_prompt)
        
        state.research_notes = response.content
        
        # Record agent result
        state.agent_results.append(AgentResult(
            agent=AgentName.RESEARCHER,
            content=response.content,
            metadata={"cost_usd": response.cost_usd, "input_tokens": response.input_tokens, "output_tokens": response.output_tokens}
        ))
        
        return state
