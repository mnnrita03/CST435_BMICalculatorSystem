from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate_bmi', methods=['POST'])
def calculate_bmi():
    data = request.get_json()
    weight = data.get("weight")
    height = data.get("height")
    bmi = round(weight / (height ** 2), 2)
    return jsonify({"bmi": bmi})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
