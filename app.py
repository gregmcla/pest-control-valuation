from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://pest-control-valuation-1.onrender.com"}})

@app.route('/')
def home():
    return "Flask is running!"

@app.route('/api/valuate', methods=['POST'])
def valuate():
    data = request.json
    annual_revenue = data.get('annual_revenue', 0)
    ebitda = data.get('ebitda', 0)
    industry = data.get('industry', '')
    # Replace the following with your valuation logic
    valuation = ebitda * 5
    return jsonify({'valuation': valuation})

if __name__ == '__main__':
    app.run(debug=True)
