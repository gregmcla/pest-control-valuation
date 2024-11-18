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
        growth_rate = data.get("growthRate", None)
        customer_retention = data.get("customerRetention", None)
        geographic_reach = data.get("geographicReach", None)

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
        if growth_rate:
            adjustment += (growth_rate - 10) * 0.1  # Growth rate adjustment
        if customer_retention:
            adjustment += (customer_retention - 80) * 0.05  # Customer retention adjustment
        if geographic_reach:
            adjustment += geographic_reach * 0.02  # Geographic reach adjustment

        adjusted_multiple = multiple + adjustment

        # Calculate valuation
        valuation = ebitda * adjusted_multiple if ebitda else annual_revenue * 0.15 * adjusted_multiple

        # Generate insights
        insights = []
        if growth_rate:
            if growth_rate > 15:
                insights.append(f"Your high growth rate of {growth_rate}% is driving an increased valuation multiple.")
            elif growth_rate < 5:
                insights.append(f"A low growth rate of {growth_rate}% might reduce your valuation multiple.")
        if customer_retention:
            if customer_retention > 90:
                insights.append(f"Excellent customer retention ({customer_retention}%) boosts your valuation.")
            elif customer_retention < 70:
                insights.append(f"Customer retention at {customer_retention}% is below industry standards.")
        if geographic_reach:
            if geographic_reach > 10:
                insights.append(f"Operating in {geographic_reach} states significantly enhances your valuation.")
            else:
                insights.append(f"Geographic reach in {geographic_reach} states provides moderate impact on valuation.")
        if industry == "B2B Software":
            insights.append("B2B software businesses often see high multiples due to scalability and recurring revenue.")

        # Return valuation and insights
        return jsonify({
            "valuation": round(valuation, 2),
            "insights": "<br>".join(insights) if insights else "No additional insights available.",
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 400

# Run the Flask app
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
