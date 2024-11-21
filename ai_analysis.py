from transformers import pipeline
import yfinance as yf
import pandas as pd
from typing import Dict, List
import gc  # Add garbage collection

INDUSTRY_TICKERS = {
    "SaaS": ["CRM", "MSFT", "WDAY", "NOW"],
    "IT Consulting": ["ACN", "CTSH", "EPAM"],
    "Healthcare": ["HCA", "UNH", "THC"],
    "Manufacturing": ["GE", "MMM", "CAT"],
    "Pest Control": ["ROLLINS", "BWXT"],
    "HVAC": ["CARR", "TT", "JCI"]
}

class ValuationAI:
    def __init__(self, model_cache_dir='/tmp/models'):
        self.cache_dir = model_cache_dir
        self.model = pipeline('text-generation', model='gpt-2', cache_dir=model_cache_dir)

    def analyze_market_trends(self, industry: str) -> dict:
        """Simple market trends analysis"""
        return {
            "market_sentiment": "positive",
            "growth_potential": {
                "short_term": {"rate": 0.15, "confidence": 0.8},
                "medium_term": {"rate": 0.20, "confidence": 0.7},
                "long_term": {"rate": 0.25, "confidence": 0.6}
            },
            "risk_factors": [
                {
                    "category": "Market",
                    "level": "medium",
                    "impact": "moderate",
                    "mitigation": "Regular market analysis"
                }
            ],
            "opportunities": [
                {
                    "type": "Market Expansion",
                    "potential": "High",
                    "investment_required": "Medium",
                    "expected_roi": "15-25%"
                }
            ]
        }

    def generate_insights(self, data):
        # Generate insights using the model
        # ...existing code...

        # Clean up to free memory
        del self.model
        gc.collect()