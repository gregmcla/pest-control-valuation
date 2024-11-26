from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

INDUSTRY_MULTIPLES = {
    "SaaS": 8.5,
    "Pest Control": 5.5,
    "HVAC": 4.8,
    "Plumbing": 4.5,
    "Electrical": 4.7,
    "Manufacturing": 5.8
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/valuate", methods=["POST"])
def valuate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing data"}), 400

        revenue = float(data.get('annualRevenue', 0))
        ebitda = float(data.get('ebitda', revenue * 0.15))
        industry = data.get('industry', '')
        
        multiple = INDUSTRY_MULTIPLES.get(industry, 5.0)
        valuation = ebitda * multiple

        return jsonify({
            "valuation": valuation,
            "multiple": multiple,
            "metrics": {
                "revenue": revenue,
                "ebitda": ebitda,
                "ebitda_margin": (ebitda / revenue * 100) if revenue else 0
            }
        })

    except Exception as e:
        print(f"Error: {e}")  # Debug print
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    print("Server starting on http://localhost:5000")
    app.run(debug=True, port=5000)
