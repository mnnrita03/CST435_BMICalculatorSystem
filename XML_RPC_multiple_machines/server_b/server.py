# server_b/server.py
from xmlrpc.server import SimpleXMLRPCServer

def calculate_bmi_value(weight, height):
    """Calculate BMI based on weight (kg) and height (m)."""
    try:
        if height <= 0:
            return {"ok": False, "error": "Invalid height value"}
        bmi = weight / (height ** 2)
        return {"ok": True, "bmi": round(bmi, 2)}
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("0.0.0.0", 8001), allow_none=True)
    server.register_function(calculate_bmi_value, "calculate_bmi_value")
    print("[Server B] Running on port 8001...")
    server.serve_forever()
