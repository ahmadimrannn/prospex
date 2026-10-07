from config.llm import model
from graph.schemas.schema import VerifiedLeadList
from graph.state.state import LeadAgentState
from graph.prompts.prompts import generate_lead_verification_prompt


lead_verification_structured_llm = model.with_structured_output(
    VerifiedLeadList
)

def lead_verification_node(state: LeadAgentState):
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

        for lead in res.leads:
            lead_data = lead.model_dump()

            if lead.status == "verified":
                verified_leads.append(lead_data)
            else:
                rejected_leads.append(lead_data)

        return {
            "verified_leads": verified_leads,
            "rejected_leads": rejected_leads,
        }

    except Exception as e:
        print(f"Lead verification failed: {e}")

        return {
            "verified_leads": [],
            "rejected_leads": leads,
        }