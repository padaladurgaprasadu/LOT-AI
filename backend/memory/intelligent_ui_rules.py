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
