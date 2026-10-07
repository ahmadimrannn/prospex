from config.database_config import fetch_all, execute


def fetch_existing_leads(
    industry: str,
    city: str,
) -> list[dict]:
    query = """
        SELECT
            id,
            business_name,
            industry,
            city,
            website,
            contact,
            whatsapp_evidence,
            source,
            status,
            verification_score,
            verification_notes,
            missing_fields,
            created_at,
            updated_at
        FROM leads
        WHERE LOWER(industry) = LOWER(%s)
          AND LOWER(city) = LOWER(%s)
    """

    rows = fetch_all(query, (industry, city))

    return [dict(row) for row in rows]


def insert_lead(lead: dict) -> None:
    query = """
        INSERT INTO leads (
            business_name,
            industry,
            city,
            website,
            contact,
            whatsapp_evidence,
            source,
            status,
            verification_score,
            verification_notes,
            missing_fields
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT DO NOTHING
    """

    execute(
        query,
        (
            lead["business_name"],
            lead["industry"],
            lead["city"],
            lead.get("website"),
            lead.get("contact"),
            lead.get("whatsapp_evidence"),
            lead["source"],
            lead["status"],
            lead.get("verification_score"),
            lead.get("verification_notes", []),
            lead.get("missing_fields", []),
        ),
    )