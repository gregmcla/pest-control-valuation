from typing import Dict, List
import pandas as pd
from decimal import Decimal
import logging

class CompetitiveAnalysis:
    def analyze_market_position(self, metrics: Dict, industry_data: Dict) -> Dict:
        """Analyze competitive position with error handling"""
        try:
            market_share = self._calculate_market_share(metrics)
            advantages = self._identify_advantages(metrics)
            threats = self._analyze_threats(metrics, industry_data)
            
            return {
                "market_position": {
                    "share": market_share,
                    "rank": self._determine_market_rank(market_share),
                    "trend": self._analyze_trend(metrics)
                },
                "competitive_advantages": advantages,
                "threats": threats,
                "opportunities": self._identify_opportunities(metrics, industry_data),
                "strategic_recommendations": self._generate_recommendations(
                    market_share, advantages, threats
                )
            }
        except Exception as e:
            logging.error(f"Error in competitive analysis: {str(e)}")
            return self._get_fallback_analysis()

    def _get_fallback_analysis(self) -> Dict:
        """Provide fallback analysis when errors occur"""
        return {
            "market_position": {
                "share": 0,
                "rank": "Unknown",
                "trend": {"direction": "stable", "strength": "unknown"}
            },
            "competitive_advantages": [],
            "threats": [],
            "opportunities": []
        }

    def _calculate_market_share(self, metrics: Dict) -> float:
        """Calculate market share based on revenue and industry size"""
        revenue = float(metrics.get("revenue", 0))
        industry_revenue = self._get_industry_revenue(metrics["industry"])
        return (revenue / industry_revenue) * 100 if industry_revenue else 0

    def _identify_advantages(self, metrics: Dict) -> List[Dict]:
        """Identify competitive advantages"""
        advantages = []
        
        # Analyze operational efficiency
        if metrics["ebitda_margin"] > Decimal("20"):
            advantages.append({
                "type": "Operational Efficiency",
                "strength": "High",
                "sustainability": "Strong",
                "impact": "Significant cost advantage"
            })
            
        # Analyze market presence
        if metrics["geographic_reach"] > Decimal("5"):
            advantages.append({
                "type": "Market Coverage",
                "strength": "Strong",
                "sustainability": "High",
                "impact": "Wide market access"
            })
            
        return advantages

    def _analyze_threats(self, metrics: Dict, industry_data: Dict) -> List[Dict]:
        """Analyze competitive threats"""
        threats = []
        
        # Market competition analysis
        market_concentration = self._calculate_market_concentration(industry_data)
        if market_concentration > 0.7:  # High concentration
            threats.append({
                "type": "Market Competition",
                "severity": "High",
                "immediacy": "Immediate",
                "mitigation": "Differentiate services and build brand loyalty"
            })
            
        return threats

    def _generate_recommendations(self, market_share: float, 
                                advantages: List[Dict], 
                                threats: List[Dict]) -> List[Dict]:
        """Generate strategic recommendations"""
        recommendations = []
        
        # Market position-based recommendations
        if market_share < 10:
            recommendations.append({
                "priority": "High",
                "action": "Market Expansion",
                "details": "Focus on gaining market share through targeted marketing",
                "timeline": "6-12 months"
            })
            
        return recommendations

    def _get_industry_revenue(self, industry: str) -> float:
        """Get total industry revenue - replace with actual data source"""
        industry_revenues = {
            "SaaS": 1000000000000,  # $1T
            "IT Consulting": 500000000000,  # $500B
            "Pest Control": 20000000000,  # $20B
            # Add other industries...
        }
        return industry_revenues.get(industry, 0)

    def _determine_market_rank(self, market_share: float) -> str:
        """Determine market position rank"""
        if market_share > 20:
            return "Market Leader"
        elif market_share > 10:
            return "Strong Competitor"
        elif market_share > 5:
            return "Established Player"
        return "Emerging Player"

    def _analyze_trend(self, metrics: Dict) -> Dict:
        """Analyze growth trend"""
        return {
            "direction": "up" if metrics["growth_rate"] > 0 else "down",
            "strength": self._calculate_trend_strength(metrics),
            "sustainability": self._assess_trend_sustainability(metrics)
        }

    def _identify_opportunities(self, metrics: Dict, industry_data: Dict) -> List[Dict]:
        """Identify market opportunities"""
        return [
            {
                "type": "Geographic Expansion",
                "potential": "High" if metrics["geographic_reach"] < 5 else "Medium",
                "investment_required": self._estimate_investment_need(metrics),
                "expected_roi": "25-35%"
            },
            {
                "type": "Service Diversification",
                "potential": "Medium",
                "investment_required": "Moderate",
                "expected_roi": "15-25%"
            }
        ]

    def _calculate_market_concentration(self, industry_data: Dict) -> float:
        """Calculate market concentration (HHI)"""
        # Simplified HHI calculation
        return 0.4  # Replace with actual calculation

    def _calculate_trend_strength(self, metrics: Dict) -> str:
        """Calculate trend strength"""
        growth_rate = float(metrics["growth_rate"])
        if abs(growth_rate) > 20:
            return "Strong"
        elif abs(growth_rate) > 10:
            return "Moderate"
        return "Weak"