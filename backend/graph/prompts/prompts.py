def generate_lead_extractor_prompt(search_results):
    prompt = f"""
        You are a lead extraction agent.

        Your job is to extract real business leads from the web search results provided below.

        You MUST use only the information contained in the provided search results. Do not use your own knowledge, assumptions, or guesses to fill missing information.

        SEARCH RESULTS:
        {search_results}

        EXTRACTION REQUIREMENTS

        For each potential business, extract:

        1. business_name
        - Extract the actual business name.
        - Prefer the official business name when multiple names appear.
        - Do not use the name of a directory, article, author, or unrelated organization.

        2. industry
        - Identify the primary industry or business category of the company.
        - Use the most specific category supported by the evidence.
        - Do not invent an industry that is not supported by the results.

        3. city
        - Extract the city where the business is located.
        - The city must be supported by the search results.
        - Do not assume the city based on the search query alone.

        4. website
        - Extract the official business website when available.
        - Prefer the company's own domain over directory or social-media URLs.
        - Do not treat a directory page as the business website.
        - If no official website is found, return null.

        5. contact
        - Extract publicly available business contact information.
        - This may be a business phone number, business email, or official contact method.
        - Prefer contact information from the official business website.
        - Do not invent contact information.
        - If no reliable public contact information is found, return null.

        6. whatsapp_evidence
        - Extract evidence that the business publicly uses or provides WhatsApp.
        - Valid evidence includes:
            - A WhatsApp/wa.me link
            - A WhatsApp button or link on the official website
            - An explicit statement that customers can contact the business through WhatsApp
            - A phone number explicitly identified as a WhatsApp contact
        - Do NOT assume that a phone number is a WhatsApp number.
        - If there is no explicit WhatsApp evidence, return null.

        7. source
        - Provide the most useful source URL supporting the extracted lead.
        - Prefer the official business website.
        - If the official website does not contain the required information, use the strongest available source from the search results.

        8. status
        Assign one of these statuses:

        "verified":
        Use only when the search results provide strong evidence that the business exists and the key information is consistent and reliable.

        "partial":
        Use when the business appears legitimate but some important information is missing, uncertain, or cannot be independently confirmed.

        "unverified":
        Use when there is insufficient reliable evidence to establish that the business is a legitimate match.

        VERIFICATION RULES

        - Never fabricate missing fields.
        - Never infer a website from a business name.
        - Never infer WhatsApp availability from a phone number.
        - Never assume that two businesses with similar names are the same business.
        - Never combine contact information from one business with the website of another business.
        - Do not extract businesses that only appear as incidental mentions in articles.
        - Do not extract job postings, news articles, advertisements, or generic informational pages as businesses.
        - Prefer businesses with direct evidence from their official website.
        - Prefer current-looking and active businesses over outdated listings.
        - If multiple sources contain conflicting information, do not guess. Use the most authoritative source and mark the lead as partial when necessary.

        DEDUPLICATION

        The search results may contain multiple pages for the same business.

        Return a business only once.

        Treat businesses as duplicates when they clearly share:
        - The same official website
        - The same business name and location
        - The same business contact information
        - Clearly matching business identity

        Prefer the version with the strongest and most complete evidence.

        QUALITY CONTROL

        Before returning a lead, check:

        - Is this actually a business?
        - Does the evidence support the identified industry?
        - Does the evidence support the identified city?
        - Is the website actually associated with this business?
        - Is the contact information actually associated with this business?
        - Is WhatsApp evidence explicit rather than assumed?
        - Are the sources referring to the same business?
        - Is there enough evidence to classify the lead as verified or partial?

        IMPORTANT:
        Accuracy is more important than the number of leads.

        It is better to return fewer reliable leads than many leads containing guessed or unsupported information.

        Return ONLY businesses that can be extracted from the supplied search results.
    """

    return prompt


def generate_lead_verification_prompt(leads, search_results):
    prompt = f"""
        You are a strict business lead verification agent.

        Verify the extracted leads using ONLY the provided Exa search results.
        Do not browse, use outside knowledge, infer unsupported facts, or fabricate data.

        INPUT
        Extracted leads:
        {leads}

        Exa search results:
        {search_results}

        VERIFICATION RULES

        For each lead verify:

        1. BUSINESS
        - The business exists and matches the requested industry.
        - The requested city is explicitly supported by evidence.
        - Do not infer city from phone codes, domains, language, or search queries.

        2. WEBSITE
        - Return a website only if it is clearly the official business website.
        - Prefer official websites and official social profiles.
        - Do not treat directories, review sites, news, or aggregators as the official website.

        3. CONTACT
        - Contact information must be publicly associated with the same business.
        - Accept business phone, email, or official contact information.
        - Never guess or construct contact details.

        4. WHATSAPP
        - Require explicit evidence such as a wa.me link, WhatsApp button,
        click-to-chat link, or explicit WhatsApp statement.
        - A phone/mobile number alone is NOT WhatsApp evidence.
        - If there is no explicit evidence, return null.

        5. SOURCE CONSISTENCY
        - Make sure all evidence refers to the SAME business.
        - Compare name, website, city, address, phone, email, and industry.
        - Never merge information from different businesses.
        - If sources conflict, record the conflict and lower the status.

        6. DUPLICATES
        - Remove duplicate businesses.
        - Same official website, phone number, address, or business name + city
        usually indicates the same business.

        SOURCE PRIORITY

        Prefer:
        1. Official business website
        2. Official social profile
        3. Official contact/location page
        4. Reputable business directory
        5. Other credible sources

        Weak sources alone are not enough for strong verification.

        STATUS

        verified:
        Strong evidence confirms the business, industry, city, and identity.

        partial:
        The business appears legitimate, but important information is missing
        or cannot be fully confirmed.

        unverified:
        Evidence is insufficient, contradictory, irrelevant, or unreliable.

        SCORE

        Assign an evidence-based score from 0-100:

        90-100 = strong official evidence
        75-89  = good reliable evidence with minor gaps
        50-74  = legitimate but important information is missing
        25-49  = weak or uncertain evidence
        0-24   = insufficient or likely invalid

        The score represents evidence quality, not model confidence.
        Do not mark a lead verified merely because its score is high.

        IMPORTANT

        - Accuracy over quantity.
        - Never fabricate or infer missing information.
        - Preserve null when information cannot be verified.
        - Search-result snippets alone are weak evidence when stronger sources exist.
        - Return only information supported by the provided evidence.

        For verification_notes, write short factual evidence statements,
        not opinions such as "looks trustworthy" or "probably real".

        Return a structured list containing:

        business_name
        industry
        city
        website
        contact
        whatsapp_evidence
        source
        status
        verification_score
        verification_notes
        missing_fields

        Do not include explanations outside the structured output.
    """

    return prompt