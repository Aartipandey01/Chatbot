from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your currency conversion function
def convert_currency(from_currency, to_currency, amount):
    # Free API endpoint for currency conversion
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"

    try:
        response = requests.get(url)
        data = response.json()

        if 'rates' not in data or to_currency not in data['rates']:
            return None

        rate = data['rates'][to_currency]
        converted_amount = amount * rate

        return converted_amount

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Route for chatbot interaction
@app.route('/convert', methods=['POST'])
def convert():
    data = request.json

    if not all(k in data for k in ("from_currency", "to_currency", "amount")):
        return jsonify({"error": "Missing parameters"}), 400

    from_currency = data['from_currency'].upper()
    to_currency = data['to_currency'].upper()
    amount = float(data['amount'])

    converted_amount = convert_currency(from_currency, to_currency, amount)

    if converted_amount is None:
        return jsonify({"error": "Conversion failed. Check the currency codes and try again."}), 400

    return jsonify({
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": amount,
        "converted_amount": converted_amount
    })

if __name__ == '__main__':
    app.run(debug=True)
