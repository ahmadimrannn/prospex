import os
import secrets
from uuid import UUID, uuid4

from dotenv import load_dotenv

load_dotenv()

API_ACCESS_TOKEN = os.getenv("API_ACCESS_TOKEN")
if not API_ACCESS_TOKEN or not API_ACCESS_TOKEN.strip():
    raise RuntimeError(
        "API_ACCESS_TOKEN environment variable is missing or empty. "
        "Server cannot start unprotected."
    )

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from graph.execute_graph import execute_graph

security = HTTPBearer(auto_error=False)


def verify_access_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> None:
    if not credentials or not secrets.compare_digest(credentials.credentials, API_ACCESS_TOKEN):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing access token",
            headers={"WWW-Authenticate": "Bearer"},
        )


app = FastAPI(
    title="Lead Generation Agent",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://prospex-toua.vercel.app", "http://localhost:3000", "http://localhost:8000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
)
def health_check():
    """
    Open health check route accessible without authentication.
    """
    return {"status": "ok"}



class LeadGenerationRequest(BaseModel):
    industry: str = Field(..., min_length=1, max_length=200)
    city: str = Field(..., min_length=1, max_length=200)

    business_type: str | None = Field(
        default=None,
        max_length=200,
    )

    keywords: list[str] = Field(default_factory=list)
    exclude_keywords: list[str] = Field(default_factory=list)

    require_website: bool
    require_contact: bool
    require_whatsapp: bool

    require_official_source: bool



class LeadGenerationResponse(BaseModel):
    thread_id: UUID
    success: bool
    status: str
    message: str
    leads: list[dict]


@app.post(
    "/leads/generate",
    response_model=LeadGenerationResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_access_token)],
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
