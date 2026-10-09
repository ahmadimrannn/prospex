from graph.state.state import LeadAgentState
from graph.prompts.prompts import generate_lead_verification_prompt
from graph.schemas.schema import VerifiedLeadList
from config.llm import model


def lead_verification_node(state: LeadAgentState):
    """Verify discovered leads using the LLM."""

    leads = state.get("discovered_leads", [])
    search_results = state.get("search_results", [])
    input_city = state.get("city", "").strip().casefold()
    is_website_required = state.get("require_website", False)

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

    verifier = model.with_structured_output(VerifiedLeadList)
    result = verifier.invoke(prompt)

    verified_leads = []
    rejected_leads = []

    for lead in result.leads:
        lead_data = (
            lead.model_dump()
            if hasattr(lead, "model_dump")
            else lead
        )

        lead_city = str(lead_data.get("city", "")).strip().casefold()

        # Reject leads whose city does not match the requested city.
        if input_city and input_city not in lead_city and lead_city not in input_city:
            rejected_leads.append(lead_data)
            continue

        lead_website = lead_data.get("website")

        if is_website_required and not lead_website:
            rejected_leads.append(lead_data)
            continue

        if lead_data.get("status") == "verified":
            verified_leads.append(lead_data)
        else:
            rejected_leads.append(lead_data)

    return {
        "verified_leads": verified_leads,
        "rejected_leads": rejected_leads,
    }