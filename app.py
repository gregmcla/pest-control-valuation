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

        # Calculate valuation
        base_multiple = 5.0
        growth_rate = float(data.get("growthRate", 0))
        customer_retention = float(data.get("customerRetention", 0))
        geographic_reach = float(data.get("geographicReach", 0))
        
        # Adjust multiple based on factors
        adjusted_multiple = base_multiple
        if growth_rate > 10:
            adjusted_multiple += 0.5
        if customer_retention > 80:
            adjusted_multiple += 0.5
        if geographic_reach > 3:
            adjusted_multiple += 0.3
            
        valuation = ebitda * adjusted_multiple
        
        # Generate insights
        insights = []
        if growth_rate < 10:
            insights.append("Consider implementing growth strategies to increase valuation")
        if customer_retention < 80:
            insights.append("Improving customer retention could increase valuation")
        if geographic_reach < 3:
            insights.append("Geographic expansion could add value")
            
        response_data = {
            "valuation": round(valuation, 2),
            "currentMultiple": adjusted_multiple,
            "insights": insights,
            "guidance": [
                {
                    "valuation": round(valuation * 1.2, 2),
                    "description": "With improved customer retention and growth",
                    "actions": ["Implement customer success program", "Develop growth strategy"]
                },
                {
                    "valuation": round(valuation * 1.4, 2),
                    "description": "Best case scenario with geographic expansion",
                    "actions": ["Expand to new markets", "Increase service offerings"]
                }
            ]
        }
        
        logging.info(f"Sending response: {response_data}")
        return jsonify(response_data)

    except ValueError as ve:
        logging.error(f"Value Error: {str(ve)}\n{traceback.format_exc()}")
        return jsonify({"error": f"Invalid number format: {str(ve)}"}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
