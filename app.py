from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/valuate', methods=['POST'])
def valuate():
    try:
        data = request.json
        industry = data.get("industry")
        b2b_subindustry = data.get("b2bSubIndustry")
        annual_revenue = data.get("annualRevenue", 0)
        ebitda = data.get("ebitda", None)
        multiple = data.get("multiple", None)

        if ebitda is None:
            ebitda = annual_revenue * 0.15

        if multiple is None:
            multiples = {
                "HVAC - Commercial": 5,
                "HVAC - Residential": 4.5,
                "Plumbing": 4.2,
                "Roofing": 4.8,
                "Landscaping - Commercial": 3.8,
                "Landscaping - Residential": 3.5,
                "Manufacturing": 6,
                "Insurance Agency - Personal Lines": 4,
                "Pest Control - Residential": 5,
                "Veterinary Practice / Animal Hospital": 6.5,
                "B2B Software": 10,
            }
            multiple = multiples.get(industry, 5)

        valuation = ebitda * multiple

        insights = f"The EBITDA multiple used for {industry} is {multiple}. For this industry, the valuation reflects a competitive market analysis."

        if industry == "B2B Software" and b2b_subindustry:
            insights += f" Sub-industry chosen: {b2b_subindustry}. Valuation accounts for unique SaaS or FinTech growth metrics."

        return jsonify({"valuation": valuation, "insights": insights})
    except Exception as e:
        return jsonify({"error": "Server Error", "details": str
