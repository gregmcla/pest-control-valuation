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
        """Initialize with lightweight models"""
        try:
            # Use smaller models
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                cache_dir=model_cache_dir,
                model_kwargs={"low_cpu_mem_usage": True}
            )
            # Remove zero-shot classifier to save memory
            self.zero_shot_classifier = None
            gc.collect()  # Force garbage collection
        except Exception as e:
            print(f"Warning: Using fallback mode due to model loading error: {e}")
            self.sentiment_analyzer = self._fallback_sentiment

    def _fallback_sentiment(self, text):
        """Fallback sentiment analysis when model fails"""
        return [{"label": "NEUTRAL", "score": 0.5}]

    def _fallback_classifier(self, text, labels):
        """Fallback classification when model fails"""
        return {"labels": labels, "scores": [1.0/len(labels)]*len(labels)}

    def analyze_market_trends(self, industry: str) -> Dict:
        """Analyze market trends with memory optimization"""
        try:
            tickers = INDUSTRY_TICKERS.get(industry, [])[:2]  # Limit to 2 tickers
            market_data = self._get_market_data(tickers)
            
            result = {
                "market_sentiment": self._analyze_sentiment(industry),
                "growth_potential": self._predict_growth(market_data),
                "risk_factors": self._identify_risks(industry)[:3],  # Limit risks
                "opportunities": self._find_opportunities(market_data, industry)[:2]  # Limit opportunities
            }
            
            # Clean up
            del market_data
            gc.collect()
            
            return result
        except Exception as e:
            print(f"Error in market analysis: {e}")
            return self._get_fallback_analysis()

    def _get_market_data(self, tickers: List[str]) -> pd.DataFrame:
        """Fetch market data with enhanced error handling"""
        if not tickers:
            return pd.DataFrame()
        try:
            df = yf.download(tickers, period="1y", progress=False)['Adj Close']
            if df.empty:
                raise ValueError("No market data available")
            return df
        except Exception as e:
            print(f"Error fetching market data: {e}")
            return pd.DataFrame()

    def _analyze_sentiment(self, industry: str) -> Dict:
        """Analyze industry sentiment"""
        news_headlines = self._fetch_industry_news(industry)
        sentiments = [
            self.sentiment_analyzer(headline)[0] 
            for headline in news_headlines[:5]
        ]
        
        return {
            "overall_sentiment": self._aggregate_sentiment(sentiments),
            "confidence": sum(s['score'] for s in sentiments) / len(sentiments),
            "trend": self._determine_trend(sentiments)
        }

    def _predict_growth(self, market_data: pd.DataFrame) -> Dict:
        """Predict industry growth potential"""
        if market_data.empty:
            return {"prediction": "neutral", "confidence": 0.5}
            
        return {
            "short_term": self._calculate_growth_metrics(market_data, '3M'),
            "medium_term": self._calculate_growth_metrics(market_data, '6M'),
            "long_term": self._calculate_growth_metrics(market_data, '1Y')
        }

    def _identify_risks(self, industry: str) -> List[Dict]:
        """Identify industry-specific risks"""
        risk_categories = [
            "Economic", "Regulatory", "Competition",
            "Technology", "Market", "Operational"
        ]
        
        risks = []
        for category in risk_categories:
            risk_level = self._assess_risk_level(industry, category)
            if risk_level['score'] > 0.3:
                risks.append({
                    "category": category,
                    "level": risk_level['level'],
                    "impact": risk_level['impact'],
                    "mitigation": self._generate_risk_mitigation(category)
                })
        
        return risks

    def _find_opportunities(self, market_data: pd.DataFrame, industry: str) -> List[Dict]:
        """Identify growth opportunities"""
        opportunities = []
        
        # Market expansion opportunities
        market_gaps = self._analyze_market_gaps(industry)
        if market_gaps:
            opportunities.extend(market_gaps)
            
        # Technology adoption opportunities
        tech_opportunities = self._analyze_tech_opportunities(industry)
        if tech_opportunities:
            opportunities.extend(tech_opportunities)
            
        return opportunities

    def _fetch_industry_news(self, industry: str) -> List[str]:
        """Mock news fetching - replace with actual API"""
        return [
            f"Industry leaders in {industry} report strong growth",
            f"New technologies reshape {industry} landscape",
            f"Market outlook positive for {industry} sector",
            f"{industry} companies adapt to changing market conditions",
            f"Innovation drives {industry} transformation"
        ]

    def _calculate_growth_metrics(self, data: pd.DataFrame, period: str) -> Dict:
        """Calculate growth metrics for a given period"""
        return {
            "rate": 0.15,  # Replace with actual calculation
            "confidence": 0.8,
            "factors": ["Market expansion", "Technology adoption"],
            "recommendations": [
                "Invest in digital transformation",
                "Expand market presence",
                "Optimize operations"
            ]
        }

    def _assess_risk_level(self, industry: str, category: str) -> Dict:
        """Assess risk level for a given category"""
        # Implement risk scoring logic
        return {
            "level": "medium",
            "score": 0.4,
            "impact": "moderate",
            "factors": ["Market volatility", "Competitive pressure"]
        }

    def _get_fallback_analysis(self) -> Dict:
        """Provide fallback analysis when main analysis fails"""
        return {
            "market_sentiment": {
                "overall_sentiment": "neutral",
                "confidence": 0.5,
                "trend": "stable"
            },
            "growth_potential": {
                "short_term": {
                    "rate": 0.05,
                    "confidence": 0.5,
                    "factors": ["Market stability"],
                    "recommendations": ["Consider market research"]
                },
                "medium_term": {
                    "rate": 0.05,
                    "confidence": 0.5,
                    "factors": ["Industry average growth"],
                    "recommendations": ["Monitor market trends"]
                },
                "long_term": {
                    "rate": 0.05,
                    "confidence": 0.5,
                    "factors": ["Economic conditions"],
                    "recommendations": ["Plan for sustainability"]
                }
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
                    "potential": "Medium",
                    "investment_required": "Moderate",
                    "expected_roi": "10-15%"
                }
            ]
        }