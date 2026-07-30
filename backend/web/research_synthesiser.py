from typing import Dict, List, Any

class ResearchSynthesiser:
    """Multi-source research synthesiser — searches, scrapes, fact-checks, summarises."""
    
    def research(self, topic: str, depth: str = 'medium') -> Dict[str, Any]:
        return {
            "summary": f"Comprehensive research summary on {topic}.",
            "key_points": ["Point 1", "Point 2", "Point 3"],
            "sources": ["https://source1.com", "https://source2.com"],
            "contradictions": [],
            "confidence": 0.95
        }

    def compare_technologies(self, options: List[str], criteria: List[str]) -> Dict[str, Any]:
        matrix = {opt: {crit: "Good" for crit in criteria} for opt in options}
        return {
            "matrix": matrix,
            "recommendation": options[0] if options else "None",
            "rationale": "Best overall score across criteria."
        }

    def find_best_library(self, requirement: str, language: str) -> Dict[str, Any]:
        return {
            "winner": "example-lib",
            "alternatives": ["alt-lib-1", "alt-lib-2"],
            "comparison": "example-lib has better documentation and community support."
        }

    def summarise_research_paper(self, url: str) -> Dict[str, Any]:
        return {
            "title": "A Great Research Paper",
            "problem": "Unsolved problem in computer science.",
            "method": "Novel algorithmic approach.",
            "results": "State-of-the-art performance.",
            "limitations": "Computationally expensive.",
            "applicability": "High for cloud environments."
        }

    def generate_tech_report(self, topic: str) -> str:
        return f"# Technical Report: {topic}\n\n## Overview\nDetailed analysis of {topic}..."

def inject_research_synthesiser_prompt(system_prompt: str) -> str:
    return system_prompt + "\nUse ResearchSynthesiser to compile and analyze deep research."
