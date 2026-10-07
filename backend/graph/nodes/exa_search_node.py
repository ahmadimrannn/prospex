from graph.state.state import LeadAgentState
from tools.web_search import web_search


def exa_search_node(state: LeadAgentState):
    """Search Exa while excluding businesses already stored in Neon."""

    queries = state["search_queries"]
    excluded_businesses = state["excluded_businesses"]

    all_results = []

    for query in queries:

        if excluded_businesses:
            exclusions = ", ".join(
                f'"{business}"'
                for business in excluded_businesses
            )

            query = (
                f"{query}. "
                f"Do not return these businesses: {exclusions}"
            )

        results = web_search(query)

        all_results.extend(results.results)

    return {
        "search_results": all_results
    }