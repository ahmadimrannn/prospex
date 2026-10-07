from graph.state import LeadAgentState
from tools.leads import fetch_existing_leads


def query_generation_node(state: LeadAgentState):
    """Fetch existing leads and generate targeted search queries."""

    industry = state["industry"]
    city = state["city"]

    # Fetch businesses already stored in Neon
    existing_leads = fetch_existing_leads(
        industry=industry,
        city=city,
    )

    # Extract existing business names
    excluded_businesses = [
        lead["business_name"]
        for lead in existing_leads
        if lead.get("business_name")
    ]

    # queries = [
    #     f"{industry} in {city} official website",
    #     f"{industry} in {city} contact",
    #     f"{industry} in {city} phone email",
    #     f"{industry} {city} address",
    #     f'{industry} {city} "contact us"',
    # ]

    # if state["require_whatsapp"]:
    #     queries.extend([
    #         f"{industry} {city} WhatsApp",
    #         f'{industry} {city} "WhatsApp" contact',
    #     ])

    queries = [
        f'{industry} businesses in {city} official website',
    ]

    # Only perform an additional search when WhatsApp evidence is explicitly required.
    if state["require_whatsapp"]:
        queries.append(
            f'{industry} businesses in {city} WhatsApp'
        )

    return {
        "search_queries": queries,
        "existing_leads": existing_leads,
        "excluded_businesses": excluded_businesses,
    }