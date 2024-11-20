class StrategyEngine:
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