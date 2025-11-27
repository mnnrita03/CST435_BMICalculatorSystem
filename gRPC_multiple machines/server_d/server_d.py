from concurrent import futures
import grpc
import os
import sys

# Add parent directory to Python path for importing generated files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bmi_pb2
import bmi_pb2_grpc

# Use environment variable for port (Docker-friendly)
PORT = os.getenv("PORT", "50054")

# Optional: gRPC tuning for better performance (especially in containers)
GRPC_OPTIONS = [
    ('grpc.keepalive_time_ms', 10000),           # Keepalive ping every 10s
    ('grpc.keepalive_timeout_ms', 5000),         # Timeout if no ACK within 5s
    ('grpc.max_send_message_length', 10 * 1024 * 1024),  # 10 MB
    ('grpc.max_receive_message_length', 10 * 1024 * 1024),
]

def recommend(category: str, age: int) -> str:
    """Generate personalized health recommendation based on BMI category and age."""
    if category == "Underweight":
        msg = "Increase your calorie intake and include strength training."
    elif category == "Normal":
        msg = "Maintain your current lifestyle and stay active."
    elif category == "Overweight":
        msg = "Exercise 3 times a week and monitor your calorie intake."
    else:
        msg = "Consult a doctor and start a guided weight-loss program."

    # Add age-specific advice
    if age < 18:
        msg += " (Ensure proper nutrition for your growth.)"
    elif age > 50:
        msg += " (Focus on light exercise suitable for your age.)"

    return msg


class RecommendationService(bmi_pb2_grpc.RecommendationServiceServicer):
    """Implements the GetRecommendation RPC."""
    def GetRecommendation(self, request, context):
        advice = recommend(request.category, request.age)
        return bmi_pb2.RecommendationResponse(recommendation=advice)


def serve():
    """Start gRPC server for RecommendationService."""
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=GRPC_OPTIONS
    )
    bmi_pb2_grpc.add_RecommendationServiceServicer_to_server(RecommendationService(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    print(f"✅ Server D (RecommendationService) running on port {PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
