from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import traceback

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for testing
logging.basicConfig(level=logging.DEBUG)

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
            "B2B Software": 7.0,
            "Pest Control - Residential": 5.5,
            "HVAC - Commercial": 5.2,
            "HVAC - Residential": 4.8,
            "Plumbing": 4.5,
            "Roofing": 4.3,
            "Manufacturing": 5.8
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
        
        response_data = {
            "valuation": round(valuation, 2),
            "currentMultiple": round(adjusted_multiple, 2),
            "metrics": metrics_analysis,
            "adjustments": multiple_adjustments,
            "scenarios": generate_enhanced_scenarios(valuation, adjusted_multiple, metrics_analysis)
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

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
