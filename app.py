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
        b2b_subindustry = data.get("b2bSubIndustry", None)
        annual_revenue = float(data.get("annualRevenue", 0))
        ebitda = float(data.get("ebitda", 0))
        recurring_revenue = float(data.get("recurringRevenue", 0))
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
        if recurring_revenue:
            adjustment += (recurring_revenue / annual_revenue) * 2  # Bonus for recurring revenue

        adjusted_multiple = multiple + adjustment

        # Calculate valuation
        valuation = ebitda * adjusted_multiple if ebitda else annual_revenue * 0.15 * adjusted_multiple

        # Generate insights
        insights = []

        # General growth rate insights
        if growth_rate:
            if growth_rate > 15:
                insights.append(f"Your high growth rate of {growth_rate}% is driving an increased valuation multiple.")
            elif growth_rate < 5:
                insights.append(f"A low growth rate of {growth_rate}% might reduce your valuation multiple.")

        # Customer retention insights
        if customer_retention:
            if customer_retention > 90:
                insights.append(f"Excellent customer retention ({customer_retention}%) boosts your valuation.")
            elif customer_retention < 70:
                insights.append(f"Customer retention at {customer_retention}% is below industry standards.")

        # Geographic reach insights
        if geographic_reach:
            if geographic_reach > 10:
                insights.append(f"Operating in {geographic_reach} states significantly enhances your valuation.")
            else:
                insights.append(f"Geographic reach in {geographic_reach} states provides moderate impact on valuation.")

        # Recurring revenue insights
        if recurring_revenue:
            recurring_percentage = (recurring_revenue / annual_revenue) * 100 if annual_revenue else 0
            insights.append(f"Recurring revenue contributes {recurring_percentage:.2f}% to your overall revenue, boosting valuation.")

        # B2B Software-specific insights
        if industry == "B2B Software":
            insights.append("B2B software businesses often see high multiples due to scalability and recurring revenue.")
            if b2b_subindustry:
                # Sub-Industry specific insights
                if b2b_subindustry == "SaaS":
                    insights.append("SaaS businesses are valued highly for their recurring subscription revenue models.")
                elif b2b_subindustry == "FinTech":
                    insights.append("FinTech businesses attract strong valuations due to their disruptive potential in finance.")
                elif b2b_subindustry == "MarTech":
                    insights.append("MarTech businesses benefit from high demand for data-driven marketing solutions.")
                elif b2b_subindustry == "HealthTech":
                    insights.append("HealthTech businesses command high valuations due to their impact on healthcare innovation.")

        # Improved scenarios for guidance
        improved_scenario_1 = valuation * 1.2  # Example: Increase by 20%
        improved_scenario_2 = valuation * 1.5  # Example: Increase by 50%

        # Guidance for improvement
        guidance = [
            {
                "scenario": "Improved Scenario 1",
                "valuation": round(improved_scenario_1, 2),
                "description": "Focus on increasing growth rate and customer retention to achieve a 20% higher valuation."
            },
            {
                "scenario": "Improved Scenario 2",
                "valuation": round(improved_scenario_2, 2),
                "description": "Expand geographic reach and emphasize recurring revenue to achieve a 50% higher valuation."
            }
        ]

        # Return valuation, insights, and guidance
        return jsonify({
            "valuation": round(valuation, 2),
            "insights": "<br>".join(insights) if insights else "No additional insights available.",
            "guidance": guidance
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 400

# Run the Flask app
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
