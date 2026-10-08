import os
from dotenv import load_dotenv

load_dotenv()

HUBSPOT_ACCESS_TOKEN = os.getenv("HUBSPOT_SERVICE_KEY")

if not HUBSPOT_ACCESS_TOKEN:
    raise RuntimeError(
        "HUBSPOT_SERVICE_KEY is not set in the environment."
    )

headers = {
    "Authorization": f"Bearer {HUBSPOT_ACCESS_TOKEN}",
    "Content-Type": "application/json",
}