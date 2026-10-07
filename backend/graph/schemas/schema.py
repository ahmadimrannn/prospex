from typing import Optional, Literal, List
from pydantic import BaseModel, Field


class LeadData(BaseModel):
    business_name: Optional[str] = Field(
        default=None,
        description="The official or publicly listed name of the business."
    )

    industry: str = Field(
        description="The primary industry or business category the company operates in, such as restaurant, real estate, software development, healthcare, or retail."
    )

    city: str = Field(
        description="The city where the business is located or primarily operates."
    )

    website: Optional[str] = Field(
        default=None,
        description="The official business website URL. Use null if no reliable official website can be found."
    )

    contact: Optional[str] = Field(
        description="A publicly available business contact method, such as a phone number, email address, or other official contact information."
    )

    whatsapp_evidence: Optional[str] = Field(
        default=None,
        description="Evidence that the business has a publicly available WhatsApp contact, such as a WhatsApp link, WhatsApp-enabled phone number, or explicit WhatsApp mention on an official business page. Use null if no reliable evidence is found."
    )

    source: str = Field(
        description="The URL or source where the lead information was found and can be independently verified."
    )

    status: Literal["verified", "unverified", "partial"] = Field(
        description="Lead verification status: 'verified' when the key business details are supported by reliable public sources; 'partial' when some details are verified but important information is missing or uncertain; 'unverified' when the information could not be reliably confirmed."
    )


class LeadDataList(BaseModel):
    leads: List[LeadData]


class VerifiedLead(BaseModel):
    business_name: Optional[str] = Field(
        default=None,
        description="The official/public business name supported by the evidence."
    )

    industry: Optional[str] = Field(
        default=None,
        description="The primary industry or business category supported by the evidence."
    )

    city: Optional[str] = Field(
        default=None,
        description="The city where the business operates, based on reliable evidence."
    )

    website: Optional[str] = Field(
        default=None,
        description="The official business website. Must be supported by evidence."
    )

    contact: Optional[str] = Field(
        default=None,
        description="A publicly available business contact such as phone number, email, or official contact page."
    )

    whatsapp_evidence: Optional[str] = Field(
        default=None,
        description="Explicit evidence that the business uses WhatsApp, such as a wa.me link, WhatsApp button, or explicit WhatsApp statement."
    )

    source: Optional[str] = Field(
        default=None,
        description="The strongest source URL supporting the verified business information."
    )

    status: Literal["verified", "partial", "unverified"] = Field(
        description="Verification result based strictly on the available evidence."
    )

    verification_score: int = Field(
        ge=0,
        le=100,
        description="Evidence-based verification score from 0 to 100."
    )

    verification_notes: List[str] = Field(
        default_factory=list,
        description="Specific evidence and reasoning supporting the verification decision."
    )

    missing_fields: List[str] = Field(
        default_factory=list,
        description="Important fields that could not be reliably verified."
    )

class VerifiedLeadList(BaseModel):
    leads: List[VerifiedLead]