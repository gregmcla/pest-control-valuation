
from decimal import Decimal
from typing import Dict

class ValuationService:
    INDUSTRY_MULTIPLES = {
        "SaaS": 8.5,
        "Pest Control": 5.5,
        "HVAC": 4.8,
        # Add other industries...
    }

    def calculate(self, data: Dict) -> Dict:
        revenue = Decimal(str(data.get("annualRevenue", 0)))
        ebitda = Decimal(str(data.get("ebitda", revenue * Decimal("0.15"))))
        industry = data.get("industry", "")
        
        multiple = self.INDUSTRY_MULTIPLES.get(industry, 5.0)
        valuation = ebitda * Decimal(str(multiple))

        return {
            "valuation": float(valuation),
            "multiple": multiple,
            "metrics": {
                "revenue": float(revenue),
                "ebitda": float(ebitda),
                "ebitda_margin": float(ebitda / revenue * 100) if revenue else 0
            }
        }