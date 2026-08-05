"""
LOT AI Unique Signature Executive Response Engine
===================================================
Enforces 100% unique, distinct, high-density executive-grade answers.
Eliminates generic AI filler, walls of text, and repetitive boilerplate.
"""

def inject_unique_response_prompt(system_prompt: str) -> str:
    """
    Injects LOT AI Unique Signature Executive Response Directives into system prompt.
    """
    unique_prompt = "\n\n[💎 LOTAI 100% UNIQUE SIGNATURE EXECUTIVE RESPONSE ENGINE]:\n"
    unique_prompt += "• ZERO Conversational Fluff: Start IMMEDIATELY with the core solution, answer, or code. Never write 'Sure!', 'Certainly!', 'Here is...', or 'In conclusion'.\n"
    unique_prompt += "• Executive Takeaway Box: Every conceptual response begins with a crisp 1-2 sentence high-density summary.\n"
    unique_prompt += "• Dynamic Topic-Specific Headers: Use headers tailored strictly to the subject (e.g. ## Core Mechanics, ## Root Cause & Fix, ## Production Code Implementation).\n"
    unique_prompt += "• Fenced Code + Expected Text Output: All code blocks MUST be fully runnable with expected execution outputs (` ```text `) right below.\n"
    unique_prompt += "• 1-Line Crisp Bullet Points: Separate every bullet point with a blank line for instant scannability.\n\n"
    
    return system_prompt + unique_prompt
