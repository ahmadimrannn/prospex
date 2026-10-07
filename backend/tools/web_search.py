from exa_py import Exa
from dotenv import load_dotenv

load_dotenv()

exa = Exa()

exa_system_prompt = """
Search for real, currently operating businesses that match the query.

Prioritize:
- Official business websites
- Official business social media profiles
- Reputable business directories and listings
- Pages containing direct business contact information

Prefer primary and authoritative sources over articles, aggregators, scraped pages, and generic content.

When multiple results refer to the same business, prefer the most authoritative source and avoid duplicate results.

Do not return irrelevant businesses, businesses outside the requested location, or results that only mention a business without providing useful information about it.

Prioritize results that contain evidence useful for verifying:
- Business name
- Industry
- City/location
- Official website
- Public business contact information
- WhatsApp availability when relevant to the query

Do not infer or fabricate missing information.
"""


def web_search(query: str):
    """Search the web for potential business leads and supporting evidence."""

    results = exa.search(
        query=query,
        system_prompt=exa_system_prompt,
        num_results=7,
        contents={
            "highlights": True,
            "text": True,
        },
    )

    return results