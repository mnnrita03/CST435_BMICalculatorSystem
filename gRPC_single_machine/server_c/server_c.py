from concurrent import futures
import grpc
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bmi_pb2
import bmi_pb2_grpc

# --- Configuration ---
PORT = os.getenv("PORT", "50053")

# gRPC performance tuning options
GRPC_OPTIONS = [
    ('grpc.keepalive_time_ms', 10000),                  # 10s ping
    ('grpc.keepalive_timeout_ms', 5000),                # 5s timeout
    ('grpc.max_send_message_length', 10 * 1024 * 1024), # 10MB
    ('grpc.max_receive_message_length', 10 * 1024 * 1024),
]

def classify(bmi: float) -> str:
    """Return BMI category based on WHO classification."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25.0:
        return "Normal"
    elif bmi < 30.0:
        return "Overweight"
    else:
        return "Obese"

class CategoryService(bmi_pb2_grpc.CategoryServiceServicer):
    def ClassifyBMI(self, request, context):
        """Classify BMI and return category."""
        start = time.time()

        bmi_value = request.bmi

        # Validate input
        if bmi_value <= 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("BMI value must be positive.")
            return bmi_pb2.ClassifyResponse(category="Invalid BMI")

        # Classify
        category = classify(bmi_value)
        elapsed = (time.time() - start) * 1000

        print(f"[Server C] ✅ BMI={bmi_value:.2f} → Category={category} ({elapsed:.2f} ms)")
        return bmi_pb2.ClassifyResponse(category=category)

def serve():
    """Run gRPC CategoryService server."""
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=GRPC_OPTIONS
    )
    bmi_pb2_grpc.add_CategoryServiceServicer_to_server(CategoryService(), server)
    server.add_insecure_port(f"localhost:{PORT}")
    print(f"✅ Server C (CategoryService) running on port {PORT}")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
