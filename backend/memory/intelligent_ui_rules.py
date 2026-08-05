"""
LOT AI Intelligent UI Rules Matrix
====================================
Dynamically maps query Content Types to their exact valid UI components:
[Hero Image, Gallery, Timeline, Map, Quick Facts, FAQ].

Matrix Rules:
- Places:      Hero Image ✅ | Gallery ✅ | Timeline ✅ | Map ✅ | Quick Facts ✅ | FAQ ✅
- People:      Hero Image ✅ | Gallery ✅ | Timeline ✅ | Map ❌ | Quick Facts ✅ | FAQ ✅
- Education:   Hero Image ⚪ | Gallery ❌ | Timeline ❌ | Map ❌ | Quick Facts ⚪ | FAQ ✅
- Companies:   Hero Image ✅ | Gallery ✅ | Timeline ✅ | Map ⚪ | Quick Facts ✅ | FAQ ✅
- Products:    Hero Image ✅ | Gallery ✅ | Timeline ❌ | Map ❌ | Quick Facts ✅ | FAQ ✅
- Diseases:    Hero Image ⚪ | Gallery ❌ | Timeline ❌ | Map ❌ | Quick Facts ✅ | FAQ ✅
- Animals:     Hero Image ✅ | Gallery ✅ | Timeline ❌ | Map ✅ | Quick Facts ✅ | FAQ ✅
- Recipes:     Hero Image ✅ | Gallery ✅ | Timeline ❌ | Map ❌ | Quick Facts ✅ | FAQ ✅
- Movies:      Hero Image ✅ | Gallery ✅ | Timeline ❌ | Map ❌ | Quick Facts ✅ | FAQ ✅
- Books:       Hero Image ✅ | Gallery ⚪ | Timeline ❌ | Map ❌ | Quick Facts ✅ | FAQ ✅
- News:        Hero Image ✅ | Gallery ⚪ | Timeline ✅ | Map ⚪ | Quick Facts ✅ | FAQ ✅
- Programming: Hero Image ⚪ | Gallery ❌ | Timeline ❌ | Map ❌ | Quick Facts ⚪ | FAQ ✅
"""

import logging

logger = logging.getLogger(__name__)

INTELLIGENT_UI_MATRIX = {
    "Places":      {"hero_image": True,  "gallery": True,  "timeline": True,  "map": True,  "quick_facts": True,  "faq": True},
    "People":      {"hero_image": True,  "gallery": True,  "timeline": True,  "map": False, "quick_facts": True,  "faq": True},
    "Education":   {"hero_image": False, "gallery": False, "timeline": False, "map": False, "quick_facts": False, "faq": True},
    "Companies":   {"hero_image": True,  "gallery": True,  "timeline": True,  "map": False, "quick_facts": True,  "faq": True},
    "Products":    {"hero_image": True,  "gallery": True,  "timeline": False, "map": False, "quick_facts": True,  "faq": True},
    "Diseases":    {"hero_image": False, "gallery": False, "timeline": False, "map": False, "quick_facts": True,  "faq": True},
    "Animals":     {"hero_image": True,  "gallery": True,  "timeline": False, "map": True,  "quick_facts": True,  "faq": True},
    "Recipes":     {"hero_image": True,  "gallery": True,  "timeline": False, "map": False, "quick_facts": True,  "faq": True},
    "Movies":      {"hero_image": True,  "gallery": True,  "timeline": False, "map": False, "quick_facts": True,  "faq": True},
    "Books":       {"hero_image": True,  "gallery": False, "timeline": False, "map": False, "quick_facts": True,  "faq": True},
    "News":        {"hero_image": True,  "gallery": False, "timeline": True,  "map": False, "quick_facts": True,  "faq": True},
    "Programming": {"hero_image": False, "gallery": False, "timeline": False, "map": False, "quick_facts": False, "faq": True}
}

def classify_content_type(query: str) -> str:
    """
    Classifies user query into the 12-Class Taxonomy:
    [Person, Place, Educational, Product, Company, Disease, Movie, Book, News, Recipe, Programming, Animal, Generic]
    
    Expanded keyword coverage for accurate hero image triggering.
    """
    q = query.lower().strip()
    
    # === PROGRAMMING & ACADEMIC TOPICS (highest priority — prevent false hero image triggers) ===
    prog_keywords = {"code", "python", "java", "js", "javascript", "typescript", "ts", "c++", "cpp", "c#", "golang", "rust", 
                     "html", "css", "react", "angular", "vue", "svelte", "nextjs", "django", "flask", "fastapi",
                     "algorithm", "dsa", "oop", "function", "class", "bug", "error", "api", "database", "sql",
                     "mongodb", "redis", "docker", "kubernetes", "git", "npm", "pip", "webpack", "vite",
                     "debug", "compile", "deploy", "regex", "json", "yaml", "graphql", "rest", "websocket",
                     "loop", "array", "string", "variable", "syntax", "object", "pointer", "recursion", "async"}
    if any(k in q.split() or k in q for k in ["javascript", "typescript", "python", "for loop", "while loop", "data structure"]) or any(k in q.split() for k in prog_keywords) or "how to code" in q or "build a" in q or "write a program" in q:
        return "Programming"

    # === PLACES & LANDMARKS (expanded global coverage) ===
    place_keywords = {
        # Generic place words
        "temple", "city", "country", "state", "fort", "lake", "mountain", "river", "park", "museum",
        "airport", "palace", "castle", "cathedral", "mosque", "church", "monastery", "beach", "island",
        "waterfall", "volcano", "canyon", "desert", "glacier", "valley", "bridge", "tower", "monument",
        "statue", "memorial", "plaza", "square", "garden", "zoo", "aquarium", "stadium", "arena",
        "capital", "village", "town", "district", "province", "continent", "ocean", "sea", "harbour",
        "harbor", "port", "lighthouse", "pyramid", "ruins", "heritage", "landmark",
        # Famous world landmarks & places
        "eiffel tower", "taj mahal", "great wall", "colosseum", "machu picchu", "petra", "angkor wat",
        "christ the redeemer", "chichen itza", "stonehenge", "acropolis", "parthenon", "big ben",
        "statue of liberty", "golden gate", "niagara falls", "grand canyon", "mount everest",
        "mount fuji", "kilimanjaro", "sahara", "amazon", "nile", "ganges", "mississippi",
        "great barrier reef", "galapagos", "yellowstone", "yosemite", "swiss alps",
        # Indian places
        "tirupati", "kedarnath", "sabarimala", "vijayawada", "hyderabad", "mumbai", "delhi", "bangalore",
        "chennai", "kolkata", "jaipur", "agra", "varanasi", "rishikesh", "dharamsala", "shimla",
        "manali", "ladakh", "goa", "kerala", "hampi", "mysore", "ooty", "darjeeling", "amritsar",
        "golden temple", "red fort", "qutub minar", "gateway of india", "charminar", "hawa mahal",
        # World cities
        "paris", "london", "tokyo", "new york", "los angeles", "san francisco", "chicago", "dubai",
        "singapore", "hong kong", "shanghai", "beijing", "sydney", "melbourne", "rome", "barcelona",
        "amsterdam", "berlin", "vienna", "prague", "istanbul", "cairo", "moscow", "toronto",
        "vancouver", "rio de janeiro", "buenos aires", "cape town", "bangkok", "seoul", "taipei"
    }
    if any(k in q for k in place_keywords):
        return "Place"

    # === PEOPLE & PERSONALITIES (expanded) ===
    people_keywords = {
        "who is", "who was", "biography", "life of", "born in", "died in",
        "ceo", "founder", "president", "prime minister", "king", "queen", "emperor",
        "actor", "actress", "singer", "musician", "artist", "painter", "composer",
        "scientist", "physicist", "mathematician", "chemist", "biologist", "astronaut",
        "philosopher", "writer", "poet", "journalist", "athlete", "player", "coach",
        "leader", "activist", "revolutionary", "inventor", "entrepreneur", "billionaire",
        "nobel prize", "pulitzer", "oscar winner",
        # Famous people (expanded)
        "elon musk", "steve jobs", "bill gates", "jeff bezos", "mark zuckerberg", "sundar pichai",
        "satya nadella", "tim cook", "jensen huang", "sam altman", "linus torvalds",
        "apj abdul kalam", "narendra modi", "gandhi", "nehru", "ambedkar", "tagore",
        "albert einstein", "isaac newton", "nikola tesla", "marie curie", "stephen hawking",
        "alan turing", "charles darwin", "galileo", "da vinci", "shakespeare", "aristotle",
        "barack obama", "donald trump", "joe biden", "xi jinping", "putin",
        "sachin tendulkar", "virat kohli", "dhoni", "lionel messi", "cristiano ronaldo",
        "taylor swift", "beyonce", "drake", "kanye west", "michael jackson",
        "oprah winfrey", "warren buffett", "jack ma", "ratan tata"
    }
    if any(k in q for k in people_keywords):
        return "Person"

    # === COMPANIES ===
    company_keywords = {"inc", "corp", "ltd", "google", "apple", "microsoft", "nvidia", "amazon", 
                        "tesla", "meta", "tcs", "infosys", "wipro", "samsung", "intel", "amd",
                        "netflix", "spotify", "uber", "airbnb", "openai", "anthropic", "deepmind",
                        "spacex", "twitter", "linkedin", "adobe", "salesforce", "oracle", "ibm",
                        "stock price", "market cap", "quarterly earnings", "ipo", "startup"}
    if any(k in q for k in company_keywords):
        return "Company"

    # === DISEASE & HEALTH ===
    disease_keywords = {"disease", "syndrome", "symptom", "fever", "virus", "infection", "cancer", 
                        "diabetes", "treatment", "medicine", "therapy", "diagnosis", "health",
                        "pandemic", "vaccine", "allergy", "disorder", "surgery", "hospital"}
    if any(k in q for k in disease_keywords):
        return "Disease"

    # === RECIPES & FOOD ===
    recipe_keywords = {"recipe", "how to cook", "dish", "curry", "biryani", "ingredients", "baking",
                       "cuisine", "how to make", "meal prep", "food", "restaurant"}
    if any(k in q for k in recipe_keywords):
        return "Recipe"

    # === PRODUCTS & GADGETS ===
    product_keywords = {"iphone", "macbook", "galaxy", "laptop", "phone", "specs", "gadget", 
                        "headphone", "smartwatch", "tv", "console", "playstation", "xbox",
                        "pixel", "oneplus", "airpods", "ipad", "kindle", "gopro", "drone",
                        "camera", "monitor", "keyboard", "mouse", "gpu", "processor", "chip"}
    if any(k in q for k in product_keywords):
        return "Product"

    # === ANIMALS & WILDLIFE ===
    animal_keywords = {"lion", "tiger", "elephant", "dog", "cat", "animal", "wildlife", "habitat",
                       "species", "fauna", "reptile", "bird", "fish", "whale", "dolphin", "shark",
                       "snake", "eagle", "wolf", "bear", "deer", "monkey", "gorilla", "panda",
                       "penguin", "cheetah", "leopard", "rhinoceros", "hippopotamus", "crocodile",
                       "dinosaur", "insect", "butterfly", "horse", "cow", "parrot", "owl"}
    if any(k in q for k in animal_keywords):
        return "Animal"

    # === EDUCATIONAL & SCIENCE ===
    educational_keywords = {"quantum", "physics", "chemistry", "biology", "mathematics", "calculus",
                            "equation", "theory", "science", "astronomy", "geology", "ecology",
                            "thermodynamics", "relativity", "evolution", "genetics", "neuroscience",
                            "engineering", "statistics", "probability", "linear algebra", "topology"}
    if any(k in q for k in educational_keywords):
        return "Educational"

    # === MOVIES & ENTERTAINMENT ===
    movie_keywords = {"movie", "film", "cinema", "director", "box office", "imdb", "trailer",
                      "oscar", "emmy", "grammy", "tv show", "series", "anime", "cartoon"}
    if any(k in q for k in movie_keywords):
        return "Movie"

    # === BOOKS & LITERATURE ===
    book_keywords = {"book", "novel", "author", "publisher", "isbn", "bestseller", "literary",
                     "fiction", "non-fiction", "manga", "comic", "graphic novel"}
    if any(k in q for k in book_keywords):
        return "Book"

    return "Generic"

def inject_intelligent_ui_rules(system_prompt: str) -> str:
    """
    Injects Intelligent UI Matrix Rules into AI system prompts.
    """
    matrix_prompt = "\n\n[🎨 LOTAI INTELLIGENT UI RULES MATRIX]:\n"
    matrix_prompt += "You MUST enforce these exact UI Component Rules based on the query Content Type:\n"
    matrix_prompt += "• Places: Hero Image ✅ | Gallery ✅ | Timeline ✅ | Map ✅ | Quick Facts ✅ | FAQ ✅\n"
    matrix_prompt += "• People: Hero Image ✅ | Gallery ✅ | Timeline ✅ | Map ❌ | Quick Facts ✅ | FAQ ✅\n"
    matrix_prompt += "• Programming / Coding / CS: Hero Image ❌ | Gallery ❌ | Timeline ❌ | Map ❌ | Quick Facts ⚪ | Code Blocks ✅ | FAQ ✅\n"
    matrix_prompt += "• Education / Science: Hero Image ⚪ | Gallery ❌ | Timeline ❌ | Map ❌ | Quick Facts ⚪ | FAQ ✅\n"
    matrix_prompt += "• Companies: Hero Image ✅ | Gallery ✅ | Timeline ✅ | Quick Facts ✅ | FAQ ✅\n"
    matrix_prompt += "• Products / Movies / Recipes: Hero Image ✅ | Gallery ✅ | Quick Facts ✅ | FAQ ✅\n"
    matrix_prompt += "• Diseases: Hero Image ⚪ | Gallery ❌ | Timeline ❌ | Quick Facts ✅ | FAQ ✅\n"
    matrix_prompt += "• Animals: Hero Image ✅ | Gallery ✅ | Map ✅ | Quick Facts ✅ | FAQ ✅\n\n"
    matrix_prompt += "CRITICAL: Do NOT generate Timelines, Maps, or Galleries for Programming or Educational topics! Only include checked UI blocks for each specific content category.\n"
    
    return system_prompt + matrix_prompt
