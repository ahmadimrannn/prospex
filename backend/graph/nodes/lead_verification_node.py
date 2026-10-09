from graph.state.state import LeadAgentState
from graph.prompts.prompts import generate_lead_verification_prompt
from graph.schemas.schema import VerifiedLeadList
from config.llm import llm


def lead_verification_node(state: LeadAgentState):
    """Verify discovered leads using the LLM."""

    leads = state.get("discovered_leads", [])
    search_results = state.get("search_results", [])

    if not leads:
        return {
            "verified_leads": [],
            "rejected_leads": [],
            "leads": [],
        }

    prompt = generate_lead_verification_prompt(
        leads=leads,
        search_results=search_results,
    )

    verifier = llm.with_structured_output(VerifiedLeadList)
    result = verifier.invoke(prompt)

    verified_leads = []
    rejected_leads = []

    for lead in result.leads:
        lead_data = (
            lead.model_dump()
            if hasattr(lead, "model_dump")
            else lead
        )

        if lead_data.get("status") == "verified":
            verified_leads.append(lead_data)
        else:
            rejected_leads.append(lead_data)

    return {
        "verified_leads": verified_leads,
        "rejected_leads": rejected_leads,
        "leads": verified_leads,
    }