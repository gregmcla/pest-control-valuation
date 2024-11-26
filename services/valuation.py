
from decimal import Decimal
from typing import Dict
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from pest_control_valuation.services.constants import INDUSTRY_MULTIPLES
except ImportError:
    from services.constants import INDUSTRY_MULTIPLES

class ValuationService:
    def calculate(self, data: Dict) -> Dict:
        revenue = Decimal(str(data.get("annualRevenue", 0)))
        ebitda = Decimal(str(data.get("ebitda", revenue * Decimal("0.15"))))
        industry = data.get("industry", "")
        
        multiple = INDUSTRY_MULTIPLES.get(industry, Decimal("5.0"))
        valuation = ebitda * multiple

        return {
            "value": float(valuation),
            "multiple": float(multiple),
            "metrics": {
                "revenue": float(revenue),
                "ebitda": float(ebitda),
                "ebitda_margin": float(ebitda / revenue * 100) if revenue else 0
            }
        }