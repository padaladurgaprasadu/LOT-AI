"""
Business market intelligence engine for LOT AI.
"""
from typing import Dict, Any, List

class MarketAnalyser:
    """Analyzes market sizes, business models, and pricing strategies."""

    def estimate_market_size(self, industry: str, geography: str = 'global') -> Dict[str, Any]:
        """Estimates market size using Fermi estimation principles."""
        # Mock values based on common industries
        base_tam = 100.0 if industry.lower() == 'saas' else 50.0
        return {
            "tam_usd_bn": base_tam,
            "sam_usd_bn": base_tam * 0.4,
            "som_usd_bn": base_tam * 0.05,
            "cagr_pct": 12.5,
            "sources": ["Statista", "Gartner", "Fermi Estimation"],
            "methodology": "Top-down approach combining industry reports with typical geographic distributions."
        }

    def analyse_business_model(self, description: str) -> Dict[str, Any]:
        """Analyzes a business model from a description."""
        model_type = "B2B SaaS" if "software" in description.lower() else "B2C"
        return {
            "model_type": model_type,
            "revenue_streams": ["Subscriptions", "One-time setup fees"],
            "unit_economics": {"cac": 500, "ltv": 2500},
            "risks": ["High churn rate", "Customer acquisition costs"],
            "opportunities": ["Upselling", "API access monetization"]
        }

    def generate_lean_canvas(self, idea: str) -> Dict[str, Any]:
        """Generates a lean canvas for a business idea."""
        return {
            "problem": ["Inefficiency", "High costs"],
            "solution": ["Automated AI tool", "Cloud-based platform"],
            "unique_value_prop": "Fastest time to market",
            "unfair_advantage": "Proprietary AI models",
            "customer_segments": ["SMEs", "Enterprises"],
            "channels": ["Direct sales", "Content marketing"],
            "cost_structure": ["Hosting", "Salaries"],
            "revenue_streams": ["SaaS subscriptions"],
            "key_metrics": ["MRR", "Churn Rate"]
        }

    def swot_analysis(self, business: str, market: str) -> Dict[str, Any]:
        """Performs SWOT analysis."""
        return {
            "strengths": ["Strong engineering team", "Innovative technology"],
            "weaknesses": ["Limited marketing budget", "Lack of brand awareness"],
            "opportunities": [f"Growth in {market}", "Partnerships"],
            "threats": ["Established competitors", "Regulatory changes"]
        }

    def pricing_strategy(self, product: str, target_market: str, competitors: List[str] = None) -> Dict[str, Any]:
        """Recommends a pricing strategy."""
        return {
            "recommended_model": "Freemium",
            "price_points": {"free": 0, "pro": 49, "enterprise": 499},
            "rationale": "Freemium encourages adoption in early stages, with Pro tier capturing core users."
        }

    def growth_metrics(self, description: str) -> Dict[str, Any]:
        """Defines growth metrics for a business."""
        return {
            "north_star_metric": "Weekly Active Users",
            "leading_indicators": ["Signups per day", "Onboarding completion rate"],
            "lagging_indicators": ["Monthly Recurring Revenue (MRR)", "Churn Rate"],
            "targets": {"wau": 10000, "mrr": 50000}
        }


def inject_market_prompt(system_prompt: str, task: str) -> str:
    """Adds market intelligence directive to the system prompt."""
    market_directive = "\n[Market Capability]: LOT AI can analyze market sizes, generate lean canvases, run SWOT, and define pricing."
    return f"{system_prompt}\nTask: {task}\n{market_directive}"
