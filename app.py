from flask import Flask, request, jsonify
from flask_cors import CORS  # Ensure CORS is enabled

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route('/')
def home():
    return "Flask is running!"

@app.route('/api/valuate', methods=['POST'])
def valuate():
    data = request.json
    annual_revenue = data.get('annual_revenue', 0)
    ebitda = data.get('ebitda', 0)
    multiple = data.get('multiple', 5)
    valuation = ebitda * multiple
    return jsonify({'valuation': valuation})

if __name__ == '__main__':
    app.run(debug=True)

