from graph.state.state import LeadAgentState
from tools.leads import fetch_existing_leads


def query_generation_node(state: LeadAgentState):
    """Fetch existing leads and generate queries based on lead requirements."""

    industry = state["industry"].strip()
    city = state["city"].strip()

    require_website = state.get("require_website", False)
    require_contact = state.get("require_contact", False)
    require_official_source = state.get("require_official_source", True)

    # Fetch existing leads from Neon for this industry and city.
    existing_leads = fetch_existing_leads(
        industry=industry,
        city=city,
    )

    excluded_businesses = [
        lead["business_name"].strip()
        for lead in existing_leads
        if lead.get("business_name")
        and lead["business_name"].strip()
    ]

    # Generate focused queries based on the requested requirements.
    queries = []

    # Always search for businesses matching the requested industry and city.
    if require_website or require_official_source:
        queries.append(
            f'{industry} businesses in {city} official website'
        )
    else:
        queries.append(
            f'{industry} businesses in {city}'
        )

    # Search for contact information only when it is required.
    if require_contact:
        queries.append(
            f'{industry} businesses in {city} phone email contact details, and WhatsApp contact'
        )

    # Look for official social profiles when an official source is required.
    if require_official_source:
        queries.append(
            f'{industry} businesses in {city} official Facebook Instagram'
        )

    # If a website is required, search for businesses with their own domains.
    if require_website:
        queries.append(
            f'{industry} in {city} business website contact us'
        )

    # Remove duplicate queries while preserving order.
    queries = list(dict.fromkeys(queries))

    return {
        "search_queries": queries,
        "existing_leads": existing_leads,
        "excluded_businesses": excluded_businesses,
    }