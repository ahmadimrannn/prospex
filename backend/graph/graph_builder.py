from langgraph.graph import END, StateGraph

from graph.nodes.exa_search_node import exa_search_node
from graph.nodes.lead_extraction_node import lead_extractor
from graph.nodes.lead_verification_node import lead_verification_node
from graph.nodes.finalize_leads import finalize_leads
from graph.nodes.query_generation_node import query_generation_node
from graph.state.state import LeadAgentState

from config.database_config import checkpointer

def build_graph():
    """Build the lead discovery pipeline."""
    workflow = StateGraph(LeadAgentState)

    workflow.add_node("query_generation", query_generation_node)
    workflow.add_node("exa_search", exa_search_node)
    workflow.add_node("lead_extraction", lead_extractor)
    workflow.add_node("lead_verification", lead_verification_node)
    workflow.add_node("finalize_leads", finalize_leads)

    workflow.set_entry_point("query_generation")
    workflow.add_edge("query_generation", "exa_search")
    workflow.add_edge("exa_search", "lead_extraction")
    workflow.add_edge("lead_extraction", "lead_verification")
    workflow.add_edge("lead_verification", "finalize_leads")
    workflow.add_edge("finalize_leads", END)

    return workflow.compile(checkpointer=checkpointer)


graph = build_graph()
