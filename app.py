from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/valuate", methods=["POST"])
def valuate():
    try:
        # Parse JSON request data
        data = request.json
        industry = data.get("industry")
        annual_revenue = float(data.get("annualRevenue", 0))
        ebitda = float(data.get("ebitda", 0))
        multiple = data.get("multiple", None)
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

        # Use default multiple if not provided
        if not multiple:
            multiple = industry_multiples.get(industry, 5)

        # Adjust multiples based on optional fields
        adjustment = 0
        if growth_rate > 10:
            adjustment += (growth_rate - 10) * 0.1  # Growth rate adjustment
        if customer_retention > 80:
            adjustment += (customer_retention - 80) * 0.05  # Customer retention adjustment
        if geographic_reach > 0:
            adjustment += geographic_reach * 0.02  # Geographic reach adjustment

        current_multiple = multiple + adjustment

        # Calculate valuation
        valuation = ebitda * current_multiple if ebitda else annual_revenue * 0.15 * current_multiple

        # Improved scenarios for guidance
        improved_multiple_1 = current_multiple + 1  # Example improvement for scenario 1
        improved_multiple_2 = current_multiple + 2  # Example improvement for scenario 2

        improved_valuation_1 = ebitda * improved_multiple_1 if ebitda else annual_revenue * 0.15 * improved_multiple_1
        improved_valuation_2 = ebitda * improved_multiple_2 if ebitda else annual_revenue * 0.15 * improved_multiple_2

        # Generate insights
        insights = [
            f"Your current EBITDA multiple is {current_multiple:.2f}x.",
            f"Increasing your growth rate, customer retention, or geographic reach can improve your multiple.",
        ]

        # Guidance for improvement
        guidance = [
            {
                "scenario": "Improved Scenario 1",
                "valuation": round(improved_valuation_1, 2),
                "multiple": round(improved_multiple_1, 2),
                "description": "Increase growth rate by 10% and customer retention by 15% to achieve this multiple."
            },
            {
                "scenario": "Improved Scenario 2",
                "valuation": round(improved_valuation_2, 2),
                "multiple": round(improved_multiple_2, 2),
                "description": "Expand geographic reach by 5 states and improve customer retention by 20% to achieve this multiple."
            }
        ]

        # Return valuation, insights, and guidance
        return jsonify({
            "valuation": round(valuation, 2),
            "currentMultiple": round(current_multiple, 2),
            "insights": "<br>".join(insights),
            "guidance": guidance
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 400


# Run the Flask app
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
