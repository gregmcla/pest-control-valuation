import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import traceback
import sys
from decimal import Decimal, InvalidOperation
from typing import Dict, List, Union
from datetime import datetime
from ai_analysis import ValuationAI
from competitive_analysis import CompetitiveAnalysis
from strategy_engine import StrategyEngine
from dotenv import load_dotenv
import gc

load_dotenv()  # Load environment variables

# Initialize Flask app and configure logging first
app = Flask(__name__)

# Get port from environment variable (Render sets this automatically)
port = int(os.environ.get("PORT", 5000))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Update CORS configuration to use allowed origins from environment
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'https://pest-control-valuation-1.onrender.com').split(',')

# Update CORS configuration to be more permissive
CORS(app, 
     resources={r"/*": {
         "origins": "*",  # Allow all origins in development
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"],
         "max_age": 600,
         "supports_credentials": True
     }})

# Configure rate limiter
RATE_LIMIT = os.getenv('API_RATE_LIMIT', '50/hour')
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[RATE_LIMIT],
    storage_uri="memory://"  # Use in-memory storage for simplicity
)

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
    "SaaS": Decimal("8.5"),
    "IT Consulting": Decimal("7.0"),
    "Custom Software": Decimal("6.5"),
    "Medical Practice": Decimal("6.0"),
    "Home Healthcare": Decimal("5.5"),
    "Diagnostic Center": Decimal("6.2"),
    "Industrial Manufacturing": Decimal("5.8"),
    "Specialty Manufacturing": Decimal("6.0"),
    "Food Manufacturing": Decimal("5.5"),
    "Plumbing": Decimal("4.5"),
    "Electrical": Decimal("4.7"),
    "HVAC": Decimal("4.8"),
    "Roofing": Decimal("4.3"),
    "Pest Control": Decimal("5.5"),
    "Landscaping": Decimal("4.4")
}

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class ApiError(Exception):
    """Base exception for API errors"""
    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        self.status_code = status_code

def validate_numeric_field(value: Union[str, float, int, Decimal], field_name: str, 
                         min_value: float = None, max_value: float = None) -> Decimal:
    """Validate numeric fields with proper error messages"""
    try:
        value = Decimal(str(value))
        if min_value is not None and value < Decimal(str(min_value)):
            raise ApiError(f"{field_name} must be at least {min_value}")
        if max_value is not None and value > Decimal(str(max_value)):
            raise ApiError(f"{field_name} must not exceed {max_value}")
        return value
    except (ValueError, InvalidOperation):
        raise ApiError(f"Invalid {field_name} value")

def validate_input(data: Dict) -> None:
    """Enhanced input validation"""
    if not isinstance(data, dict):
        raise ApiError("Invalid request format")

    required_fields = {
        "industry": "Industry selection",
        "annualRevenue": "Annual revenue"
    }
    
    for field, name in required_fields.items():
        if field not in data:
            raise ApiError(f"{name} is required")
    
    # Validate industry
    if data["industry"] not in INDUSTRY_MULTIPLES:
        raise ApiError("Invalid industry selection")
    
    # Validate numeric fields
    validate_numeric_field(data["annualRevenue"], "Annual revenue", min_value=0)
    if "ebitda" in data:
        validate_numeric_field(data["ebitda"], "EBITDA", min_value=0)
    if "growthRate" in data:
        validate_numeric_field(data["growthRate"], "Growth rate", min_value=-100, max_value=1000)
    if "customerRetention" in data:
        validate_numeric_field(data["customerRetention"], "Customer retention", min_value=0, max_value=100)
    if "geographicReach" in data:
        validate_numeric_field(data["geographicReach"], "Geographic reach", min_value=0)

def calculate_metrics(data: Dict) -> Dict:
    """Calculate all business metrics with error handling"""
    try:
        revenue = Decimal(str(data["annualRevenue"]))
        ebitda = Decimal(str(data.get("ebitda", revenue * Decimal("0.15"))))
        retention = Decimal(str(data.get("customerRetention", 0)))
        industry = data.get("industry")
        
        if industry not in INDUSTRY_MULTIPLES:
            logging.warning(f"Unknown industry: {industry}, using default multiple")
        
        return {
            "revenue": revenue,
            "ebitda": ebitda,
            "ebitda_margin": (ebitda / revenue * 100) if revenue else Decimal("0"),
            "retention_rate": retention,
            "growth_rate": Decimal(str(data.get("growthRate", 0))),
            "geographic_reach": Decimal(str(data.get("geographicReach", 0))),
            "recurring_revenue_pct": calculate_recurring_revenue_percentage(data),
            "industry": industry
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

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })

# Add CORS error handler
@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all exceptions and ensure CORS headers are set"""
    response = jsonify({
        "error": str(e),
        "type": "server_error"
    })
    response.status_code = 500
    return response

def initialize_components():
    """Initialize components with memory management"""
    try:
        MODEL_CACHE_DIR = os.getenv('MODEL_CACHE_DIR', '/tmp/models')
        os.makedirs(MODEL_CACHE_DIR, exist_ok=True)
        
        # Initialize with error handling
        try:
            ai = ValuationAI(model_cache_dir=MODEL_CACHE_DIR)
        except Exception as e:
            logging.error(f"Error initializing ValuationAI: {e}")
            ai = None

        gc.collect()
        comp = CompetitiveAnalysis()
        gc.collect()
        strat = StrategyEngine()
        gc.collect()
        
        if ai is None:
            raise RuntimeError("Failed to initialize ValuationAI")
        
        return ai, comp, strat
    except Exception as e:
        logging.error(f"Error initializing components: {e}")
        raise RuntimeError("Failed to initialize required components")

try:
    ai_analyzer, competitive_analyzer, strategy_engine = initialize_components()
except Exception as e:
    logging.error(f"Critical initialization error: {e}")
    sys.exit(1)

# Update the valuate endpoint to include CORS headers
@app.route("/api/valuate", methods=["POST", "OPTIONS"])
@limiter.limit("50 per hour")
def valuate():
    """Main valuation endpoint with enhanced error handling and debugging"""
    logging.info("Received valuation request")
    
    # Handle preflight requests
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        return response

    try:
        if not request.is_json:
            raise ApiError("Request must be JSON")

        data = request.get_json()
        logging.info(f"Request data: {data}")

        # Add data validation logging
        validate_input(data)
        logging.info("Input validation passed")

        # Process in chunks to manage memory
        metrics = calculate_metrics(data)
        gc.collect()
        
        market_trends = ai_analyzer.analyze_market_trends(data["industry"])
        gc.collect()
        
        competitive_position = competitive_analyzer.analyze_market_position(metrics, market_trends)
        gc.collect()
        
        strategy = strategy_engine.generate_recommendations(data, competitive_position)
        gc.collect()
        
        adjustments = calculate_adjustments(metrics)
        logging.info(f"Calculated adjustments: {adjustments}")

        valuation = calculate_valuation(metrics, adjustments)
        logging.info(f"Final valuation: {valuation}")
        
        response_data = {
            "valuation": float(valuation),
            "currentMultiple": float(sum(adjustments.values())),
            "metrics": {k: float(v) if isinstance(v, Decimal) else v for k, v in metrics.items()},
            "adjustments": {k: float(v) for k, v in adjustments.items()},
            "scenarios": generate_enhanced_scenarios(valuation, sum(adjustments.values()), metrics),
            "industryComparison": generate_industry_comparison(data["industry"], metrics),  # Fixed this line
            "marketAnalysis": market_trends,
            "competitivePosition": competitive_position,
            "strategicPlan": strategy
        }
        
        return jsonify(response_data)

    except ApiError as e:
        logging.error(f"API error: {str(e)}")
        return jsonify({"error": e.message, "type": "api_error"}), e.status_code
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e), "type": "server_error"}), 500

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
    try:
        base_multiple = INDUSTRY_MULTIPLES.get(metrics["industry"], Decimal("5.0"))
        adjusted_multiple = base_multiple + sum(adjustments.values())
        valuation = metrics["ebitda"] * adjusted_multiple
        return valuation.quantize(Decimal("0.01"))
    except Exception as e:
        logging.error(f"Valuation calculation error: {str(e)}")
        raise ValueError("Error calculating valuation")

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
    valuation = Decimal(str(valuation))
    current_multiple = Decimal(str(current_multiple))
    return [
        {
            "name": "Current",
            "valuation": float(valuation),  # Convert to float for JSON
            "multiple": float(current_multiple),
            "description": "Based on current performance"
        },
        {
            "name": "Optimized",
            "valuation": float(valuation * Decimal("1.3")),
            "multiple": float(current_multiple + Decimal("1.0")),
            "description": "With improved metrics"
        },
        {
            "name": "Best Case",
            "valuation": float(valuation * Decimal("1.5")),
            "multiple": float(current_multiple + Decimal("1.5")),
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

def generate_industry_comparison(industry: str, metrics: Dict) -> Dict:
    try:
        return {
            "industryAvgMultiple": float(INDUSTRY_MULTIPLES.get(industry, 5.0)),
            "peerComparison": {
                "growth": compare_to_peers(metrics["growth_rate"], "growth_rate"),
                "margin": compare_to_peers(metrics["ebitda_margin"], "margin"),
                "retention": compare_to_peers(metrics["retention_rate"], "retention")
            },
            "recommendations": generate_market_recommendations(metrics)
        }
    except Exception as e:
        logging.error(f"Error generating industry comparison: {e}")
        return {
            "industryAvgMultiple": 5.0,
            "peerComparison": {"growth": "Average", "margin": "Average", "retention": "Average"},
            "recommendations": []
        }

@app.errorhandler(ApiError)
def handle_api_error(error):
    """Global error handler for API errors"""
    response = jsonify({
        "error": error.message,
        "type": "api_error"
    })
    response.status_code = error.status_code
    return response

@app.errorhandler(500)
def handle_server_error(error):
    """Global error handler for server errors"""
    response = jsonify({
        "error": "Internal server error occurred",
        "type": "server_error"
    })
    response.status_code = 500
    return response

@app.after_request
def after_request(response):
    """Enhanced security headers"""
    # Existing headers
    response.headers.update({
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self' https:; script-src 'self' 'unsafe-inline' https:; style-src 'self' 'unsafe-inline' https:; img-src 'self' data: https:;",
        'Permissions-Policy': 'geolocation=(), microphone=()',
        'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
        'Pragma': 'no-cache'
    })
    return response

if __name__ == "__main__":
    # Production settings
    app.config['JSON_SORT_KEYS'] = False  # Better performance
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,  # Ensure debug is False in production
        threaded=True
    )
