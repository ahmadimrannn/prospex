import re
from urllib.parse import urlparse

import requests

from config.hubspot_config import headers
from config.settings import HUBSPOT_INDUSTRY_MAP


HUBSPOT_API_BASE = "https://api.hubapi.com"
HUBSPOT_API_VERSION = "2026-09"


# HUBSPOT HELPER FUNCTIONS
def extract_domain(website: str | None) -> str | None:
    """Extract a clean domain from a website URL."""

    if not website:
        return None

    website = website.strip()

    if not website:
        return None

    if not website.startswith(("http://", "https://")):
        website = f"https://{website}"

    try:
        domain = urlparse(website).netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain or None

    except Exception:
        return None


def is_email(value: str | None) -> bool:
    """Return True when the value looks like an email address."""

    if not value:
        return False

    return bool(
        re.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            value.strip(),
        )
    )


def is_phone(value: str | None) -> bool:
    """Return True when the value looks like a phone number."""

    if not value:
        return False

    digits = re.sub(r"\D", "", value)

    return len(digits) >= 7

def normalize_hubspot_industry(industry: str | None) -> str | None:
    """
    Convert the AI-generated industry into a valid HubSpot
    industry enumeration value.

    Returns None when the industry cannot be safely mapped.
    """

    if not industry:
        return None

    normalized = industry.strip().lower()

    return HUBSPOT_INDUSTRY_MAP.get(normalized)

# COMPANY
def create_company(
    company_name: str,
    company_domain: str | None,
    industry: str | None = None,
    city: str | None = None,
):
    if not company_name:
        print("Cannot create company without a company name.")
        return None

    url = (
        f"{HUBSPOT_API_BASE}/crm/objects/"
        f"{HUBSPOT_API_VERSION}/companies"
    )

    properties = {
        "name": company_name,
    }

    # Website/domain
    if company_domain:
        properties["domain"] = company_domain

    # Normalize AI-generated industry into a valid
    # HubSpot enumeration value.
    hubspot_industry = normalize_hubspot_industry(industry)

    if hubspot_industry:
        properties["industry"] = hubspot_industry
    elif industry:
        print(
            f"Skipping unsupported HubSpot industry value: "
            f"{industry}"
        )

    # City is a free-text HubSpot company property.
    if city:
        properties["city"] = city

    payload = {
        "properties": properties
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

        company_id = response.json().get("id")

        print(
            f"HubSpot company created successfully: "
            f"{company_name} ({company_id})"
        )

        return company_id

    except requests.exceptions.RequestException as e:
        error_details = (
            e.response.text
            if e.response is not None
            else str(e)
        )

        print(
            f"HubSpot API error while creating company: "
            f"{error_details}"
        )

        return None

def search_company_by_name(company_name: str):
    """Find a HubSpot company by exact company name."""

    if not company_name:
        return None

    url = (
        f"{HUBSPOT_API_BASE}"
        f"/crm/objects/{HUBSPOT_API_VERSION}/companies/search"
    )

    payload = {
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "name",
                        "operator": "EQ",
                        "value": company_name,
                    }
                ]
            }
        ],
        "properties": [
            "name",
            "domain",
        ],
        "limit": 1,
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

        results = response.json().get("results", [])

        if results:
            return results[0]["id"]

        return None

    except requests.exceptions.RequestException as e:
        print(
            f"HubSpot API error while searching company "
            f"{company_name}: {e}"
        )

        return None


def search_company_by_domain(company_domain: str):
    """Find a HubSpot company by exact domain."""

    if not company_domain:
        return None

    url = (
        f"{HUBSPOT_API_BASE}"
        f"/crm/objects/{HUBSPOT_API_VERSION}/companies/search"
    )

    payload = {
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "domain",
                        "operator": "EQ",
                        "value": company_domain,
                    }
                ]
            }
        ],
        "properties": [
            "name",
            "domain",
        ],
        "limit": 1,
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

        results = response.json().get("results", [])

        if results:
            return results[0]["id"]

        return None

    except requests.exceptions.RequestException as e:
        print(
            f"HubSpot API error while searching company "
            f"domain {company_domain}: {e}"
        )

        return None


def update_company(
    company_id: str,
    company_name: str,
    company_domain: str | None,
):
    """Update an existing HubSpot company."""

    if not company_id or not company_name:
        return None

    url = (
        f"{HUBSPOT_API_BASE}"
        f"/crm/v3/objects/companies/{company_id}"
    )

    properties = {
        "name": company_name,
    }

    if company_domain:
        properties["domain"] = company_domain

    payload = {
        "properties": properties
    }

    try:
        response = requests.patch(
            url=url,
            headers=headers,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

        return response.json().get("id")

    except requests.exceptions.RequestException as e:
        print(
            f"HubSpot API error while updating company: {e}"
        )

        return None


def create_or_update_company(
    company_name: str,
    company_domain: str | None,
):
    """
    Find an existing company by domain first, then name.

    If found, return the existing company ID.
    Otherwise create a new company.
    """

    if not company_name:
        return None

    # Domain is the strongest company identity.
    if company_domain:
        company_id = search_company_by_domain(
            company_domain
        )

        if company_id:
            print(
                f"Company already exists by domain: "
                f"{company_name}"
            )
            return company_id

    # Fallback to company name.
    company_id = search_company_by_name(company_name)

    if company_id:
        print(
            f"Company already exists by name: "
            f"{company_name}"
        )
        return company_id

    # Company does not exist.
    print(f"Creating company: {company_name}")

    return create_company(
        company_name=company_name,
        company_domain=company_domain,
    )


# CONTACT
def create_contact(
    firstname: str,
    lastname: str,
    email: str | None = None,
    phone: str | None = None,
):
    """Create a HubSpot contact."""

    if not email and not phone:
        print(
            "Cannot create contact without email or phone."
        )
        return None

    url = (
        f"{HUBSPOT_API_BASE}"
        f"/crm/v3/objects/contacts"
    )

    properties = {
        "firstname": firstname,
        "lastname": lastname,
    }

    if email:
        properties["email"] = email

    if phone:
        properties["phone"] = phone

    payload = {
        "properties": properties
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

        return response.json().get("id")

    except requests.exceptions.RequestException as e:
        error_details = (
            e.response.text
            if e.response is not None
            else str(e)
        )

        print(
            f"HubSpot API error while creating contact: "
            f"{error_details}"
        )

        return None


def search_contact_by_email(email: str):
    """Find a HubSpot contact by email."""

    if not email:
        return None

    email = email.strip().lower()

    url = (
        f"{HUBSPOT_API_BASE}"
        f"/crm/objects/{HUBSPOT_API_VERSION}/contacts/search"
    )

    payload = {
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "email",
                        "operator": "EQ",
                        "value": email,
                    }
                ]
            }
        ],
        "properties": [
            "firstname",
            "lastname",
            "email",
            "phone",
        ],
        "limit": 1,
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

        results = response.json().get("results", [])

        if results:
            return results[0]["id"]

        return None

    except requests.exceptions.RequestException as e:
        print(
            f"HubSpot API error while searching contact "
            f"by email: {e}"
        )

        return None


def search_contact_by_phone(phone: str):
    """Find a HubSpot contact by phone."""

    if not phone:
        return None

    url = (
        f"{HUBSPOT_API_BASE}"
        f"/crm/objects/{HUBSPOT_API_VERSION}/contacts/search"
    )

    payload = {
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "phone",
                        "operator": "EQ",
                        "value": phone,
                    }
                ]
            }
        ],
        "properties": [
            "firstname",
            "lastname",
            "email",
            "phone",
        ],
        "limit": 1,
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

        results = response.json().get("results", [])

        if results:
            return results[0]["id"]

        return None

    except requests.exceptions.RequestException as e:
        print(
            f"HubSpot API error while searching contact "
            f"by phone: {e}"
        )

        return None


def update_contact(
    contact_id: str,
    firstname: str,
    lastname: str,
    email: str | None = None,
    phone: str | None = None,
):
    """Update an existing HubSpot contact."""

    if not contact_id:
        return None

    url = (
        f"{HUBSPOT_API_BASE}"
        f"/crm/v3/objects/contacts/{contact_id}"
    )

    properties = {
        "firstname": firstname,
        "lastname": lastname,
    }

    if email:
        properties["email"] = email

    if phone:
        properties["phone"] = phone

    payload = {
        "properties": properties
    }

    try:
        response = requests.patch(
            url=url,
            headers=headers,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

        return response.json().get("id")

    except requests.exceptions.RequestException as e:
        print(
            f"HubSpot API error while updating contact: {e}"
        )

        return None


def create_or_update_contact(
    firstname: str,
    lastname: str,
    email: str | None = None,
    phone: str | None = None,
):
    """
    Find an existing contact by email or phone.

    If found, return the existing contact ID.
    Otherwise create a new contact.
    """

    contact_id = None

    if email:
        contact_id = search_contact_by_email(email)

    if not contact_id and phone:
        contact_id = search_contact_by_phone(phone)

    if contact_id:
        print("Contact already exists. Updating contact.")

        return update_contact(
            contact_id=contact_id,
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone=phone,
        )

    print("Creating new contact.")

    return create_contact(
        firstname=firstname,
        lastname=lastname,
        email=email,
        phone=phone,
    )


# ASSOCIATION
def associate_contact_with_company(
    contact_id: str,
    company_id: str,
):
    """Associate an existing Contact with an existing Company."""

    if not contact_id or not company_id:
        print(
            "Cannot create association without "
            "contact_id and company_id."
        )
        return False

    url = (
        f"{HUBSPOT_API_BASE}"
        f"/crm/objects/{HUBSPOT_API_VERSION}"
        f"/contacts/{contact_id}"
        f"/associations/default/companies/{company_id}"
    )

    try:
        response = requests.put(
            url=url,
            headers=headers,
            timeout=10,
        )

        response.raise_for_status()

        return True

    except requests.exceptions.RequestException as e:
        print(
            f"HubSpot API error while associating "
            f"contact with company: {e}"
        )

        return False


def write_lead_to_hubspot(lead: dict) -> dict:
    """
    Write one verified lead into HubSpot.

    IMPORTANT:
    If the company already exists in HubSpot, the lead is
    considered already present and NOTHING is written again.
    """

    if not lead:
        return {
            "success": False,
            "status": "skipped",
            "reason": "Empty lead.",
        }

    # Only verified leads enter CRM.
    if lead.get("status") != "verified":
        return {
            "success": False,
            "status": "skipped",
            "reason": "Lead is not verified.",
            "business_name": lead.get("business_name"),
        }

    business_name = lead.get("business_name")
    industry = lead.get("industry")
    city = lead.get("city")
    website = lead.get("website")
    contact = lead.get("contact")

    if not business_name:
        return {
            "success": False,
            "status": "skipped",
            "reason": "Business name is missing.",
        }

    domain = extract_domain(website)

    # CHECK EXISTING COMPANY BEFORE WRITING ANYTHING
    existing_company_id = None

    # First check by domain.
    if domain:
        existing_company_id = search_company_by_domain(domain)

    # Fallback to company name.
    if not existing_company_id:
        existing_company_id = search_company_by_name(
            business_name
        )

    # If company already exists, DO NOT WRITE THE LEAD AGAIN.
    if existing_company_id:
        print(
            f"Lead already exists in HubSpot: "
            f"{business_name}. Skipping."
        )

        return {
            "success": True,
            "status": "already_exists",
            "business_name": business_name,
            "company_id": existing_company_id,
            "contact_id": None,
            "association_created": False,
        }

    # CREATE COMPANY
    company_id = create_company(
        company_name=business_name,
        company_domain=domain,
        industry=industry,
        city=city,
    )

    if not company_id:
        return {
            "success": False,
            "status": "failed",
            "reason": "Failed to create company.",
            "business_name": business_name,
        }

    # CREATE CONTACT IF CONTACT DATA IS USABLE
    contact_id = None

    if contact:
        contact = contact.strip()

        if is_email(contact):
            contact_id = create_or_update_contact(
                firstname=business_name,
                lastname="",
                email=contact,
            )

        elif is_phone(contact):
            contact_id = create_or_update_contact(
                firstname=business_name,
                lastname="",
                phone=contact,
            )

    # ASSOCIATE CONTACT WITH COMPANY
    association_created = False

    if contact_id:
        association_created = associate_contact_with_company(
            contact_id=contact_id,
            company_id=company_id,
        )

    return {
        "success": True,
        "status": "created",
        "business_name": business_name,
        "company_id": company_id,
        "contact_id": contact_id,
        "association_created": association_created,
    }


def write_leads_to_hubspot(leads: list[dict]) -> dict:
    """
        Write verified leads into HubSpot.

        Existing leads are skipped automatically.
        One failure does not stop the remaining leads.

        Returns:
            Summary containing counts, overall status,
            frontend message, and individual results.
    """

    results = []

    for lead in leads:
        try:
            result = write_lead_to_hubspot(lead)

        except Exception as e:
            result = {
                "success": False,
                "status": "failed",
                "business_name": lead.get("business_name"),
                "reason": str(e),
            }

        results.append(result)

    created = [
        result
        for result in results
        if result.get("status") == "created"
    ]

    already_exists = [
        result
        for result in results
        if result.get("status") == "already_exists"
    ]

    failed = [
        result
        for result in results
        if result.get("status") == "failed"
    ]

    skipped = [
        result
        for result in results
        if result.get("status") == "skipped"
    ]

    total = len(leads)

    created_count = len(created)
    already_exists_count = len(already_exists)
    failed_count = len(failed)
    skipped_count = len(skipped)

    # Determine overall CRM write status.
    if created_count > 0 and failed_count == 0:
        if already_exists_count > 0:
            status = "partial"
            message = (
                "New leads were written into CRM successfully. "
                "Some leads already existed."
            )
        else:
            status = "created"
            message = (
                "New leads are written into CRM successfully."
            )

    elif created_count > 0 and failed_count > 0:
        status = "partial"
        message = (
            "Some leads were written into CRM, "
            "but some leads could not be written."
        )

    elif created_count == 0 and already_exists_count == total:
        status = "already_exists"
        message = (
            "No new leads were written. "
            "All leads already exist in CRM."
        )

    elif created_count == 0 and failed_count > 0:
        status = "failed"
        message = (
            "No leads were written into CRM. "
            "Some leads failed to write."
        )

    elif created_count == 0 and skipped_count == total:
        status = "skipped"
        message = (
            "No leads were written into CRM. "
            "All leads were skipped."
        )

    else:
        status = "partial"
        message = (
            "Lead processing completed, "
            "but no new leads were written."
        )

    return {
        "success": created_count > 0,
        "status": status,
        "message": message,

        "total": total,
        "created": created_count,
        "already_exists": already_exists_count,
        "failed": failed_count,
        "skipped": skipped_count,

        "results": results,
    }

# NOTE
def write_note(
    contact_id: str,
    note: str,
    company_id: str | None = None,
) -> bool:
    """Write a note to a contact and optionally its company."""

    if not contact_id or not note:
        print(
            "Cannot write note without contact_id "
            "and note content."
        )
        return False

    from datetime import datetime, timezone

    now_utc = datetime.now(timezone.utc)

    formatted_timestamp = (
        now_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        + "Z"
    )

    url = (
        f"{HUBSPOT_API_BASE}"
        f"/crm/objects/{HUBSPOT_API_VERSION}/notes"
    )

    associations = [
        {
            "to": {
                "id": str(contact_id),
            },
            "types": [
                {
                    "associationCategory": "HUBSPOT_DEFINED",
                    "associationTypeId": 202,
                }
            ],
        }
    ]

    if company_id:
        associations.append(
            {
                "to": {
                    "id": str(company_id),
                },
                "types": [
                    {
                        "associationCategory": "HUBSPOT_DEFINED",
                        "associationTypeId": 190,
                    }
                ],
            }
        )

    payload = {
        "properties": {
            "hs_timestamp": formatted_timestamp,
            "hs_note_body": str(note),
        },
        "associations": associations,
    }

    try:
        response = requests.post(
            url=url,
            json=payload,
            headers=headers,
            timeout=10,
        )

        response.raise_for_status()

        return True

    except requests.exceptions.RequestException as e:
        error_details = (
            e.response.text
            if e.response is not None
            else str(e)
        )

        print(
            f"HubSpot API error while writing note: "
            f"{error_details}"
        )

        return False