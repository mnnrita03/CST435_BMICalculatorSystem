from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/bmi_category', methods=['POST'])
def bmi_category():
    data = request.get_json()
    bmi = data.get("bmi")

    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return jsonify({"category": category})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
