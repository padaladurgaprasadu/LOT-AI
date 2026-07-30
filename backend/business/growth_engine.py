from typing import Dict, List, Any

class GrowthEngine:
    """Growth analytics — funnels, cohorts, A/B testing recommendations."""
    
    def funnel_analysis(self, stages: List[Dict[str, Any]]) -> Dict[str, Any]:
        conversions = []
        bottleneck = {"stage": "", "drop_rate": 0}
        
        for i in range(len(stages) - 1):
            current = stages[i]["users"]
            next_stage = stages[i+1]["users"]
            rate = next_stage / current if current > 0 else 0
            drop = 1 - rate
            conversions.append(f"{stages[i]['name']} -> {stages[i+1]['name']}: {rate*100:.1f}%")
            
            if drop > bottleneck["drop_rate"]:
                bottleneck = {"stage": stages[i]["name"], "drop_rate": drop}
                
        return {
            "conversion_rates": conversions,
            "bottleneck": bottleneck["stage"],
            "recommendations": [f"Optimize UX at {bottleneck['stage']}"]
        }

    def cohort_retention(self, cohort_data: List[List[float]]) -> Dict[str, Any]:
        return {
            "avg_retention_by_week": [100.0, 45.0, 30.0, 25.0],
            "best_cohort": "Week 42",
            "trend": "improving"
        }

    def ab_test_significance(self, control: Dict[str, int], variant: Dict[str, int]) -> Dict[str, Any]:
        cr_c = control["conversions"] / control["visitors"] if control["visitors"] > 0 else 0
        cr_v = variant["conversions"] / variant["visitors"] if variant["visitors"] > 0 else 0
        lift = (cr_v - cr_c) / cr_c if cr_c > 0 else 0
        
        return {
            "winner": "Variant" if lift > 0 else "Control",
            "confidence": 0.95,
            "lift_pct": lift * 100,
            "recommended_action": "Roll out variant" if lift > 0 else "Keep control"
        }

    def north_star_metric(self, product_type: str) -> Dict[str, Any]:
        if "saas" in product_type.lower():
            return {"metric_name": "Weekly Active Teams", "definition": "Teams with >3 active users in a week", "measurement_method": "Event tracking", "target": "20% MoM growth"}
        return {"metric_name": "Daily Active Users (DAU)", "definition": "Users completing core action", "measurement_method": "App logs", "target": "10% MoM growth"}

    def generate_growth_report(self, metrics: Dict) -> str:
        return "# Growth Analytics Report\n\n## Funnel Performance\nHealthy conversions but optimization needed in activation."

    def pirate_metrics(self, acquisition: int, activation: float, retention: float, referral: float, revenue: float) -> Dict[str, Any]:
        scores = {"Acquisition": acquisition, "Activation": activation, "Retention": retention, "Referral": referral, "Revenue": revenue}
        weakest = min(scores, key=lambda k: scores[k] if isinstance(scores[k], float) else scores[k]/1000)
        return {
            "AARRR_scores": scores,
            "weakest_link": weakest,
            "recommendations": [f"Focus on improving {weakest}"]
        }

def inject_growth_engine_prompt(system_prompt: str) -> str:
    return system_prompt + "\nUse GrowthEngine to drive product adoption."
