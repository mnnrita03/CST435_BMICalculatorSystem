from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/recommendation', methods=['POST'])
def recommendation():
    data = request.get_json()
    category = data.get("category")
    age = data.get("age")

    # Basic health advice logic
    if category == "Underweight":
        msg = "Increase your calorie intake and include strength training."
    elif category == "Normal weight":
        msg = "Maintain your current lifestyle and stay active."
    elif category == "Overweight":
        msg = "Exercise 3 times a week and monitor your calorie intake."
    else:
        msg = "Consult a doctor and start a guided weight-loss program."

    # Age factor adjustment
    if age < 18:
        msg += " (Ensure proper nutrition for your growth.)"
    elif age > 50:
        msg += " (Focus on light exercise suitable for your age.)"

    return jsonify({"recommendation": msg})

if __name__ == "__main__":
    app.run(host="localhost", port=5003)
