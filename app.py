import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from decimal import Decimal
from typing import Dict
from datetime import datetime
from ai_analysis import ValuationAI
from competitive_analysis import CompetitiveAnalysis
from strategy_engine import StrategyEngine
from dotenv import load_dotenv

# Initialize Flask app and load config
app = Flask(__name__)
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize CORS and rate limiter
CORS(app)
limiter = Limiter(app=app, key_func=get_remote_address)

# Initialize components
try:
    MODEL_CACHE_DIR = os.getenv('MODEL_CACHE_DIR', '/tmp/models')
    os.makedirs(MODEL_CACHE_DIR, exist_ok=True)
    ai_analyzer = ValuationAI(model_cache_dir=MODEL_CACHE_DIR)
    competitive_analyzer = CompetitiveAnalysis()
    strategy_engine = StrategyEngine()
except Exception as e:
    logger.error(f"Failed to initialize components: {e}")
    raise

@app.route("/health")
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})

@app.route("/api/valuate", methods=["POST"])
@limiter.limit("50/hour")
def valuate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request data"}), 400

        # Calculate base metrics
        metrics = calculate_metrics(data)
        
        # Get analysis results
        market_analysis = competitive_analyzer.analyze_market_position(metrics, {})
        ai_insights = ai_analyzer.analyze_market_trends(metrics["industry"])
        strategy = strategy_engine.generate_recommendations(data, market_analysis)

        # Calculate final valuation
        valuation_result = calculate_valuation_result(metrics, market_analysis, ai_insights, strategy)
        
        return jsonify(valuation_result)

    except Exception as e:
        logger.error(f"Valuation error: {e}")
        return jsonify({"error": str(e)}), 500

# ... rest of the calculation functions with proper error handling ...

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
