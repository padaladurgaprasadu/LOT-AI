"""
PrismAI Y-Combinator GStack Engine
===================================
Inspired by Garry Tan's gstack (https://github.com/garrytan/gstack).
Enforces Y-Combinator production engineering standards, rapid MVP execution,
and type-safe Next.js/React + FastAPI + PostgreSQL stack templates.
"""

def inject_gstack_prompt(system_prompt: str) -> str:
    """
    Injects Y-Combinator gstack production standards & stack blueprints.
    """
    gstack_prompt = "\n\n[🚀 PRISMAI Y-COMBINATOR GSTACK ENGINE (Garry Tan gstack Architecture)]:\n"
    gstack_prompt += "• YC Production Stack: Enforces Next.js/React + TypeScript + Tailwind CSS + FastAPI + PostgreSQL (Prisma/Supabase).\n"
    gstack_prompt += "• Rapid Startup Execution: Generates clean, scalable, production-ready SaaS architectures tuned for YC startup velocity.\n"
    gstack_prompt += "• End-to-End Type Safety: Enforces strict TypeScript schemas from database models to frontend UI components.\n\n"
    
    return system_prompt + gstack_prompt
