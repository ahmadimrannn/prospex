from graph.state.state import LeadAgentState
from tools.leads import insert_lead
from tools.hubspot import write_leads_to_hubspot


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

    hubspot_result = write_leads_to_hubspot(verified_leads)

    print(
        f"HubSpot: created={hubspot_result['created']}, "
        f"already_exists={hubspot_result['already_exists']}, "
        f"failed={hubspot_result['failed']}"
    )

    return {
    "success": hubspot_result["success"],
    "status": hubspot_result["status"],
    "message": hubspot_result["message"],
    "leads": verified_leads,
}