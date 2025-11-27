from datetime import datetime
import time
import os
import grpc
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bmi_pb2
import bmi_pb2_grpc


A_ADDR = os.environ.get("A_ADDR", "localhost:50051")


def main():
    print("=== BMI Calculator Client (gRPC Batch Mode) ===")

    data_file = "bmi_data.txt"

    if not os.path.exists(data_file):
        print(f"❌ File '{data_file}' not found!")
        return

    with open(data_file, "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    total_requests = len(lines)
    total_time = 0
    success_count = 0
    fail_count = 0

    print(f"📦 Sending {total_requests} BMI requests to gRPC server...\n")

    # Connect once, reuse channel
    with grpc.insecure_channel(A_ADDR) as ch:
        stub = bmi_pb2_grpc.ServerAServiceStub(ch)

        for idx, line in enumerate(lines, start=1):
            try:
                name, weight, height, age = [x.strip() for x in line.split(",")]
                weight = float(weight)
                height = float(height)
                age = int(age)

                req = bmi_pb2.UserRequest(name=name, weight=weight, height=height, age=age)

                start_time = time.perf_counter()
                resp = stub.SubmitUser(req)
                elapsed_time = time.perf_counter() - start_time
                total_time += elapsed_time

                print(f"✅ {idx}. {resp.name} | BMI: {resp.bmi:.2f} | {resp.category}")
                print(f"   Recommendation: {resp.recommendation}")
                print(f"   ⏱️ Time: {elapsed_time:.3f}s\n")
                success_count += 1

            except grpc.RpcError as e:
                print(f"❌ gRPC error for {name}: {e.code()} - {e.details()}")
                fail_count += 1
                continue
            except ValueError:
                print(f"⚠️ Skipping invalid line: {line}")
                fail_count += 1
                continue
            except Exception as e:
                print(f"❌ Unexpected error for {line}: {e}")
                fail_count += 1
                continue

    avg_time = total_time / total_requests if total_requests else 0
    throughput = total_requests / total_time if total_time > 0 else 0

    print("\n--- Summary ---")
    print(f"✅ Successful requests: {success_count}")
    print(f"❌ Failed requests: {fail_count}")
    print(f"📈 Total Time: {total_time:.2f} seconds")
    print(f"⚡ Average Time per Request: {avg_time:.3f} seconds")
    print(f"💨 Throughput: {throughput:.2f} requests/sec")


if __name__ == "__main__":
    main()
