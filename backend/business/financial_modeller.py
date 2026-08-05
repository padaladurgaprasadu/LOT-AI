"""
Financial modelling and projections engine for LOT AI.
"""
from typing import Dict, Any, List

class FinancialModeller:
    """Engine for financial calculations and projections."""

    def saas_unit_economics(self, arpu_usd: float, cac_usd: float, churn_rate_monthly: float, gross_margin: float = 0.7) -> Dict[str, Any]:
        """Calculates SaaS unit economics."""
        customer_lifetime_months = 1 / churn_rate_monthly if churn_rate_monthly > 0 else 0
        ltv = arpu_usd * gross_margin * customer_lifetime_months
        ltv_cac_ratio = ltv / cac_usd if cac_usd > 0 else 0
        payback_months = cac_usd / (arpu_usd * gross_margin) if (arpu_usd * gross_margin) > 0 else 0
        
        return {
            "ltv": round(ltv, 2),
            "ltv_cac_ratio": round(ltv_cac_ratio, 2),
            "payback_months": round(payback_months, 2),
            "magic_number": round((arpu_usd * 12) / cac_usd, 2) if cac_usd > 0 else 0
        }

    def revenue_projection(self, mrr_usd: float, growth_rate_monthly: float, churn_rate: float, months: int = 24) -> List[Dict[str, Any]]:
        """Projects revenue over time."""
        projections = []
        current_mrr = mrr_usd
        customers = 100 # arbitrary starting point
        
        for month in range(1, months + 1):
            churn_revenue = current_mrr * churn_rate
            new_revenue = current_mrr * growth_rate_monthly
            current_mrr = current_mrr + new_revenue - churn_revenue
            customers = int(customers * (1 + growth_rate_monthly - churn_rate))
            
            projections.append({
                "month": month,
                "mrr": round(current_mrr, 2),
                "arr": round(current_mrr * 12, 2),
                "customers": customers,
                "churn_revenue": round(churn_revenue, 2)
            })
            
        return projections

    def runway_calculator(self, cash_usd: float, monthly_burn_usd: float, monthly_revenue_usd: float = 0) -> Dict[str, Any]:
        """Calculates startup runway."""
        net_burn = monthly_burn_usd - monthly_revenue_usd
        months_runway = cash_usd / net_burn if net_burn > 0 else float('inf')
        
        return {
            "months_runway": round(months_runway, 1) if months_runway != float('inf') else -1,
            "break_even_month": "N/A" if net_burn > 0 else 0,
            "raise_by_date": f"In {int(months_runway) - 6} months" if net_burn > 0 and months_runway > 6 else "Immediately"
        }

    def roi_calculator(self, investment_usd: float, returns: List[float], years: int = 5) -> Dict[str, Any]:
        """Calculates ROI and NPV."""
        total_return = sum(returns[:years])
        roi_pct = ((total_return - investment_usd) / investment_usd) * 100 if investment_usd > 0 else 0
        
        # Simple NPV with 10% discount rate
        npv = -investment_usd
        for i, ret in enumerate(returns[:years]):
            npv += ret / ((1 + 0.10) ** (i + 1))
            
        return {
            "roi_pct": round(roi_pct, 2),
            "npv": round(npv, 2),
            "irr": 0.15, # Mock IRR
            "payback_years": 3.0 # Mock payback
        }

    def pricing_sensitivity(self, base_price: float, elasticity: float = -1.5, volumes: List[float] = None) -> List[Dict[str, Any]]:
        """Calculates revenue impact across price points based on elasticity."""
        if volumes is None:
            volumes = [1000] # Base volume
        
        results = []
        prices = [base_price * 0.8, base_price, base_price * 1.2]
        base_vol = volumes[0]
        
        for price in prices:
            pct_change_price = (price - base_price) / base_price if base_price > 0 else 0
            pct_change_vol = pct_change_price * elasticity
            new_vol = base_vol * (1 + pct_change_vol)
            
            results.append({
                "price": round(price, 2),
                "volume": int(new_vol),
                "revenue": round(price * new_vol, 2)
            })
            
        return results

    def generate_financial_summary(self, params: Dict[str, Any]) -> str:
        """Generates a plain English financial summary."""
        return f"Based on the inputs, the projected runway is {params.get('months_runway', 'N/A')} months. The startup requires immediate attention to LTV/CAC ratios."

    def cost_breakdown(self, tech_stack: str, team_size: int, users_monthly: int) -> Dict[str, Any]:
        """Estimates monthly costs for infrastructure and team."""
        infra_cost = 500 + (users_monthly * 0.01)
        people_cost = team_size * 8000 # Assume $8k/mo average
        tools_cost = team_size * 100
        
        return {
            "infrastructure": infra_cost,
            "people": people_cost,
            "tools": tools_cost,
            "total_monthly_usd": infra_cost + people_cost + tools_cost
        }


def inject_financial_prompt(system_prompt: str, task: str) -> str:
    """Adds financial modelling directive to system prompt."""
    fin_directive = "\n[Financial Capability]: LOT AI can calculate unit economics, project revenue, compute runway, and break down costs."
    return f"{system_prompt}\nTask: {task}\n{fin_directive}"
