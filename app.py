from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        print(f"Template error: {e}")  # Debug print
        return "Error loading template", 500

@app.route("/api/valuate", methods=["POST"])
def valuate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        revenue = float(data.get('annualRevenue', 0))
        ebitda = float(data.get('ebitda', revenue * 0.15))
        valuation = ebitda * 5.0
        
        return jsonify({
            "valuation": valuation,
            "metrics": {
                "revenue": revenue,
                "ebitda": ebitda,
                "ebitda_margin": (ebitda / revenue * 100) if revenue else 0
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    print("Starting server...")  # Debug print
    app.run(debug=True, port=5000)
