from urllib.parse import urlparse

from config.llm import model
from graph.schemas.schema import VerifiedLeadList
from graph.state.state import LeadAgentState
from graph.prompts.prompts import generate_lead_verification_prompt


lead_verification_structured_llm = model.with_structured_output(
    VerifiedLeadList
)


def normalize_text(value: str | None) -> str:
    """
    Normalize text for deterministic comparisons.
    """
    if not value:
        return ""

    return " ".join(
        value.strip().lower().split()
    )


def has_valid_website(value: str | None) -> bool:
    """
    Check whether a lead contains a real website URL.
    """

    if not value:
        return False

    value = value.strip()

    if not value:
        return False

    invalid_values = {
        "n/a",
        "na",
        "none",
        "null",
        "unknown",
        "not available",
        "not found",
        "-",
    }

    if value.lower() in invalid_values:
        return False

    try:
        parsed = urlparse(value)

        return (
            parsed.scheme in {"http", "https"}
            and bool(parsed.netloc)
        )

    except Exception:
        return False


def has_valid_contact(value: str | None) -> bool:
    """
    Check whether a lead contains usable public contact data.
    """

    if not value:
        return False

    value = value.strip()

    if not value:
        return False

    invalid_values = {
        "n/a",
        "na",
        "none",
        "null",
        "unknown",
        "not available",
        "not found",
        "-",
    }

    return value.lower() not in invalid_values


def reject_lead(
    lead_data: dict,
    reason: str,
) -> dict:
    """
    Add deterministic rejection information.
    """

    return {
        **lead_data,
        "status": "unverified",
        "verification_notes": [
            *lead_data.get("verification_notes", []),
            reason,
        ],
    }


def lead_verification_node(
    state: LeadAgentState,
):
    """
    Verify extracted leads using LLM evidence verification,
    followed by deterministic validation of hard requirements.

    The LLM evaluates evidence.
    Python enforces hard business constraints.
    """

    leads = state["discovered_leads"]
    search_results = state["search_results"]

    if not leads:
        return {
            "verified_leads": [],
            "rejected_leads": [],
        }

    prompt = generate_lead_verification_prompt(
        leads=leads,
        search_results=search_results,
    )

    try:
        res = lead_verification_structured_llm.invoke(prompt)

        verified_leads = []
        rejected_leads = []

        requested_city = normalize_text(
            state["city"]
        )

        requested_industry = normalize_text(
            state["industry"]
        )

        for lead in res.leads:

            lead_data = lead.model_dump()

            # -------------------------------------------------
            # LLM VERIFICATION
            # -------------------------------------------------

            if lead.status != "verified":
                rejected_leads.append(
                    lead_data
                )
                continue

            lead_city = normalize_text(
                lead.city
            )

            lead_industry = normalize_text(
                lead.industry
            )

            # -------------------------------------------------
            # HARD RULE 1: CITY
            # -------------------------------------------------

            if lead_city != requested_city:

                rejected_leads.append(
                    reject_lead(
                        lead_data,
                        (
                            f"City mismatch. "
                            f"Requested '{state['city']}', "
                            f"but lead is in "
                            f"'{lead.city}'."
                        ),
                    )
                )

                continue

            # -------------------------------------------------
            # HARD RULE 2: INDUSTRY
            # -------------------------------------------------

            if lead_industry != requested_industry:

                rejected_leads.append(
                    reject_lead(
                        lead_data,
                        (
                            f"Industry mismatch. "
                            f"Requested '{state['industry']}', "
                            f"but lead is categorized as "
                            f"'{lead.industry}'."
                        ),
                    )
                )

                continue

            # -------------------------------------------------
            # HARD RULE 3: WEBSITE
            # -------------------------------------------------

            if state["require_website"]:

                if not has_valid_website(
                    lead.website
                ):

                    rejected_leads.append(
                        reject_lead(
                            lead_data,
                            (
                                "Website is required "
                                "but no valid website "
                                "was verified."
                            ),
                        )
                    )

                    continue

            # -------------------------------------------------
            # HARD RULE 4: CONTACT
            # -------------------------------------------------

            if state["require_contact"]:

                if not has_valid_contact(
                    lead.contact
                ):

                    rejected_leads.append(
                        reject_lead(
                            lead_data,
                            (
                                "Contact information is "
                                "required but was not verified."
                            ),
                        )
                    )

                    continue

            # -------------------------------------------------
            # HARD RULE 5: WHATSAPP
            # -------------------------------------------------

            if state["require_whatsapp"]:

                if not lead.whatsapp_evidence:

                    rejected_leads.append(
                        reject_lead(
                            lead_data,
                            (
                                "WhatsApp evidence is "
                                "required but was not verified."
                            ),
                        )
                    )

                    continue

            # -------------------------------------------------
            # HARD RULE 6: OFFICIAL SOURCE
            # -------------------------------------------------

            if state["require_official_source"]:

                if not lead.source:

                    rejected_leads.append(
                        reject_lead(
                            lead_data,
                            (
                                "An official source is "
                                "required but was not provided."
                            ),
                        )
                    )

                    continue

            # -------------------------------------------------
            # PASSED ALL CHECKS
            # -------------------------------------------------

            verified_leads.append(
                lead_data
            )

            # Respect requested maximum.
            if len(verified_leads) >= state["max_leads"]:
                break

        return {
            "verified_leads": verified_leads,
            "rejected_leads": rejected_leads,
        }

    except Exception as e:

        print(
            f"Lead verification failed: {e}"
        )

        return {
            "verified_leads": [],
            "rejected_leads": leads,
        }