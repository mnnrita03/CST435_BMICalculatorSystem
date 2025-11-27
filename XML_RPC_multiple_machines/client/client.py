from xmlrpc.client import ServerProxy
import time, os
from datetime import datetime

def main():
    print("=== 🧮 BMI Calculator Client (Batch Mode, XML-RPC) ===")

    a = ServerProxy("http://server_a:8000/", allow_none=True)
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

    print(f"📦 Sending {total_requests} BMI requests...\n")

    for idx, line in enumerate(lines, start=1):
        try:
            name, weight, height, age = [x.strip() for x in line.split(",")]
            weight, height, age = float(weight), float(height), int(age)

            start_time = time.perf_counter()

            # 1️⃣ Submit to Server A (handles entire pipeline)
            res = a.submit_user(name, weight, height, age)
            if not res["ok"]:
                print(f"❌ {name}: Error → {res['error']}")
                fail_count += 1
                continue

            bmi = res["bmi"]
            category = res["category"]
            recommendation = res["recommendation"]

            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            total_time += elapsed_time
            success_count += 1

            print(f"✅ {idx}. {name} | BMI: {bmi:.2f} | {category}")
            print(f"   💬 Recommendation: {recommendation}")
            print(f"   ⏱️ Time: {elapsed_time:.3f}s\n")

        except Exception as e:
            print(f"⚠️ {idx}. Error processing line '{line}': {e}")
            fail_count += 1

    avg_time = total_time / total_requests if total_requests else 0
    throughput = total_requests / total_time if total_time > 0 else 0

    print("\n--- 📊 Summary ---")
    print(f"✅ Successful requests: {success_count}")
    print(f"❌ Failed requests: {fail_count}")
    print(f"⏱️ Total Time: {total_time:.2f} seconds")
    print(f"⚡ Average Time per Request: {avg_time:.3f} seconds")
    print(f"🚀 Throughput: {throughput:.2f} requests/sec")
    print(f"🕒 Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
