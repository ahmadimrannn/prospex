from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from graph.graph_builder import graph

class LeadGenerationRequest(BaseModel):
    industry: str = Field(..., min_length=1, max_length=200)
    city: str = Field(..., min_length=1, max_length=200)

    business_type: str | None = Field(
        default=None,
        max_length=200,
    )

    keywords: list[str] = Field(default_factory=list)
    exclude_keywords: list[str] = Field(default_factory=list)

    require_website: bool = True
    require_contact: bool = True
    require_whatsapp: bool = False

    min_sources: int = Field(default=2, ge=1)
    require_official_source: bool = True

    max_leads: int = Field(default=20, ge=1, le=100)

# -----------------------------
# Graph Execution
# -----------------------------

def execute_graph(
    request: LeadGenerationRequest,
    thread_id: UUID | None = None,
) -> dict:
    """
    Execute the lead-generation LangGraph with a unique thread ID.
    """

    thread_id = thread_id or uuid4()

    initial_state = {
        "industry": request.industry,
        "city": request.city,

        "business_type": request.business_type,
        "keywords": request.keywords,
        "exclude_keywords": request.exclude_keywords,

        "require_website": request.require_website,
        "require_contact": request.require_contact,
        "require_whatsapp": request.require_whatsapp,

        "min_sources": request.min_sources,
        "require_official_source": request.require_official_source,

        "max_leads": request.max_leads,

        "search_queries": [],
        "search_results": [],

        "existing_leads": [],
        "excluded_businesses": [],

        "discovered_leads": [],
        "verified_leads": [],
        "rejected_leads": [],

        "leads": [],
    }

    config = {
        "configurable": {
            "thread_id": str(thread_id),
        }
    }

    result = graph.invoke(
        initial_state,
        config=config,
    )

    return {
        "thread_id": thread_id,
        "leads": result.get("leads", []),
    }