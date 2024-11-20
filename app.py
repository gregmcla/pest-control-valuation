from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "The valuation API is running."})

@app.route("/api/valuate", methods=["POST"])  # Fixed route
def valuate():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type"}), 400

        data = request.get_json()
        
        # Required fields validation
        if not data.get("industry"):
            return jsonify({"error": "Industry is required"}), 400
        if not data.get("annualRevenue"):
            return jsonify({"error": "Annual revenue is required"}), 400

        # Extract and convert data with safe defaults
        industry = data["industry"]
        annual_revenue = float(data["annualRevenue"])
        ebitda = float(data.get("ebitda", annual_revenue * 0.15))
        recurring_revenue = float(data.get("recurringRevenue", 0))
        growth_rate = float(data.get("growthRate", 0))
        customer_retention = float(data.get("customerRetention", 0))
        geographic_reach = float(data.get("geographicReach", 0))

        # Default industry multiples
        industry_multiples = {
            "HVAC - Commercial": 5,
            "HVAC - Residential": 4.5,
            "Plumbing": 4,
            "Roofing": 3.5,
            "Landscaping - Commercial": 3,
            "Landscaping - Residential": 2.8,
            "Manufacturing": 6,
            "Insurance Agency - Personal Lines": 7,
            "Pest Control - Residential": 6.5,
            "Veterinary Practice / Animal Hospital": 8,
            "B2B Software": 10,
        }

        # Calculate the multiple and valuation
        base_multiple = industry_multiples.get(industry, 5)
        adjustments = sum([
            0.1 * max(0, growth_rate - 10),
            0.05 * max(0, customer_retention - 80),
            0.02 * geographic_reach,
            2 * (recurring_revenue / annual_revenue if annual_revenue > 0 else 0)
        ])

        current_multiple = base_multiple + adjustments
        valuation = ebitda * current_multiple

        # Calculate improved scenarios
        improved_multiple_1 = current_multiple + 1
        improved_multiple_2 = current_multiple + 2
        
        response_data = {
            "valuation": round(valuation, 2),
            "currentMultiple": round(current_multiple, 2),
            "insights": f"Current multiple: {current_multiple:.1f}x<br>Industry baseline: {base_multiple:.1f}x<br>Total adjustments: +{adjustments:.1f}x",
            "guidance": [
                {
                    "valuation": round(ebitda * improved_multiple_1, 2),
                    "description": f"Increase growth rate and retention to achieve {improved_multiple_1:.1f}x multiple"
                },
                {
                    "valuation": round(ebitda * improved_multiple_2, 2),
                    "description": f"Expand reach and recurring revenue to achieve {improved_multiple_2:.1f}x multiple"
                }
            ]
        }
        
        return jsonify(response_data)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
