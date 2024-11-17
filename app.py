from flask_cors import CORS
from flask import Flask, request, jsonify


app = Flask(__name__)
CORS(app)

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

