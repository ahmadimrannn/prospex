from graph.state.state import LeadAgentState
from tools.leads import insert_lead


def finalize_leads(state: LeadAgentState):
    """Keep the final verified leads in state and save them to Neon."""

    verified_leads = state.get("verified_leads", [])

    # Save final verified leads to Neon
    for lead in verified_leads:
        try:
            insert_lead(lead)
        except Exception as e:
            print(
                f"Failed to insert lead "
                f"{lead.get('business_name', 'unknown')}: {str(e)}"
            )

    return {
        "leads": verified_leads
    }