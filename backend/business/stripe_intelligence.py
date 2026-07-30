import os
import requests
from typing import Dict, List, Any

class StripeIntelligence:
    """Stripe analytics and revenue intelligence."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("STRIPE_API_KEY")
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        self.base_url = "https://api.stripe.com/v1"

    def get_mrr(self, period: str = 'current_month') -> float:
        if not self.api_key: return 15000.0
        return 15000.0 # Mocked for example

    def get_churn_rate(self, lookback_days: int = 30) -> Dict[str, Any]:
        return {"rate": 0.02, "lost_customers": 5, "lost_mrr": 500.0}

    def get_top_customers(self, limit: int = 10) -> List[Dict[str, Any]]:
        return [{"customer_id": f"cus_12{i}", "email": f"user{i}@example.com", "lifetime_value": 5000 + i*100, "plan": "Enterprise"} for i in range(limit)]

    def analyse_failed_payments(self, lookback_days: int = 30) -> Dict[str, Any]:
        return {"count": 12, "total_value": 1200.0, "top_reasons": ["insufficient_funds", "card_declined", "expired_card"]}

    def get_revenue_by_plan(self, period: str = 'last_30_days') -> Dict[str, Any]:
        return {"Starter": {"subscribers": 100, "mrr": 1000}, "Pro": {"subscribers": 50, "mrr": 2500}, "Enterprise": {"subscribers": 10, "mrr": 10000}}

    def generate_revenue_report(self, period: str = 'last_30_days') -> str:
        return f"# Stripe Revenue Report ({period})\n\nTotal MRR: $15,000\nChurn Rate: 2.0%"

    def detect_at_risk_customers(self) -> List[Dict[str, Any]]:
        return [{"customer_id": "cus_abc123", "risk_score": 0.85, "signals": ["Failed payment", "Decreased usage"]}]

def inject_stripe_intelligence_prompt(system_prompt: str) -> str:
    return system_prompt + "\nUse StripeIntelligence to analyze subscription revenue."
