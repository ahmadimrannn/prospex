from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from graph.execute_graph import execute_graph


app = FastAPI(
    title="Lead Generation Agent",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

    max_leads: int = Field(default=10, ge=1, le=100)


class LeadGenerationResponse(BaseModel):
    thread_id: UUID
    leads: list[dict]


@app.post(
    "/leads/generate",
    response_model=LeadGenerationResponse,
    status_code=status.HTTP_200_OK,
)
def generate_leads(request: LeadGenerationRequest):
    """
    Generate verified business leads for an industry and city.
    """

    thread_id = uuid4()

    try:
        result = execute_graph(
            request=request,
            thread_id=thread_id,
        )

        return result

    except Exception as e:
        # Log the actual exception internally in production.
        print(
            f"Lead generation failed "
            f"(thread_id={thread_id}): {str(e)}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lead generation failed.",
        )
