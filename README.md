# Lead Intelligence & CRM Automation

An agentic lead-generation pipeline that discovers, verifies, and writes business leads to a centralized CRM based on industry and city.

The system is designed to reduce manual lead research by combining web search, structured extraction, verification, persistence, and CRM synchronization into a single LangGraph workflow.

---

## Overview

Traditional lead-generation workflows usually require manually searching for businesses, opening websites, collecting contact information, checking social presence, looking for publicly available WhatsApp evidence, and then copying the results into a CRM.

This project automates that workflow.

Given an **industry** and **city**, the system:

1. Generates targeted search queries.
2. Searches the web for relevant businesses.
3. Extracts structured business information.
4. Verifies the collected information against available evidence.
5. Persists the final leads in PostgreSQL.
6. Writes verified leads to HubSpot CRM.

The workflow is implemented as a **4-node LangGraph agent** with PostgreSQL persistence and Gemini-powered reasoning.

---

## System Architecture

```text
                         ┌──────────────────────┐
                         │   User / API Client  │
                         │ Industry + City      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Query Generation    │
                         │                      │
                         │ Existing lead check  │
                         │ Search query creation│
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Lead Discovery     │
                         │                      │
                         │       Exa API        │
                         │    Web discovery     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Lead Verification    │
                         │                      │
                         │ Gemini LLM           │
                         │ Evidence validation  │
                         │ Data normalization   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Lead Finalization  │
                         │                      │
                         │ PostgreSQL / Neon    │
                         │ HubSpot CRM           │
                         └──────────────────────┘
```

---

## Core Workflow

The LangGraph workflow contains four primary nodes:

### 1. Query Generation

The workflow receives:

```text
Industry
City
```

The node checks existing leads stored in PostgreSQL and generates targeted search queries.

Existing businesses can be excluded from subsequent discovery to reduce duplicate lead generation.

---

### 2. Lead Discovery

The discovery node uses the **Exa API** to search the web for relevant businesses.

The search process focuses on discovering businesses that match the requested:

* Industry
* City
* Business identity
* Website
* Public contact information
* Public social presence
* Publicly available WhatsApp evidence

The discovery stage is intentionally separated from verification.

Search results are treated as **candidate evidence**, not automatically as verified leads.

---

### 3. Lead Verification

Candidate businesses are passed through a verification stage powered by **Gemini**.

The verification process evaluates the available evidence and produces structured lead information.

The system is designed to distinguish between:

```text
Discovered
    ↓
Candidate
    ↓
Evidence collected
    ↓
Verified
```

rather than treating every search result as a valid lead.

The verification stage focuses on preventing common lead-generation failures such as:

* Incorrect businesses
* Duplicate businesses
* Incorrect locations
* Unsupported contact information
* Fabricated contact details
* Unsupported WhatsApp claims
* Weak or missing sources

---

### 4. Lead Finalization

Verified leads are finalized and persisted in the system.

The final lead record contains the required business information and verification metadata before being written to the CRM.

The finalized data is stored in **Neon PostgreSQL** and synchronized with **HubSpot CRM**.

---

# Lead Schema

The system is designed around the following required fields:

| Field               | Description                                              |
| ------------------- | -------------------------------------------------------- |
| `business_name`     | Verified business name                                   |
| `industry`          | Target industry                                          |
| `city`              | Business location                                        |
| `website`           | Official/public business website                         |
| `contact`           | Publicly available contact information                   |
| `whatsapp_evidence` | Evidence indicating publicly available WhatsApp presence |
| `source`            | Source/evidence used for the lead                        |
| `status`            | Lead verification/status state                           |

Example:

```json
{
  "business_name": "Example Restaurant",
  "industry": "Restaurant",
  "city": "Gujranwala",
  "website": "https://example.com",
  "contact": {
    "phone": "+92XXXXXXXXXX",
    "email": "contact@example.com"
  },
  "whatsapp_evidence": {
    "available": true,
    "source": "https://example.com/contact"
  },
  "source": "https://example.com",
  "status": "verified"
}
```

The exact structure can evolve as the verification and CRM requirements become more sophisticated.

---

# Technology Stack

| Component           | Technology |
| ------------------- | ---------- |
| Agent orchestration | LangGraph  |
| LLM                 | Gemini     |
| Web discovery       | Exa API    |
| Database            | PostgreSQL |
| Managed PostgreSQL  | Neon       |
| CRM                 | HubSpot    |
| Observability       | LangSmith  |
| API                 | FastAPI    |
| Language            | Python     |

---

# Why LangGraph?

The workflow is intentionally implemented as a graph instead of a single LLM call.

Lead generation contains multiple deterministic stages with different responsibilities:

```text
Query
  ↓
Discovery
  ↓
Verification
  ↓
Finalization
```

LangGraph provides explicit state transitions between these stages and makes it possible to add:

* Checkpointing
* Retries
* Conditional routing
* Human-in-the-loop verification
* Persistent state
* Observability
* Evaluation
* Additional verification stages

The architecture therefore does not depend on a single prompt producing trustworthy CRM data.

---

# Why Exa?

The system requires web discovery rather than relying on a static business database.

Exa is used as the web discovery layer to find relevant businesses and supporting web evidence.

The important architectural distinction is:

```text
Exa
 ↓
Discovery / Evidence
 ↓
Gemini
 ↓
Structured verification
```

Exa results are not treated as inherently correct.

The verification layer determines whether the discovered information is sufficient to classify a lead as verified.

---

# Why Gemini?

Gemini is used for the reasoning and structured extraction portions of the workflow.

The LLM is responsible for tasks such as:

* Interpreting search results
* Extracting structured business information
* Evaluating evidence
* Normalizing lead information
* Determining whether available evidence supports the lead

The LLM is not treated as the source of truth.

External evidence remains the basis for verification.

---

# Database

The project uses **Neon PostgreSQL** for persistent lead storage.

PostgreSQL provides:

* Persistent lead records
* Duplicate detection
* Querying by industry and city
* Historical lead storage
* CRM synchronization support
* Future evaluation datasets

A simplified conceptual model is:

```text
┌────────────────────────┐
│         leads          │
├────────────────────────┤
│ id                     │
│ business_name          │
│ industry               │
│ city                   │
│ website                │
│ contact                │
│ whatsapp_evidence      │
│ source                 │
│ status                 │
│ created_at             │
│ updated_at             │
└────────────────────────┘
```

The actual database schema should remain the source of truth for production deployments.

---

# HubSpot Integration

Verified leads are written to **HubSpot CRM** after finalization.

The intended data flow is:

```text
Web Discovery
      ↓
Verification
      ↓
PostgreSQL
      ↓
HubSpot CRM
```

This separation is intentional.

PostgreSQL acts as the application's persistent data layer while HubSpot acts as the downstream CRM system.

This also prevents the CRM from becoming the only source of application state.

---

# Duplicate Prevention

Duplicate prevention happens before new leads are finalized.

The workflow checks previously stored leads based on the requested search context, including:

```text
Industry
City
Business identity
```

This prevents repeatedly discovering and inserting the same businesses during subsequent runs.

For production deployments, business identity should ideally be normalized using stable identifiers such as:

* Normalized domain
* Normalized business name
* Location
* CRM record ID

rather than relying exclusively on raw business-name comparison.

---

# Verification Philosophy

The most important design principle in this project is:

> **Discovery is not verification.**

A search engine finding a business does not mean the business is verified.

A lead should only be considered verified when the available evidence supports the required fields.

For example:

```text
Search result
      ↓
"ABC Restaurant"
      ↓
Website discovered
      ↓
Website confirms business identity
      ↓
Website confirms location
      ↓
Public contact information found
      ↓
WhatsApp evidence checked
      ↓
Lead marked verified
```

This prevents the common failure mode where an LLM fills missing fields using plausible-looking information.

---

# WhatsApp Evidence

WhatsApp information is only recorded when publicly available evidence supports it.

Examples of evidence may include:

* Public WhatsApp links
* `wa.me` links
* WhatsApp contact buttons
* Public website references to WhatsApp
* Other publicly accessible business contact pages

The system should **not infer WhatsApp availability simply because a phone number exists**.

For example:

```text
Phone number exists
        ≠
WhatsApp verified
```

This distinction is important for maintaining data quality.

---

# API

The application exposes the lead-generation workflow through a FastAPI interface.

A typical request contains:

```json
{
  "industry": "restaurants",
  "city": "Gujranwala",
  "require_whatsapp": true
}
```

The API starts the LangGraph execution and returns the resulting workflow state according to the application's API contract.

The graph execution uses a unique `thread_id` for each run so that state and execution history remain isolated.

---

# Observability

**LangSmith is used as the planned observability layer.**

The integration is being added to monitor the agent's behavior across the workflow.

The intended observability coverage includes:

```text
API Request
    ↓
LangGraph Run
    ├── Query Generation
    ├── Exa Search
    ├── Gemini Reasoning
    ├── Verification
    └── CRM Write
```

LangSmith will be used to inspect:

* Graph execution traces
* Node execution
* LLM calls
* Tool calls
* Latency
* Errors
* Token usage
* Intermediate state
* Failed executions

This is especially important because lead-generation quality cannot be evaluated reliably from the final CRM records alone.

---

# Environment Variables

Create a `.env` file locally:

```env
# Gemini
GOOGLE_API_KEY=

# Exa
EXA_API_KEY=

# Neon / PostgreSQL
DATABASE_URL=

# HubSpot
HUBSPOT_ACCESS_TOKEN=

# LangSmith
LANGSMITH_API_KEY=
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=lead-generation-agent
```

Never commit `.env` to version control.

Add it to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
.pytest_cache/
```

---

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

## 2. Create the virtual environment

Using `uv`:

```bash
uv sync
```

Or create a virtual environment manually:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

---

## 3. Configure environment variables

Create:

```text
.env
```

and configure the required API keys and database credentials.

---

## 4. Run the application

```bash
uv run uvicorn api.main:app --reload
```

The API will be available locally at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

---

# Project Structure

A recommended structure for the project is:

```text
lead-generation-agent/
│
├── api/
│   ├── __init__.py
│   └── main.py
│
├── graph/
│   ├── __init__.py
│   ├── state.py
│   ├── nodes.py
│   └── graph.py
│
├── tools/
│   ├── __init__.py
│   ├── exa.py
│   ├── leads.py
│   └── hubspot.py
│
├── database/
│   ├── __init__.py
│   └── ...
│
├── tests/
│   ├── ...
│
├── .env
├── .gitignore
├── pyproject.toml
└── README.md
```

The exact structure may differ from the implementation.

---

# Error Handling

External services are inherently unreliable.

The production implementation should treat failures independently:

```text
Exa failure
    ↓
Retry / fail gracefully

Gemini failure
    ↓
Retry / fail gracefully

PostgreSQL failure
    ↓
Do not mark persistence successful

HubSpot failure
    ↓
Preserve PostgreSQL lead
    ↓
Retry CRM synchronization
```

A CRM outage should not cause already verified lead data to disappear.

Similarly, an LLM failure should not result in fabricated lead data being persisted.

---

# Security

The application handles external API credentials and potentially sensitive business contact information.

Production deployments should therefore follow these rules:

* Never commit API keys.
* Store secrets in environment variables or a secrets manager.
* Never expose API credentials to the frontend.
* Validate API inputs.
* Use HTTPS in production.
* Restrict database credentials.
* Use least-privilege HubSpot credentials.
* Do not store unnecessary personal information.
* Treat webhook/API credentials as secrets.
* Log errors without leaking credentials.

---

# Data Quality Rules

The system should enforce the following principles:

### No fabricated fields

If evidence does not contain a contact:

```text
contact = null
```

not:

```text
contact = guessed value
```

### No inferred WhatsApp

```text
phone number
≠
WhatsApp evidence
```

### Source required

Every verified lead should have supporting source information.

### Duplicate control

The same business should not repeatedly enter the CRM as a new lead.

### Verification before CRM

Unverified candidates should not be treated as verified CRM leads.

---

# Failure Modes

The system is designed around several known failure modes in automated lead generation.

### Duplicate businesses

**Problem:** The same company appears across multiple searches.

**Mitigation:** Existing-lead lookup and normalized identity checks.

### Search-result hallucination

**Problem:** An LLM invents missing business details.

**Mitigation:** Evidence-based extraction and verification.

### Incorrect location

**Problem:** A business with the correct name exists in another city.

**Mitigation:** Explicit city/location verification.

### Unsupported WhatsApp claims

**Problem:** A phone number is incorrectly classified as WhatsApp.

**Mitigation:** Require public WhatsApp evidence.

### CRM synchronization failure

**Problem:** HubSpot becomes temporarily unavailable.

**Mitigation:** PostgreSQL remains the persistent application data layer.

---

# Production Roadmap

The current system provides the core lead-generation pipeline.

The next production improvements include:

### Observability

* [ ] Complete LangSmith tracing
* [ ] Trace every LangGraph node
* [ ] Track Exa calls
* [ ] Track Gemini calls
* [ ] Track CRM operations
* [ ] Monitor latency and failures

### Evaluation

* [ ] Build a labeled lead evaluation dataset
* [ ] Measure business identification accuracy
* [ ] Measure location accuracy
* [ ] Measure contact extraction accuracy
* [ ] Measure WhatsApp evidence accuracy
* [ ] Measure duplicate rate
* [ ] Measure CRM write success rate

### Reliability

* [ ] Retry policies for external APIs
* [ ] Exponential backoff
* [ ] Request timeouts
* [ ] Idempotent CRM writes
* [ ] Failure recovery
* [ ] Dead-letter/retry mechanism for failed CRM synchronization

### Data Quality

* [ ] Domain normalization
* [ ] Business-name normalization
* [ ] Stronger duplicate detection
* [ ] Source ranking
* [ ] Evidence scoring
* [ ] Confidence thresholds

### Scalability

* [ ] Background graph execution
* [ ] Job queue
* [ ] Rate-limit handling
* [ ] Concurrent search execution
* [ ] Batch CRM synchronization
* [ ] Database indexing

---

# Design Principles

The system follows several principles that guide the implementation.

### 1. Search for evidence, not answers

Search APIs provide evidence.

The agent should not blindly trust search-result text.

### 2. Separate discovery from verification

Finding a business and verifying a business are different tasks.

### 3. Never fabricate missing information

Missing information should remain missing.

### 4. Database before CRM

Application state should not depend entirely on an external CRM.

### 5. Make external side effects explicit

Writing to HubSpot is a separate stage from reasoning and verification.

### 6. Observability is part of the system

Agentic workflows are difficult to debug without traces of what the model and tools actually did.

---

# Current Status

| Component                  | Status         |
| -------------------------- | -------------- |
| LangGraph workflow         | ✅ Implemented  |
| 4-node architecture        | ✅ Implemented  |
| Gemini integration         | ✅ Implemented  |
| Exa web discovery          | ✅ Implemented  |
| PostgreSQL persistence     | ✅ Implemented  |
| Neon PostgreSQL            | ✅ Implemented  |
| Lead verification          | ✅ Implemented  |
| HubSpot CRM integration    | ✅ Implemented  |
| FastAPI API                | ✅ Implemented  |
| LangSmith observability    | 🚧 In progress |
| Automated evaluation suite | 🔜 Planned     |
| Production retry/recovery  | 🔜 Planned     |
| Advanced deduplication     | 🔜 Planned     |

---

# License

Add the project's license here.

For example:

```text
MIT License
```

if the repository is intended to be released under MIT.

---

# Disclaimer

This system collects publicly available business information for lead-generation purposes.

The application should respect applicable website terms of service, API usage policies, privacy requirements, and applicable laws when collecting, storing, and using business contact information.

Public availability of information does not automatically mean unrestricted permission to use that information for every purpose.
