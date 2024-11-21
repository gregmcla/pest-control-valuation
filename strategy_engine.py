from typing import Dict, List
import logging

class StrategyEngine:
    def __init__(self):
        pass

    def generate_recommendations(self, company_data: dict, market_analysis: dict) -> dict:
        """Generate comprehensive strategic recommendations"""
        immediate_actions = self.get_priority_actions(company_data, market_analysis)
        growth_plan = self.develop_growth_plan(company_data, market_analysis)
        risk_strategy = self.create_risk_strategy(company_data, market_analysis)
        value_drivers = self.identify_value_drivers(company_data)

        return {
            "summary": self._generate_summary(company_data, market_analysis),
            "immediate_actions": immediate_actions,
            "growth_strategy": growth_plan,
            "risk_mitigation": risk_strategy,
            "value_enhancement": value_drivers,
            "timeline": self._create_implementation_timeline(immediate_actions, growth_plan)
        }

    def get_priority_actions(self, data: dict, analysis: dict) -> list:
        """Determine priority actions based on analysis"""
        actions = []
        metrics = analysis.get("metrics", {})
        
        # Check profitability
        if metrics.get("ebitda_margin", 0) < 15:
            actions.append({
                "action": "Improve Operational Efficiency",
                "priority": "High",
                "timeline": "0-3 months",
                "expected_impact": "3-5% margin improvement"
            })
            
        # Check growth
        if metrics.get("growth_rate", 0) < 10:
            actions.append({
                "action": "Implement Growth Initiatives",
                "priority": "High",
                "timeline": "0-6 months",
                "expected_impact": "10-15% revenue increase"
            })
            
        return actions

    def _generate_summary(self, data: dict, analysis: dict) -> dict:
        """Generate executive summary"""
        return {
            "overview": self._create_overview(data),
            "key_findings": self._identify_key_findings(analysis),
            "critical_areas": self._identify_critical_areas(data, analysis),
            "expected_outcomes": self._project_outcomes(data, analysis)
        }

    def _create_implementation_timeline(self, actions: list, plan: dict) -> list:
        """Create implementation timeline"""
        timeline = []
        
        # Sort actions by priority and timeline
        for action in actions:
            timeline.append({
                "phase": "Immediate",
                "action": action["action"],
                "duration": action["timeline"],
                "dependencies": [],
                "resources_needed": self._estimate_resources(action)
            })
            
        return timeline

    def _estimate_resources(self, action: dict) -> dict:
        """Estimate required resources for action"""
        return {
            "budget": self._calculate_budget(action),
            "personnel": self._estimate_personnel_needs(action),
            "timeline": action.get("timeline", "3 months"),
            "external_support": self._determine_external_needs(action)
        }

    def develop_growth_plan(self, company_data, market_analysis):
        # Placeholder for growth plan logic
        return ["Growth Plan 1", "Growth Plan 2"]

    def create_risk_strategy(self, company_data, market_analysis):
        # Placeholder for risk strategy logic
        return ["Risk Strategy 1", "Risk Strategy 2"]

    def identify_value_drivers(self, company_data):
        # Placeholder for value drivers logic
        return ["Value Driver 1", "Value Driver 2"]

    def _create_overview(self, data: dict) -> dict:
        """Create business overview"""
        return {
            "size_category": self._determine_size_category(data),
            "market_position": self._assess_market_position(data),
            "growth_stage": self._determine_growth_stage(data),
            "risk_level": self._assess_risk_level(data)
        }

    def _identify_key_findings(self, analysis: dict) -> list:
        """Identify key findings from analysis"""
        findings = []
        metrics = analysis.get("metrics", {})
        
        if metrics.get("ebitda_margin", 0) < 15:
            findings.append({
                "area": "Profitability",
                "finding": "Below industry average margins",
                "impact": "High",
                "action_required": True
            })
            
        return findings

    def _identify_critical_areas(self, data: dict, analysis: dict) -> list:
        """Identify critical areas needing attention"""
        return [
            area for area in self._analyze_business_areas(data, analysis)
            if area["priority"] == "High"
        ]

    def _project_outcomes(self, data: dict, analysis: dict) -> dict:
        """Project potential outcomes"""
        return {
            "best_case": self._calculate_best_case(data),
            "expected": self._calculate_expected_case(data),
            "worst_case": self._calculate_worst_case(data)
        }

    def _calculate_budget(self, action: dict) -> str:
        """Calculate budget for action"""
        priority = action.get("priority", "Medium")
        return {
            "High": "$50,000-100,000",
            "Medium": "$25,000-50,000",
            "Low": "$10,000-25,000"
        }.get(priority, "$25,000-50,000")

    def _determine_size_category(self, data: dict) -> str:
        """Determine company size category"""
        revenue = float(data.get("annualRevenue", 0))
        if revenue > 50000000:
            return "Enterprise"
        elif revenue > 10000000:
            return "Mid-Market"
        elif revenue > 1000000:
            return "Small Business"
        return "Micro Business"

    def _assess_market_position(self, data: dict) -> str:
        """Assess market position"""
        market_share = float(data.get("marketShare", 0))
        if market_share > 20:
            return "Market Leader"
        elif market_share > 10:
            return "Strong Competitor"
        elif market_share > 5:
            return "Established Player"
        return "Market Entrant"

    def _determine_growth_stage(self, data: dict) -> str:
        """Determine company growth stage"""
        growth_rate = float(data.get("growthRate", 0))
        age = float(data.get("businessAge", 0))
        
        if growth_rate > 50 and age < 5:
            return "Early Growth"
        elif growth_rate > 20:
            return "Rapid Growth"
        elif growth_rate > 10:
            return "Steady Growth"
        return "Mature"

    def _assess_risk_level(self, data: dict) -> str:
        """Assess company risk level"""
        score = 0
        if float(data.get("customerRetention", 0)) > 80:
            score += 1
        if float(data.get("recurringRevenue", 0)) > float(data.get("annualRevenue", 1)) * 0.4:
            score += 1
        if float(data.get("geographicReach", 0)) > 3:
            score += 1
        return "Low" if score >= 2 else "Medium" if score == 1 else "High"
    
    def _analyze_business_areas(self, data: dict, analysis: dict) -> list:
        """Analyze critical business areas"""
        areas = []
        metrics = analysis.get("metrics", {})
        
        if metrics.get("ebitda_margin", 0) < 15:
            areas.append({
                "name": "Profitability",
                "priority": "High",
                "current": metrics.get("ebitda_margin", 0),
                "target": "20%"
            })
            
        if metrics.get("growth_rate", 0) < 10:
            areas.append({
                "name": "Growth",
                "priority": "High",
                "current": metrics.get("growth_rate", 0),
                "target": "15%"
            })
            
        return areas

    def _calculate_best_case(self, data: dict) -> dict:
        """Calculate best case scenario"""
        revenue = float(data.get("annualRevenue", 0))
        growth_rate = float(data.get("growthRate", 10))
        return {
            "revenue": revenue * 1.5,
            "growth_rate": min(growth_rate * 1.5, 50),
            "margin": min(float(data.get("ebitda", 0)) / revenue * 1.3, 35),
            "timeline": "2-3 years",
            "probability": "25%"
        }

    def _calculate_expected_case(self, data: dict) -> dict:
        """Calculate expected case scenario"""
        revenue = float(data.get("annualRevenue", 0))
        growth_rate = float(data.get("growthRate", 10))
        return {
            "revenue": revenue * 1.2,
            "growth_rate": min(growth_rate * 1.2, 30),
            "margin": min(float(data.get("ebitda", 0)) / revenue * 1.15, 25),
            "timeline": "12-18 months",
            "probability": "60%"
        }

    def _calculate_worst_case(self, data: dict) -> dict:
        """Calculate worst case scenario"""
        revenue = float(data.get("annualRevenue", 0))
        growth_rate = float(data.get("growthRate", 10))
        return {
            "revenue": revenue * 0.9,
            "growth_rate": growth_rate * 0.5,
            "margin": (float(data.get("ebitda", 0)) / revenue) * 0.8,
            "timeline": "12 months",
            "probability": "15%"
        }

    def _estimate_personnel_needs(self, action: dict) -> dict:
        """Estimate personnel requirements for action"""
        priority = action.get("priority", "Medium")
        timeline = action.get("timeline", "3-6 months")
        
        base_needs = {
            "High": {
                "project_manager": 1,
                "specialists": 2,
                "support_staff": 2
            },
            "Medium": {
                "project_manager": 1,
                "specialists": 1,
                "support_staff": 1
            },
            "Low": {
                "specialists": 1,
                "support_staff": 1
            }
        }
        
        return base_needs.get(priority, base_needs["Medium"])

    def _determine_external_needs(self, action: dict) -> list:
        """Determine external support requirements"""
        needs = []
        
        if "marketing" in action.get("action", "").lower():
            needs.append("Marketing Agency")
        if "technology" in action.get("action", "").lower():
            needs.append("IT Consultants")
        if "efficiency" in action.get("action", "").lower():
            needs.append("Process Optimization Consultants")
            
        return needs if needs else ["No external support required"]

    def _estimate_timeline(self, action: dict) -> dict:
        """Estimate detailed timeline for action implementation"""
        priority = action.get("priority", "Medium")
        timelines = {
            "High": {
                "planning": "2-4 weeks",
                "implementation": "2-3 months",
                "review": "2 weeks"
            },
            "Medium": {
                "planning": "4-6 weeks",
                "implementation": "3-4 months",
                "review": "3 weeks"
            },
            "Low": {
                "planning": "6-8 weeks",
                "implementation": "4-6 months",
                "review": "4 weeks"
            }
        }
        return timelines.get(priority, timelines["Medium"])

    def _calculate_roi_estimate(self, action: dict, data: dict) -> dict:
        """Calculate estimated ROI for action"""
        revenue = float(data.get("annualRevenue", 0))
        cost = float(self._calculate_budget(action).replace("$", "").split("-")[0].replace(",", ""))
        
        roi_estimates = {
            "High": {"min": 0.25, "max": 0.4},
            "Medium": {"min": 0.15, "max": 0.25},
            "Low": {"min": 0.05, "max": 0.15}
        }
        
        priority = action.get("priority", "Medium")
        roi_range = roi_estimates.get(priority, roi_estimates["Medium"])
        
        return {
            "estimated_return": round(cost * (1 + roi_range["max"]), 2),
            "roi_percentage": f"{int(roi_range['min']*100)}-{int(roi_range['max']*100)}%",
            "payback_period": "6-12 months" if priority == "High" else "12-18 months"
        }

    def _validate_action(self, action: dict) -> bool:
        """Validate action data structure"""
        required_fields = ["action", "priority", "timeline"]
        return all(field in action for field in required_fields)

    def _get_fallback_resources(self) -> dict:
        """Provide fallback resource estimation"""
        return {
            "budget": "$25,000-50,000",
            "personnel": {"specialists": 1, "support_staff": 1},
            "timeline": "3-6 months",
            "external_support": ["No external support required"]
        }

    def generate_strategic_plan(self, metrics: Dict) -> Dict:
        """Generate a strategic plan based on business metrics"""
        logging.info("Generating strategic plan")
        plan = {
            "growth_strategy": self._determine_growth_strategy(metrics),
            "operational_improvements": self._identify_operational_improvements(metrics),
            "market_expansion": self._assess_market_expansion_opportunities(metrics),
            "risk_mitigation": self._develop_risk_mitigation_plan(metrics)
        }
        return plan

    def _determine_growth_strategy(self, metrics: Dict) -> List[str]:
        """Determine growth strategies"""
        strategies = []
        if metrics["growth_rate"] < 10:
            strategies.append("Invest in marketing and sales to boost growth")
        if metrics["recurring_revenue_pct"] < 50:
            strategies.append("Develop subscription-based services to increase recurring revenue")
        return strategies

    def _identify_operational_improvements(self, metrics: Dict) -> List[str]:
        """Identify operational improvements"""
        improvements = []
        if metrics["ebitda_margin"] < 15:
            improvements.append("Optimize cost structures to improve margins")
        return improvements

    def _assess_market_expansion_opportunities(self, metrics: Dict) -> List[str]:
        """Assess market expansion opportunities"""
        opportunities = []
        if metrics["geographic_reach"] < 5:
            opportunities.append("Expand into new geographic markets to increase reach")
        return opportunities

    def _develop_risk_mitigation_plan(self, metrics: Dict) -> List[str]:
        """Develop a risk mitigation plan"""
        risks = []
        if metrics["retention_rate"] < 80:
            risks.append("Implement customer loyalty programs to improve retention")
        return risks