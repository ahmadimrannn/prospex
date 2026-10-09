MODEL_NAME="gemini-3.5-flash-lite"

HUBSPOT_INDUSTRY_MAP = {
    # Retail / apparel
    "clothing store": "RETAIL",
    "clothing shop": "RETAIL",
    "fashion store": "RETAIL",
    "fashion boutique": "RETAIL",
    "apparel shop": "RETAIL",

    # Apparel / fashion
    "clothing brand": "APPAREL_FASHION",
    "apparel brand": "APPAREL_FASHION",
    "fashion brand": "APPAREL_FASHION",
    "garment manufacturer": "APPAREL_FASHION",

    # Textile manufacturing
    "textile manufacturer": "TEXTILES",
    "textile manufacturing": "TEXTILES",
    "textile manufacturer": "TEXTILES",
    "textile and garment manufacturer": "TEXTILES",
    "textiles and garments manufacturing": "TEXTILES",
}

INDUSTRY_ALIASES = {
    # FOOD, RESTAURANTS & HOSPITALITY
    "restaurant": {
        "restaurant", "restaurants", "dining restaurant",
        "family restaurant", "casual dining restaurant",
        "fine dining restaurant", "local restaurant",
        "food restaurant", "eatery", "bistro", "brasserie",
    },
    "cafe": {
        "cafe", "café", "coffee shop", "coffee house",
        "espresso bar", "tea house", "tea shop",
    },
    "fast food": {
        "fast food", "fast food restaurant", "burger shop",
        "pizza shop", "takeaway restaurant", "takeout restaurant",
        "quick service restaurant", "qsr",
    },
    "bakery": {
        "bakery", "bakeries", "cake shop", "bread shop",
        "pastry shop", "patisserie", "confectionery bakery",
        "home bakery", "home based bakery", "home baking business",
        "cake bakery", "cupcake shop",
    },
    "catering": {
        "catering", "catering service", "event catering",
        "corporate catering", "food catering",
    },
    "food manufacturing": {
        "food manufacturing", "food manufacturer",
        "food processing", "food production",
        "packaged food manufacturer",
    },
    "grocery store": {
        "grocery store", "grocery shop", "supermarket",
        "mini mart", "minimart", "convenience store",
        "general store", "kiryana store", "karyana store",
    },
    "food supplier": {
        "food supplier", "food distributor", "food wholesaler",
        "wholesale food supplier", "beverage supplier",
    },
    "hotel": {
        "hotel", "hotels", "motel", "resort", "guest house",
        "guesthouse", "boutique hotel", "lodging",
    },
    "travel agency": {
        "travel agency", "travel agent", "tour operator",
        "travel company", "tourism company", "holiday planner",
        "travel services",
    },
    "event management": {
        "event management", "event planner", "event planning",
        "event organizer", "wedding planner",
        "wedding planning", "event management company",
    },

    # BEAUTY, FITNESS & PERSONAL CARE
    "salon": {
        "salon", "beauty salon", "beauty parlour", "beauty parlor",
        "hair salon", "hairdresser", "hairdressing salon",
        "ladies salon", "hair and beauty salon",
        "unisex salon", "bridal salon",
    },
    "barber shop": {
        "barber shop", "barbershop", "barber",
        "mens salon", "men's salon", "mens grooming",
    },
    "spa": {
        "spa", "day spa", "wellness spa", "massage spa",
        "massage center", "massage centre", "massage therapy",
    },
    "beauty clinic": {
        "beauty clinic", "aesthetic clinic", "skin clinic",
        "cosmetic clinic", "laser clinic", "med spa",
        "medical spa", "aesthetic center", "aesthetic centre",
    },
    "cosmetics store": {
        "cosmetics store", "cosmetic shop", "makeup store",
        "makeup shop", "beauty products store",
        "beauty supply store", "skincare store",
    },
    "gym": {
        "gym", "fitness center", "fitness centre",
        "fitness club", "health club", "fitness studio",
        "strength training gym", "weightlifting gym",
    },
    "personal trainer": {
        "personal trainer", "personal training",
        "fitness coach", "fitness instructor",
        "online fitness coach",
    },
    "yoga studio": {
        "yoga studio", "yoga center", "yoga centre",
        "pilates studio", "meditation center",
        "meditation centre",
    },
    "sports club": {
        "sports club", "sports academy", "sports facility",
        "athletic club", "martial arts school",
        "boxing gym", "swimming club",
    },
    "laundry": {
        "laundry", "laundromat", "dry cleaner",
        "dry cleaning service", "washing service",
        "laundry service", "ironing service",
    },

    # RETAIL & E-COMMERCE
    "boutique": {
        "boutique", "fashion boutique", "clothing boutique",
        "ladies boutique", "womens boutique",
        "women's boutique", "designer boutique",
        "fashion store", "apparel boutique",
    },
    "clothing store": {
        "clothing store", "clothing shop", "apparel store",
        "garment shop", "fashion retailer", "mens clothing store",
        "womens clothing store", "kids clothing store",
        "garments retailer", "ready made garments",
    },
    "textile manufacturer": {
        "textile manufacturer", "textile manufacturing",
        "textile mill", "fabric manufacturer", "fabric mill",
        "textile factory", "cloth manufacturer",
        "textile and garment manufacturer",
    },
    "clothing manufacturer": {
        "clothing manufacturer", "garment manufacturer",
        "apparel manufacturer", "garment factory",
        "clothing factory", "sportswear manufacturer",
        "uniform manufacturer", "fashion manufacturer",
    },
    "shoe store": {
        "shoe store", "shoe shop", "footwear store",
        "footwear retailer", "sneaker store",
    },
    "jewelry store": {
        "jewelry store", "jewellery store", "jewelry shop",
        "jewellery shop", "gold shop", "gold jeweler",
        "gold jeweller", "accessories jewelry store",
    },
    "electronics store": {
        "electronics store", "electronics shop",
        "electronic goods store", "computer shop",
        "mobile phone shop", "cell phone store",
        "phone accessories store", "appliance store",
    },
    "furniture store": {
        "furniture store", "furniture shop",
        "furniture retailer", "home furniture store",
        "office furniture store",
    },
    "home decor store": {
        "home decor store", "home decoration shop",
        "interior decor store", "home furnishings store",
        "lighting store", "curtain shop",
    },
    "hardware store": {
        "hardware store", "hardware shop",
        "building supplies store", "tools shop",
        "paint store", "paint shop", "plumbing supplies store",
    },
    "pharmacy": {
        "pharmacy", "chemist", "drugstore", "drug store",
        "medical store", "medicine shop",
    },
    "bookstore": {
        "bookstore", "book shop", "book store",
        "stationery shop", "stationery store",
        "office supplies store",
    },
    "toy store": {
        "toy store", "toy shop", "kids toy store",
        "children's toy store",
    },
    "pet store": {
        "pet store", "pet shop", "pet supplies store",
        "aquarium shop", "pet products retailer",
    },
    "florist": {
        "florist", "flower shop", "flower store",
        "floral shop", "floral design business",
    },
    "online store": {
        "online store", "online shop", "ecommerce store",
        "e commerce store", "ecommerce business",
        "online retailer", "internet retailer",
    },
    "wholesale distributor": {
        "wholesale distributor", "wholesaler",
        "wholesale business", "wholesale supplier",
        "distribution company", "product distributor",
    },

    # HEALTHCARE
    "hospital": {
        "hospital", "general hospital", "private hospital",
        "medical hospital", "healthcare hospital",
    },
    "medical clinic": {
        "medical clinic", "clinic", "health clinic",
        "family clinic", "general practice",
        "general practitioner", "medical center", "medical centre",
    },
    "dentist": {
        "dentist", "dental clinic", "dental practice",
        "dental surgery", "orthodontist", "orthodontic clinic",
    },
    "doctor": {
        "doctor", "physician", "medical doctor",
        "specialist doctor", "private practice physician",
    },
    "dermatologist": {
        "dermatologist", "dermatology clinic",
        "skin specialist", "skin doctor",
    },
    "eye clinic": {
        "eye clinic", "ophthalmology clinic",
        "eye hospital", "optometrist", "optician",
        "optical store", "eyewear store",
    },
    "physiotherapy": {
        "physiotherapy", "physical therapy",
        "physiotherapy clinic", "physical therapy clinic",
        "rehabilitation center", "rehabilitation centre",
    },
    "diagnostic laboratory": {
        "diagnostic laboratory", "diagnostic lab",
        "medical laboratory", "pathology lab",
        "testing laboratory", "medical testing center",
        "medical testing centre",
    },
    "veterinary clinic": {
        "veterinary clinic", "vet clinic", "veterinarian",
        "animal hospital", "animal clinic", "pet hospital",
    },
    "mental health services": {
        "mental health clinic", "psychologist",
        "psychology clinic", "psychiatrist",
        "counseling center", "counselling centre",
        "therapy practice",
    },
    "home healthcare": {
        "home healthcare", "home health care",
        "home nursing", "nursing services",
        "elder care", "caregiver services",
    },

    # EDUCATION & TRAINING
    "school": {
        "school", "private school", "public school",
        "primary school", "secondary school",
        "high school", "grammar school",
    },
    "college": {
        "college", "higher secondary school",
        "intermediate college", "community college",
    },
    "university": {
        "university", "higher education institution",
        "degree awarding institution",
    },
    "tuition center": {
        "tuition center", "tuition centre", "tuition academy",
        "coaching center", "coaching centre",
        "academy", "private tutor", "tutoring service",
    },
    "training institute": {
        "training institute", "training center", "training centre",
        "vocational institute", "skills training center",
        "professional training provider",
    },
    "language school": {
        "language school", "language institute",
        "english language center", "english academy",
        "language training center", "ielts academy",
    },
    "online education": {
        "online education", "online learning platform",
        "e learning", "elearning company",
        "online tutoring", "educational technology",
        "edtech company",
    },
    "driving school": {
        "driving school", "driving academy",
        "driving instructor", "driver training school",
    },

    # TECHNOLOGY & DIGITAL SERVICES
    "software company": {
        "software company", "software house",
        "software development company", "software developer",
        "custom software development", "saas company",
        "technology company", "tech company",
        "it company", "information technology company",
    },
    "ai company": {
        "ai company", "artificial intelligence company",
        "machine learning company", "ai solutions provider",
        "ai development company", "generative ai company",
        "automation company", "intelligent automation provider",
    },
    "it services": {
        "it services", "it support", "managed it services",
        "it consulting", "it consultancy",
        "technical support company", "computer services",
    },
    "web development": {
        "web development", "web development company",
        "website design company", "web design agency",
        "website development", "web designer",
    },
    "mobile app development": {
        "mobile app development", "app development company",
        "mobile application developer", "ios app development",
        "android app development",
    },
    "cybersecurity": {
        "cybersecurity", "cyber security company",
        "information security", "security consulting",
        "penetration testing company", "security services",
    },
    "cloud services": {
        "cloud services", "cloud computing company",
        "cloud consulting", "cloud infrastructure provider",
        "cloud migration services",
    },
    "data analytics": {
        "data analytics", "data analytics company",
        "business intelligence company", "data science company",
        "data engineering services",
    },
    "telecommunications": {
        "telecommunications", "telecom company",
        "internet service provider", "isp",
        "network services provider", "telecom services",
    },
    "digital marketing": {
        "digital marketing", "digital marketing agency",
        "online marketing agency", "internet marketing",
        "performance marketing agency",
    },
    "seo agency": {
        "seo agency", "search engine optimization",
        "search engine optimisation", "seo company",
        "seo services provider",
    },
    "social media agency": {
        "social media agency", "social media marketing",
        "social media management", "social media company",
    },
    "advertising agency": {
        "advertising agency", "ad agency",
        "advertising company", "media buying agency",
        "creative advertising agency",
    },
    "branding agency": {
        "branding agency", "brand strategy agency",
        "brand design company", "brand consultancy",
    },
    "graphic design": {
        "graphic design", "graphic design agency",
        "graphic designer", "visual design studio",
        "design studio",
    },
    "content writing": {
        "content writing", "content writing agency",
        "copywriting agency", "copywriter",
        "content marketing agency", "technical writing services",
    },
    "video production": {
        "video production", "video production company",
        "videography", "film production company",
        "commercial video production",
    },
    "photography": {
        "photography", "photography studio",
        "photographer", "commercial photography",
        "wedding photography",
    },

    # PROFESSIONAL & BUSINESS SERVICES
    "accounting": {
        "accounting", "accounting firm", "accountant",
        "bookkeeping", "bookkeeping services",
        "tax accounting", "chartered accountant",
    },
    "legal services": {
        "legal services", "law firm", "lawyer",
        "attorney", "legal consultancy",
        "legal advisor", "solicitor",
    },
    "business consulting": {
        "business consulting", "business consultancy",
        "management consulting", "business consultant",
        "strategy consulting",
    },
    "hr services": {
        "hr services", "human resources", "hr consultancy",
        "recruitment agency", "staffing agency",
        "talent acquisition", "employment agency",
    },
    "market research": {
        "market research", "market research company",
        "consumer research", "business research",
        "customer insights agency",
    },
    "translation services": {
        "translation services", "translation agency",
        "translator", "interpretation services",
        "localization company", "localisation company",
    },
    "virtual assistant": {
        "virtual assistant", "virtual assistant services",
        "administrative support", "remote assistant",
        "business support services",
    },
    "call center": {
        "call center", "call centre", "contact center",
        "contact centre", "customer support outsourcing",
        "bpo company", "business process outsourcing",
    },
    "security services": {
        "security services", "security company",
        "security guard company", "private security",
        "guarding services",
    },
    "cleaning services": {
        "cleaning services", "cleaning company",
        "commercial cleaning", "residential cleaning",
        "janitorial services", "house cleaning",
    },
    "pest control": {
        "pest control", "pest control company",
        "exterminator", "termite control", "fumigation services",
    },

    # REAL ESTATE, CONSTRUCTION & PROPERTY
    "real estate agency": {
        "real estate agency", "real estate agent",
        "property dealer", "property agency",
        "estate agency", "real estate brokerage",
        "property consultant", "property consultancy",
    },
    "property management": {
        "property management", "property management company",
        "rental management", "building management",
    },
    "construction company": {
        "construction company", "construction contractor",
        "building contractor", "civil contractor",
        "general contractor", "construction services",
    },
    "architecture": {
        "architecture", "architect", "architecture firm",
        "architectural services", "architectural design",
    },
    "interior design": {
        "interior design", "interior designer",
        "interior design company", "interior design studio",
        "interior decorator",
    },
    "engineering services": {
        "engineering services", "engineering company",
        "engineering consultancy", "civil engineering",
        "mechanical engineering services",
    },
    "electrical services": {
        "electrical services", "electrician",
        "electrical contractor", "electrical company",
        "electrical installation",
    },
    "plumbing services": {
        "plumbing services", "plumber", "plumbing company",
        "plumbing contractor",
    },
    "hvac services": {
        "hvac services", "hvac contractor",
        "air conditioning services", "ac repair",
        "heating and cooling", "ventilation services",
    },
    "solar energy": {
        "solar energy", "solar company", "solar installer",
        "solar panel installation", "solar energy provider",
        "renewable energy company",
    },
    "painting services": {
        "painting services", "painting contractor",
        "house painter", "commercial painting",
    },
    "roofing services": {
        "roofing services", "roofing contractor",
        "roof repair company", "roof installation",
    },
    "building materials": {
        "building materials", "construction materials supplier",
        "cement supplier", "steel supplier",
        "bricks supplier", "building supplies",
    },

    # AUTOMOTIVE & TRANSPORT
    "car dealership": {
        "car dealership", "car dealer", "auto dealership",
        "used car dealer", "used car dealership",
        "vehicle dealership",
    },
    "auto repair": {
        "auto repair", "auto mechanic", "car repair shop",
        "automotive repair", "vehicle repair",
        "car workshop", "auto workshop",
    },
    "auto parts": {
        "auto parts", "auto spare parts", "car parts store",
        "automotive parts supplier", "vehicle parts retailer",
    },
    "car wash": {
        "car wash", "car washing service", "auto detailing",
        "vehicle detailing", "car detailing",
    },
    "car rental": {
        "car rental", "vehicle rental", "rent a car",
        "car hire", "vehicle leasing",
    },
    "logistics": {
        "logistics", "logistics company", "logistics services",
        "supply chain company", "freight logistics",
    },
    "courier service": {
        "courier service", "courier company",
        "parcel delivery", "delivery service",
        "express delivery company",
    },
    "freight transport": {
        "freight transport", "freight forwarding",
        "freight forwarder", "cargo company",
        "cargo services", "shipping company",
    },
    "moving services": {
        "moving services", "movers", "removal company",
        "relocation services", "house moving company",
    },
    "bus and passenger transport": {
        "passenger transport", "bus company",
        "transport service", "school transport",
        "staff transportation",
    },

    # FINANCE & INSURANCE
    "bank": {
        "bank", "commercial bank", "retail bank",
        "banking services", "microfinance bank",
    },
    "insurance agency": {
        "insurance agency", "insurance company",
        "insurance broker", "insurance services",
        "insurance consultant",
    },
    "financial advisory": {
        "financial advisory", "financial advisor",
        "financial adviser", "financial planning",
        "wealth management", "investment advisory",
    },
    "microfinance": {
        "microfinance", "microfinance institution",
        "microcredit company", "micro lending",
    },
    "payment services": {
        "payment services", "payment processor",
        "payment gateway", "digital payments company",
        "fintech company", "financial technology",
    },

    # INDUSTRIAL & MANUFACTURING
    "manufacturing": {
        "manufacturing", "manufacturer",
        "manufacturing company", "industrial manufacturer",
        "production company",
    },
    "plastic manufacturing": {
        "plastic manufacturing", "plastic manufacturer",
        "plastic products manufacturer", "plastic factory",
        "plastic packaging manufacturer",
    },
    "metal fabrication": {
        "metal fabrication", "metal fabricator",
        "steel fabrication", "metal works",
        "metal manufacturing",
    },
    "furniture manufacturing": {
        "furniture manufacturing", "furniture manufacturer",
        "furniture factory", "wood furniture manufacturer",
    },
    "packaging": {
        "packaging", "packaging company",
        "packaging manufacturer", "packaging supplier",
        "carton manufacturer", "printing and packaging",
    },
    "printing services": {
        "printing services", "printing company",
        "commercial printer", "digital printing",
        "offset printing", "print shop",
    },
    "chemical manufacturing": {
        "chemical manufacturing", "chemical manufacturer",
        "industrial chemicals", "chemical production",
    },
    "pharmaceutical manufacturing": {
        "pharmaceutical manufacturer", "pharmaceutical company",
        "pharmaceutical manufacturing", "drug manufacturer",
    },
    "agricultural supplier": {
        "agricultural supplier", "agriculture supplies",
        "farm supplies", "fertilizer supplier",
        "seed supplier", "pesticide supplier",
        "agricultural equipment supplier",
    },
    "agriculture": {
        "agriculture", "farm", "farming",
        "agricultural business", "crop production",
        "livestock farming", "dairy farming",
    },
    "dairy products": {
        "dairy products", "dairy farm", "dairy company",
        "milk supplier", "milk processing",
        "dairy products manufacturer",
    },

    # MEDIA, ENTERTAINMENT & CREATIVE BUSINESSES
    "media company": {
        "media company", "media agency",
        "digital media company", "publishing company",
        "news agency", "media production",
    },
    "music school": {
        "music school", "music academy",
        "music lessons", "music teacher",
        "music training center",
    },
    "entertainment venue": {
        "entertainment venue", "amusement center",
        "amusement park", "play area", "arcade",
        "family entertainment center",
    },
    "gaming company": {
        "gaming company", "game development company",
        "video game developer", "game studio",
        "esports organization",
    },
    "influencer agency": {
        "influencer agency", "influencer marketing",
        "creator management agency", "talent management",
    },

    # OTHER LOCAL & SPECIALIST BUSINESSES
    "wedding services": {
        "wedding services", "wedding decorator",
        "wedding decor", "bridal services",
        "wedding venue", "wedding vendor",
    },
    "photocopy and printing shop": {
        "photocopy shop", "copy shop", "photocopy center",
        "photocopy centre", "printing and photocopy shop",
    },
    "repair services": {
        "repair services", "repair shop",
        "appliance repair", "electronics repair",
        "computer repair", "phone repair",
    },
    "tailoring": {
        "tailoring", "tailor", "tailoring shop",
        "tailoring services", "dressmaker",
        "custom clothing", "alteration services",
    },
    "embroidery": {
        "embroidery", "embroidery services",
        "embroidery business", "embroidery manufacturer",
        "custom embroidery", "machine embroidery",
    },
    "security systems": {
        "security systems", "cctv installation",
        "cctv company", "alarm systems",
        "surveillance systems installer",
    },
    "funeral services": {
        "funeral services", "funeral home",
        "funeral director", "burial services",
    },
    "nonprofit organization": {
        "nonprofit organization", "non profit organization",
        "charity", "charitable organization",
        "ngo", "non governmental organization",
    },
    "religious organization": {
        "religious organization", "religious institution",
        "place of worship", "mosque", "church", "temple",
    },
}

