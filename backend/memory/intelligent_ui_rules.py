"""
PrismAI Intelligent UI Rules Matrix
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
    [Person, Place, Educational, Product, Company, Disease, Movie, Book, News, Recipe, Programming, Generic]
    """
    q = query.lower().strip()
    
    prog_keywords = {"code", "python", "java", "js", "typescript", "c++", "cpp", "c#", "golang", "rust", "html", "css", "react", "algorithm", "dsa", "oop", "function", "class", "bug", "error", "api", "database", "sql"}
    if any(k in q.split() for k in prog_keywords) or "how to code" in q or "build a" in q:
        return "Programming"

    place_keywords = {"temple", "city", "country", "state", "fort", "lake", "mountain", "river", "park", "museum", "airport", "tirupati", "paris", "london", "tokyo", "taj mahal", "kedarnath", "sabarimala", "vijayawada"}
    if any(k in q for k in place_keywords):
        return "Place"

    people_keywords = {"who is", "biography", "ceo", "founder", "president", "prime minister", "actor", "scientist", "elon musk", "apj abdul kalam", "steve jobs"}
    if any(k in q for k in people_keywords):
        return "Person"

    company_keywords = {"inc", "corp", "ltd", "google", "apple", "microsoft", "nvidia", "amazon", "tesla", "meta", "tcs", "infosys"}
    if any(k in q for k in company_keywords):
        return "Company"

    disease_keywords = {"disease", "syndrome", "symptom", "fever", "virus", "infection", "cancer", "diabetes", "treatment"}
    if any(k in q for k in disease_keywords):
        return "Disease"

    recipe_keywords = {"recipe", "how to cook", "dish", "curry", "biryani", "ingredients", "baking"}
    if any(k in q for k in recipe_keywords):
        return "Recipe"

    product_keywords = {"iphone", "macbook", "galaxy", "laptop", "phone", "specs", "gadget", "headphone", "smartwatch", "tv", "console", "playstation", "xbox"}
    if any(k in q for k in product_keywords):
        return "Product"

    animal_keywords = {"lion", "tiger", "elephant", "dog", "cat", "animal", "wildlife", "habitat", "species", "fauna", "reptile", "bird"}
    if any(k in q for k in animal_keywords):
        return "Animal"

    educational_keywords = {"quantum", "physics", "chemistry", "biology", "mathematics", "calculus", "equation", "theory", "science"}
    if any(k in q for k in educational_keywords):
        return "Educational"

    movie_keywords = {"movie", "film", "cinema", "director", "box office", "imdb"}
    if any(k in q for k in movie_keywords):
        return "Movie"

    book_keywords = {"book", "novel", "author", "publisher", "isbn"}
    if any(k in q for k in book_keywords):
        return "Book"

    return "Generic"

def inject_intelligent_ui_rules(system_prompt: str) -> str:
    """
    Injects Intelligent UI Matrix Rules into AI system prompts.
    """
    matrix_prompt = "\n\n[🎨 PRISMAI INTELLIGENT UI RULES MATRIX]:\n"
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
