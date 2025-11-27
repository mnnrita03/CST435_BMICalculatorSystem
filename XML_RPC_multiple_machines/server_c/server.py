# server_c/server.py
from xmlrpc.server import SimpleXMLRPCServer

def categorize_bmi(bmi):
    """Categorize BMI into standard health ranges."""
    try:
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"
        return category
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("0.0.0.0", 8002), allow_none=True)
    server.register_function(categorize_bmi, "categorize_bmi")
    print("[Server C] Running on port 8002...")
    server.serve_forever()
