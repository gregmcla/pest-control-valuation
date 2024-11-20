from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import traceback

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for testing
logging.basicConfig(level=logging.DEBUG)

INDUSTRY_BENCHMARKS = {
    "growth_rate": {"good": 15, "excellent": 25},
    "retention": {"good": 80, "excellent": 90},
    "margin": {"good": 15, "excellent": 25}
}

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "The valuation API is running."})

@app.route("/api/valuate", methods=["POST"])
def valuate():
    logging.info("Received valuation request")
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        logging.info(f"Request data: {data}")
        
        # Validate required fields
        if not data:
            return jsonify({"error": "Empty request"}), 400
        
        if "industry" not in data:
            return jsonify({"error": "Industry is required"}), 400
        
        if "annualRevenue" not in data:
            return jsonify({"error": "Annual revenue is required"}), 400

        # Extract data with safe defaults
        annual_revenue = float(data["annualRevenue"])
        ebitda = float(data.get("ebitda", annual_revenue * 0.15))
        
        if annual_revenue <= 0:
            return jsonify({"error": "Annual revenue must be positive"}), 400

        # Industry-specific base multiples (updated based on research)
        industry_multiples = {
            # Software and Technology Services
            "SaaS": 8.5,
            "IT Consulting": 7.0,
            "Custom Software": 6.5,
            
            # Healthcare Services
            "Medical Practice": 6.0,
            "Home Healthcare": 5.5,
            "Diagnostic Center": 6.2,
            
            # Manufacturing
            "Industrial Manufacturing": 5.8,
            "Specialty Manufacturing": 6.0,
            "Food Manufacturing": 5.5,
            
            # Financial Services
            "Insurance Agency": 6.5,
            "Financial Advisory": 7.0,
            "Accounting Services": 6.0,
            
            # Trades and Home Services
            "Plumbing": 4.5,
            "Electrical": 4.7,
            "HVAC": 4.8,
            "Roofing": 4.3,
            "Pest Control": 5.5,
            "Landscaping": 4.4,
            
            # Professional Services
            "Legal": 6.5,
            "Engineering": 6.0,
            "Architectural": 5.8,
            
            # Consumer Products and Retail
            "Health and Beauty": 5.8,
            "E-Commerce": 6.0,
            "Brick and Mortar": 4.5,
            
            # Transportation and Logistics
            "Freight and Shipping": 5.0,
            "Warehousing": 4.8,
            "3PL": 5.2,
            
            # Marketing and Media
            "Digital Marketing": 6.2,
            "Creative Agency": 5.8,
            "Content Production": 5.5,
            
            # Real Estate Services
            "Property Management": 5.5,
            "Real Estate Brokerage": 6.0,
            "Real Estate Development": 6.5,
            
            # Education and Training
            "Private Education": 5.8,
            "Corporate Training": 5.5,
            "E-Learning": 6.5,
            
            # Energy and Environmental
            "Renewable Energy": 6.8,
            "Environmental Consulting": 5.8,
            "Energy Efficiency": 6.0,
            
            # Additional Services
            "Moving and Storage": 4.5,
            "Home Inspection": 4.8,
            "Security Services": 5.2
        }

        base_multiple = industry_multiples.get(data["industry"], 5.0)
        adjusted_multiple = base_multiple

        # Core metrics extraction
        growth_rate = float(data.get("growthRate", 0))
        customer_retention = float(data.get("customerRetention", 0))
        geographic_reach = float(data.get("geographicReach", 0))
        recurring_revenue = float(data.get("recurringRevenue", 0))
        ebitda_margin = (ebitda / annual_revenue * 100) if annual_revenue > 0 else 0
        recurring_revenue_percentage = (recurring_revenue / annual_revenue * 100) if annual_revenue > 0 else 0

        # Multiple adjustments based on research-backed metrics
        multiple_adjustments = {
            "growth_premium": calculate_growth_premium(growth_rate),
            "margin_premium": calculate_margin_premium(ebitda_margin),
            "retention_premium": calculate_retention_premium(customer_retention),
            "recurring_revenue_premium": calculate_recurring_revenue_premium(recurring_revenue_percentage),
            "geographic_premium": calculate_geographic_premium(geographic_reach),
            "size_premium": calculate_size_premium(annual_revenue)
        }

        # Apply adjustments
        for premium in multiple_adjustments.values():
            adjusted_multiple += premium

        valuation = ebitda * adjusted_multiple

        # Generate detailed metrics analysis
        metrics_analysis = analyze_metrics(data, multiple_adjustments)
        
        industry_avg_multiple = industry_multiples.get(data["industry"], 5.0)
        percentile = "Top 25%" if adjusted_multiple > industry_avg_multiple else "Bottom 75%"
        
        insights = generate_detailed_insights(data, INDUSTRY_BENCHMARKS)
        
        response_data = {
            "valuation": round(valuation, 2),
            "currentMultiple": round(adjusted_multiple, 2),
            "metrics": metrics_analysis,
            "adjustments": multiple_adjustments,
            "scenarios": generate_enhanced_scenarios(valuation, adjusted_multiple, metrics_analysis),
            "industryComparison": {
                "industryAvgMultiple": industry_avg_multiple,
                "percentileBenchmark": percentile
            },
            "insights": insights  # Add insights to the response
        }

        logging.info(f"Sending response: {response_data}")
        return jsonify(response_data)

    except ValueError as ve:
        logging.error(f"Value Error: {str(ve)}\n{traceback.format_exc()}")
        return jsonify({"error": f"Invalid number format: {str(ve)}"}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Internal server error"}), 500

def generate_detailed_insights(data, benchmarks):
    insights = []
    # Add detailed industry-specific insights
    growth_rate = float(data.get("growthRate", 0))
    if growth_rate < benchmarks["growth_rate"]["good"]:
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
    # Add more insight categories...
    return insights

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

def calculate_growth_premium(growth_rate):
    """Premium based on YoY revenue growth"""
    if growth_rate > 25: return 1.2
    if growth_rate > 15: return 0.8
    if growth_rate > 10: return 0.5
    if growth_rate < 0: return -0.5
    return 0

def calculate_margin_premium(ebitda_margin):
    """Premium based on EBITDA margin"""
    if ebitda_margin > 25: return 1.0
    if ebitda_margin > 20: return 0.7
    if ebitda_margin > 15: return 0.4
    if ebitda_margin < 10: return -0.3
    return 0

def calculate_retention_premium(retention):
    """Premium based on customer retention rate"""
    if retention > 90: return 0.8
    if retention > 80: return 0.5
    if retention > 70: return 0.2
    if retention < 60: return -0.4
    return 0

def calculate_recurring_revenue_premium(recurring_percentage):
    """Premium based on recurring revenue percentage"""
    if recurring_percentage > 80: return 1.0
    if recurring_percentage > 60: return 0.7
    if recurring_percentage > 40: return 0.4
    return 0

def calculate_geographic_premium(reach):
    """Premium based on geographic diversification"""
    if reach > 10: return 0.8
    if reach > 5: return 0.5
    if reach > 3: return 0.3
    return 0

def calculate_size_premium(revenue):
    """Premium based on company size"""
    if revenue > 10000000: return 0.8  # >$10M
    if revenue > 5000000: return 0.5   # >$5M
    if revenue > 1000000: return 0.2   # >$1M
    return 0

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

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
