from typing import TypedDict, List, Optional

class LeadAgentState(TypedDict):
    industry: str
    city: str

    # Optional search constraints
    business_type: Optional[str] = None
    keywords: List[str] = []
    exclude_keywords: List[str] = []

    # Lead quality requirements
    require_website: bool = True
    require_contact: bool = True
    require_whatsapp: bool = False
    require_official_source: bool = True

    # Search configuration
    search_queries: List[str] = []
    search_results: List[any]

    existing_leads: List[dict]
    excluded_businesses: List[str]
    
    # Agent working state
    discovered_leads: List[dict] = []
    verified_leads: List[dict] = []
    rejected_leads: List[dict] = []

    # Final output
    leads: List[dict] = []