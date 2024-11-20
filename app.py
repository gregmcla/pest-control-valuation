from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import traceback
from decimal import Decimal, InvalidOperation
from typing import Dict, List, Union
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for testing
logging.basicConfig(level=logging.DEBUG)

# Enhanced industry benchmarks with more detailed metrics
INDUSTRY_BENCHMARKS = {
    "growth_rate": {
        "excellent": 25,
        "good": 15,
        "average": 10,
        "below_average": 5,
        "poor": 0
    },
    "retention": {
        "excellent": 90,
        "good": 80,
        "average": 70,
        "below_average": 60,
        "poor": 50
    },
    "margin": {
        "excellent": 25,
        "good": 20,
        "average": 15,
        "below_average": 10,
        "poor": 5
    }
}

INDUSTRY_MULTIPLES = {
    # ...existing industry multiples...
}

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

def validate_input(data: Dict) -> None:
    """Validate input data with detailed error messages"""
    required_fields = {
        "industry": "Industry selection",
        "annualRevenue": "Annual revenue"
    }
    
    for field, name in required_fields.items():
        if field not in data:
            raise ValidationError(f"{name} is required")
        
    if float(data["annualRevenue"]) <= 0:
        raise ValidationError("Annual revenue must be positive")

def calculate_metrics(data: Dict) -> Dict:
    """Calculate all business metrics with error handling"""
    try:
        revenue = Decimal(str(data["annualRevenue"]))
        ebitda = Decimal(str(data.get("ebitda", revenue * Decimal("0.15"))))
        retention = Decimal(str(data.get("customerRetention", 0)))
        
        return {
            "revenue": revenue,
            "ebitda": ebitda,
            "ebitda_margin": (ebitda / revenue * 100) if revenue else Decimal("0"),
            "retention_rate": retention,
            "growth_rate": Decimal(str(data.get("growthRate", 0))),
            "geographic_reach": Decimal(str(data.get("geographicReach", 0))),
            "recurring_revenue_pct": calculate_recurring_revenue_percentage(data)
        }
    except (ValueError, InvalidOperation) as e:
        raise ValidationError(f"Invalid numeric value: {str(e)}")

def generate_detailed_insights(data: Dict, metrics: Dict) -> List[Dict]:
    """Generate comprehensive business insights"""
    insights = []
    
    growth_rate = metrics["growth_rate"]
    if growth_rate < Decimal(str(INDUSTRY_BENCHMARKS["growth_rate"]["good"])):
        insights.append({
            "category": "Growth",
            "status": "Needs Improvement",
            "impact": "High",
            "recommendations": [
                "Implement targeted marketing campaigns",
                "Expand service offerings",
                "Consider strategic acquisitions"
            ]
        })
    # ...rest of insights...
    return insights

def analyze_growth(growth_rate: Decimal) -> Dict:
    """Analyze growth rate with detailed recommendations"""
    if growth_rate < 0:
        return {
            "category": "Growth",
            "status": "Critical",
            "impact": "High",
            "score": 1,
            "recommendations": [
                "Conduct immediate market analysis",
                "Review pricing strategy",
                "Evaluate customer churn causes",
                "Consider pivot opportunities"
            ]
        }
    # ... add more growth analysis conditions ...

def analyze_market_status(metrics: Dict) -> str:
    """Analyze market position status based on metrics"""
    score = calculate_market_score(metrics)
    if score >= 8:
        return "Market Leader"
    elif score >= 6:
        return "Strong Position"
    elif score >= 4:
        return "Competitive"
    return "Needs Improvement"

def calculate_market_score(metrics: Dict) -> int:
    """Calculate market position score (0-10)"""
    score = 0
    
    # Growth contribution (0-3 points)
    if metrics["growth_rate"] > Decimal("25"): score += 3
    elif metrics["growth_rate"] > Decimal("15"): score += 2
    elif metrics["growth_rate"] > Decimal("5"): score += 1
    
    # Market reach contribution (0-3 points)
    if metrics["geographic_reach"] > Decimal("10"): score += 3
    elif metrics["geographic_reach"] > Decimal("5"): score += 2
    elif metrics["geographic_reach"] > Decimal("2"): score += 1
    
    # Profitability contribution (0-4 points)
    if metrics["ebitda_margin"] > Decimal("25"): score += 4
    elif metrics["ebitda_margin"] > Decimal("20"): score += 3
    elif metrics["ebitda_margin"] > Decimal("15"): score += 2
    elif metrics["ebitda_margin"] > Decimal("10"): score += 1
    
    return score

def generate_market_recommendations(metrics: Dict) -> List[str]:
    """Generate market position improvement recommendations"""
    recommendations = []
    
    if metrics["growth_rate"] < Decimal("15"):
        recommendations.append("Expand market presence through targeted marketing")
        recommendations.append("Consider strategic partnerships or acquisitions")
    
    if metrics["geographic_reach"] < Decimal("5"):
        recommendations.append("Evaluate expansion opportunities in adjacent markets")
        recommendations.append("Develop market entry strategies for new regions")
    
    if metrics["ebitda_margin"] < Decimal("20"):
        recommendations.append("Optimize pricing strategy and operational efficiency")
        recommendations.append("Focus on high-margin service offerings")
    
    if not recommendations:
        recommendations.append("Maintain market leadership position")
        recommendations.append("Monitor competitive landscape for emerging threats")
    
    return recommendations

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "The valuation API is running."})

# Update the main route with enhanced error handling
@app.route("/api/valuate", methods=["POST"])
def valuate():
    logging.info("Received valuation request")
    try:
        if not request.is_json:
            raise ValidationError("Request must be JSON")

        data = request.get_json()
        logging.info(f"Request data: {data}")
        
        validate_input(data)
        
        metrics = calculate_metrics(data)
        adjustments = calculate_adjustments(metrics)
        insights = generate_detailed_insights(data, metrics)
        
        response_data = {
            "valuation": calculate_valuation(metrics, adjustments),
            "metrics": metrics,
            "insights": insights,
            "adjustments": adjustments,
            "scenarios": generate_enhanced_scenarios(metrics, adjustments),
            "industryComparison": generate_industry_comparison(data, metrics)
        }
        
        logging.info(f"Sending response: {response_data}")
        return jsonify(response_data)

    except ValidationError as ve:
        return jsonify({"error": str(ve), "type": "validation_error"}), 400
    except ValueError as ve:
        logging.error(f"Value Error: {str(ve)}\n{traceback.format_exc()}")
        return jsonify({"error": f"Invalid number format: {str(ve)}"}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Internal server error", "type": "server_error"}), 500

def calculate_adjustments(metrics: Dict) -> Dict[str, Decimal]:
    """Calculate all valuation adjustments"""
    return {
        "growth_premium": Decimal(str(calculate_growth_premium(metrics["growth_rate"]))),
        "margin_premium": Decimal(str(calculate_margin_premium(metrics["ebitda_margin"]))),
        "retention_premium": Decimal(str(calculate_retention_premium(metrics["retention_rate"]))),
        "geographic_premium": Decimal(str(calculate_geographic_premium(metrics["geographic_reach"]))),
        "size_premium": Decimal(str(calculate_size_premium(metrics["revenue"])))
    }

def calculate_valuation(metrics: Dict, adjustments: Dict) -> Decimal:
    """Calculate final valuation with all adjustments"""
    base_multiple = Decimal(str(INDUSTRY_MULTIPLES.get(metrics["industry"], "5.0")))
    adjusted_multiple = base_multiple + sum(adjustments.values())
    return (metrics["ebitda"] * adjusted_multiple).quantize(Decimal("0.01"))

def analyze_market_position(data: Dict, metrics: Dict) -> Dict:
    """Analyze market position and competitive standing"""
    return {
        "category": "Market Position",
        "status": analyze_market_status(metrics),
        "impact": "High",
        "score": calculate_market_score(metrics),
        "recommendations": generate_market_recommendations(metrics)
    }

def compare_to_peers(value: Decimal, metric_type: str) -> str:
    """Compare metrics to industry benchmarks"""
    benchmarks = INDUSTRY_BENCHMARKS[metric_type]
    if value >= Decimal(str(benchmarks["excellent"])):
        return "Top 10%"
    elif value >= Decimal(str(benchmarks["good"])):
        return "Top 25%"
    elif value >= Decimal(str(benchmarks["average"])):
        return "Average"
    return "Below Average"

def generate_valuation_scenarios(base_valuation, data, current_multiple):
    return [
        {
            "name": "Current Valuation",
            "valuation": round(base_valuation, 2),
            "multiple": current_multiple,
            "description": "Based on current metrics"
        },
        {
            "name": "Growth Optimization",
            "valuation": round(base_valuation * 1.25, 2),
            "multiple": current_multiple + 0.8,
            "description": "Achieving 15%+ growth rate",
            "requirements": ["Increase marketing spend", "Enter new markets"]
        },
        {
            "name": "Operational Excellence",
            "valuation": round(base_valuation * 1.4, 2),
            "multiple": current_multiple + 1.2,
            "description": "90%+ customer retention",
            "requirements": ["Implement customer success program", "Improve service quality"]
        }
    ]

def calculate_key_metrics(data, valuation):
    annual_revenue = float(data["annualRevenue"])
    return {
        "revenueMultiple": round(valuation / annual_revenue, 2),
        "customerLifetimeValue": calculate_ltv(data),
        "operatingMargin": calculate_operating_margin(data),
        "riskProfile": assess_risk_profile(data)
    }

def calculate_growth_premium(growth_rate: Decimal) -> Decimal:
    """Premium based on YoY revenue growth"""
    if growth_rate > Decimal("25"): return Decimal("1.2")
    if growth_rate > Decimal("15"): return Decimal("0.8")
    if growth_rate > Decimal("10"): return Decimal("0.5")
    if growth_rate < Decimal("0"): return Decimal("-0.5")
    return Decimal("0")

def calculate_margin_premium(ebitda_margin: Decimal) -> Decimal:
    """Premium based on EBITDA margin"""
    if ebitda_margin > Decimal("25"): return Decimal("1.0")
    if ebitda_margin > Decimal("20"): return Decimal("0.7")
    if ebitda_margin > Decimal("15"): return Decimal("0.4")
    if ebitda_margin < Decimal("10"): return Decimal("-0.3")
    return Decimal("0")

def calculate_retention_premium(retention: Decimal) -> Decimal:
    """Premium based on customer retention rate"""
    if retention > Decimal("90"): return Decimal("0.8")
    if retention > Decimal("80"): return Decimal("0.5")
    if retention > Decimal("70"): return Decimal("0.2")
    if retention < Decimal("60"): return Decimal("-0.4")
    return Decimal("0")

def calculate_recurring_revenue_premium(recurring_percentage: Decimal) -> Decimal:
    """Premium based on recurring revenue percentage"""
    if recurring_percentage > Decimal("80"): return Decimal("1.0")
    if recurring_percentage > Decimal("60"): return Decimal("0.7")
    if recurring_percentage > Decimal("40"): return Decimal("0.4")
    return Decimal("0")

def calculate_geographic_premium(reach: Decimal) -> Decimal:
    """Premium based on geographic diversification"""
    if reach > Decimal("10"): return Decimal("0.8")
    if reach > Decimal("5"): return Decimal("0.5")
    if reach > Decimal("3"): return Decimal("0.3")
    return Decimal("0")

def calculate_size_premium(revenue: Decimal) -> Decimal:
    """Premium based on company size"""
    if revenue > Decimal("10000000"): return Decimal("0.8")  # >$10M
    if revenue > Decimal("5000000"): return Decimal("0.5")   # >$5M
    if revenue > Decimal("1000000"): return Decimal("0.2")   # >$1M
    return Decimal("0")

def analyze_metrics(data, adjustments):
    """Generate detailed metrics analysis"""
    return {
        "growth": {
            "score": adjustments["growth_premium"],
            "impact": "High",
            "benchmark": "15% industry average",
            "recommendation": generate_growth_recommendation(data)
        },
        "profitability": {
            "score": adjustments["margin_premium"],
            "impact": "High",
            "benchmark": "20% EBITDA margin target",
            "recommendation": generate_profitability_recommendation(data)
        },
        # Add more metric analyses...
    }

def generate_enhanced_scenarios(valuation, current_multiple, metrics):
    """Enhanced version of scenario generation"""
    return [
        {
            "name": "Current",
            "valuation": valuation,
            "multiple": current_multiple,
            "description": "Based on current performance"
        },
        {
            "name": "Optimized",
            "valuation": valuation * 1.3,
            "multiple": current_multiple + 1.0,
            "description": "With improved metrics"
        },
        {
            "name": "Best Case",
            "valuation": valuation * 1.5,
            "multiple": current_multiple + 1.5,
            "description": "With all metrics at industry best"
        }
    ]

def calculate_ltv(data):
    """Calculate customer lifetime value"""
    avg_revenue = float(data.get("annualRevenue", 0)) / max(float(data.get("customerCount", 100)), 1)
    retention_rate = float(data.get("customerRetention", 70)) / 100
    margin = float(data.get("ebitda", 0)) / float(data.get("annualRevenue", 1))
    return (avg_revenue * margin) / (1 - retention_rate) if retention_rate < 1 else avg_revenue * margin

def calculate_operating_margin(data):
    """Calculate operating margin"""
    revenue = float(data.get("annualRevenue", 0))
    ebitda = float(data.get("ebitda", 0))
    return (ebitda / revenue * 100) if revenue > 0 else 0

def assess_risk_profile(data):
    """Assess company risk profile"""
    score = 0
    if float(data.get("customerRetention", 0)) > 80: score += 1
    if float(data.get("recurringRevenue", 0)) > float(data.get("annualRevenue", 1)) * 0.4: score += 1
    if float(data.get("geographicReach", 0)) > 3: score += 1
    return "Low" if score >= 2 else "Medium" if score == 1 else "High"

def generate_growth_recommendation(data):
    """Generate growth-related recommendations"""
    growth_rate = float(data.get("growthRate", 0))
    if growth_rate < 10:
        return "Focus on market expansion and new customer acquisition"
    elif growth_rate < 20:
        return "Optimize current growth channels and explore new markets"
    return "Maintain current growth strategies and focus on scalability"

def generate_profitability_recommendation(data):
    """Generate profitability-related recommendations"""
    margin = float(data.get("ebitda", 0)) / float(data.get("annualRevenue", 1)) * 100
    if margin < 15:
        return "Focus on operational efficiency and pricing optimization"
    elif margin < 25:
        return "Fine-tune operations and explore premium service offerings"
    return "Maintain current profitability while ensuring quality standards"

def calculate_recurring_revenue_percentage(data: Dict) -> Decimal:
    """Calculate recurring revenue percentage with validation"""
    revenue = Decimal(str(data["annualRevenue"]))
    recurring = Decimal(str(data.get("recurringRevenue", 0)))
    
    if revenue <= 0:
        return Decimal("0")
    
    return (recurring / revenue * 100).quantize(Decimal("0.01"))

def generate_industry_comparison(data: Dict, metrics: Dict) -> Dict:
    """Generate detailed industry comparison"""
    industry = data["industry"]
    return {
        "industryAvgMultiple": INDUSTRY_MULTIPLES.get(industry, 5.0),
        "peerComparison": {
            "growth": compare_to_peers(metrics["growth_rate"], "growth_rate"),
            "margin": compare_to_peers(metrics["ebitda_margin"], "margin"),
            "retention": compare_to_peers(metrics["retention_rate"], "retention")
        }
    }

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
