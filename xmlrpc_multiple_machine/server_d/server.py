# server_d/server.py
from xmlrpc.server import SimpleXMLRPCServer

def get_recommendation(category, age):
    """Return a health recommendation based on BMI category and age."""
    try:
        # Base recommendation by category
        if category == "Underweight":
            rec = "Increase calorie intake and do light exercise."
        elif category in ("Normal weight", "Normal"):
            rec = "Maintain your routine and eat balanced meals."
        elif category == "Overweight":
            rec = "Try to exercise 3 times a week and reduce sugar intake."
        elif category == "Obese":
            rec = "Consult a doctor and follow a structured diet plan."
        else:
            rec = "Unknown category. Please consult a healthcare professional."

        # Adjust for age
        if age < 18:
            rec += " Ensure proper nutrition for healthy growth."
        elif age > 50:
            rec += " Focus on light exercises suitable for your age."

        print(f"[Server D] Recommendation generated for {category} (age {age}): {rec}")
        return rec

    except Exception as e:
        return f"Error generating recommendation: {str(e)}"

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("0.0.0.0", 8003), allow_none=True)
    server.register_function(get_recommendation, "get_recommendation")
    print("[Server D] Running on port 8003...")
    server.serve_forever()
