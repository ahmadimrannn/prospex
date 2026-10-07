from config.llm import model
from graph.schemas.schema import LeadDataList
from graph.state.state import LeadAgentState
from graph.prompts.prompts import generate_lead_extractor_prompt


lead_extractor_structured_llm = model.with_structured_output(LeadDataList)


def lead_extractor(state: LeadAgentState):
    """Extract and structure new business leads from Exa search results."""

    search_results = state.get("search_results", [])
    existing_leads = state.get("existing_leads", [])

    if not search_results:
        return {
            "discovered_leads": []
        }

    prompt = generate_lead_extractor_prompt(search_results)

    try:
        res = lead_extractor_structured_llm.invoke(prompt)

        discovered_leads = [
            lead.model_dump()
            for lead in res.leads
        ]

        # Build lookup sets for existing businesses
        existing_names = {
            lead["business_name"].strip().lower()
            for lead in existing_leads
            if lead.get("business_name")
        }

        existing_websites = {
            lead["website"].strip().lower().rstrip("/")
            for lead in existing_leads
            if lead.get("website")
        }

        # Remove businesses already stored in Neon
        new_leads = []

        for lead in discovered_leads:
            business_name = (
                lead.get("business_name") or ""
            ).strip().lower()

            website = (
                lead.get("website") or ""
            ).strip().lower().rstrip("/")

            already_exists = (
                business_name in existing_names
                or (
                    website
                    and website in existing_websites
                )
            )

            if not already_exists:
                new_leads.append(lead)

        return {
            "discovered_leads": new_leads
        }

    except Exception as e:
        print(f"Lead extraction failed: {str(e)}")

        return {
            "discovered_leads": []
        }