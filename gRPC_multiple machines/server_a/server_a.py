from concurrent import futures
import grpc
import os
import sys
import sqlite3
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bmi_pb2
import bmi_pb2_grpc

# --- Environment Variables ---
PORT = os.environ.get("PORT", "50051")
B_ADDR = os.environ.get("B_ADDR", "server_b:50052")
C_ADDR = os.environ.get("C_ADDR", "server_c:50053")
D_ADDR = os.environ.get("D_ADDR", "server_d:50054")
DB_PATH = "bmi_data.db"

# --- Initialize SQLite Database ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bmi_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            weight REAL,
            height REAL,
            age INTEGER,
            bmi REAL,
            category TEXT,
            recommendation TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()


class ServerAService(bmi_pb2_grpc.ServerAServiceServicer):
    def __init__(self):
        # Create persistent channels for B, C, D
        self.channel_b = grpc.insecure_channel(B_ADDR)
        self.channel_c = grpc.insecure_channel(C_ADDR)
        self.channel_d = grpc.insecure_channel(D_ADDR)

        # Reusable stubs
        self.bmi_stub = bmi_pb2_grpc.BMIServiceStub(self.channel_b)
        self.category_stub = bmi_pb2_grpc.CategoryServiceStub(self.channel_c)
        self.recommend_stub = bmi_pb2_grpc.RecommendationServiceStub(self.channel_d)

    def SubmitUser(self, request, context):
        start = time.time()
        try:
            # --- Step 1: Call Server B (BMI Calculation) ---
            bmi_resp = self.bmi_stub.CalculateBMI(
                bmi_pb2.BMIRequest(weight=request.weight, height=request.height)
            )
            bmi = bmi_resp.bmi

            # --- Step 2: Call Server C (Category Classification) ---
            category_resp = self.category_stub.ClassifyBMI(
                bmi_pb2.ClassifyRequest(bmi=bmi)
            )
            category = category_resp.category

            # --- Step 3: Call Server D (Recommendation) ---
            recommend_resp = self.recommend_stub.GetRecommendation(
                bmi_pb2.RecommendationRequest(category=category, age=request.age)
            )
            recommendation = recommend_resp.recommendation

            # --- Step 4: Store into SQLite ---
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bmi_data (name, weight, height, age, bmi, category, recommendation)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (request.name, request.weight, request.height, request.age, bmi, category, recommendation))
            conn.commit()
            conn.close()

            # --- Step 5: Combine all results and return ---
            result = bmi_pb2.FinalResult(
                name=request.name,
                weight=request.weight,
                height=request.height,
                age=request.age,
                bmi=bmi,
                category=category,
                recommendation=recommendation
            )

            elapsed = (time.time() - start) * 1000
            print(f"[Server A] ✅ Stored data for {request.name} | Processed in {elapsed:.2f} ms")
            return result

        except grpc.RpcError as e:
            print(f"[Server A] ❌ gRPC error: {e.code()} - {e.details()}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to communicate with one of the servers")
            return bmi_pb2.FinalResult()

        except Exception as e:
            print(f"[Server A] ❌ Unexpected error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return bmi_pb2.FinalResult()


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[('grpc.max_concurrent_streams', 100)]
    )
    bmi_pb2_grpc.add_ServerAServiceServicer_to_server(ServerAService(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    print(f"✅ Server A (gRPC) running on :{PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
