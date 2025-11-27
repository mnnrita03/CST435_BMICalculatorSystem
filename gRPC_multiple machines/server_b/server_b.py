from concurrent import futures
import grpc
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bmi_pb2
import bmi_pb2_grpc

# --- Configuration ---
PORT = os.getenv("PORT", "50052")

# Optional: gRPC tuning (good for Docker / performance)
GRPC_OPTIONS = [
    ('grpc.keepalive_time_ms', 10000),                  # 10s ping
    ('grpc.keepalive_timeout_ms', 5000),                # 5s timeout
    ('grpc.max_send_message_length', 10 * 1024 * 1024), # 10MB
    ('grpc.max_receive_message_length', 10 * 1024 * 1024),
]

class BMIService(bmi_pb2_grpc.BMIServiceServicer):
    def CalculateBMI(self, request, context):
        """
        Calculate BMI = weight / (height^2)
        - Protect against division by zero
        - Round to 2 decimal places for consistency
        """
        start = time.time()

        if request.height <= 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Height must be greater than zero.")
            return bmi_pb2.BMIResponse(bmi=0.0)

        bmi = request.weight / (request.height ** 2)
        elapsed = (time.time() - start) * 1000

        print(f"[Server B] ✅ Calculated BMI for weight={request.weight}, height={request.height:.2f} → BMI={bmi:.2f} ({elapsed:.2f} ms)")
        return bmi_pb2.BMIResponse(bmi=bmi)

def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=GRPC_OPTIONS
    )
    bmi_pb2_grpc.add_BMIServiceServicer_to_server(BMIService(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    print(f"✅ Server B (BMIService) running on port {PORT}")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
