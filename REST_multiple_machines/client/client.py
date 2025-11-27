import requests
import time
import os

def main():
    print("=== BMI Calculator Client (Batch Mode) ===")

    server_a_url = os.getenv("SERVER_A_URL", "http://server_a:5000")
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
            weight = float(weight)
            height = float(height)
            age = int(age)

            user_data = {
                "name": name,
                "weight": weight,
                "height": height,
                "age": age
            }

            start_time = time.time()
            response = requests.post(f"{server_a_url}/submit", json=user_data)
            end_time = time.time()
            elapsed_time = end_time - start_time
            total_time += elapsed_time

            if response.status_code == 200:
                result = response.json()

                bmi = result.get("bmi")
                category = result.get("category")
                recommendation = result.get("recommendation")

                try:
                    bmi_fmt = f"{float(bmi):.2f}"
                except (TypeError, ValueError):
                    bmi_fmt = "N/A"

                print(f"✅ {name} | BMI: {bmi_fmt} (from Server B) | {category} (from Server C)")
                print(f"   Recommendation (from Server D): {recommendation}")
                print(f"   ⏱️ Time: {elapsed_time:.3f}s\n")
                success_count += 1
            else:
                print(f"❌ Error for {name}: {response.status_code} {response.text}")
                fail_count += 1

        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to Server A. Check that servers are running.")
            fail_count += 1
            break
        except ValueError:
            print(f"⚠️ Skipping invalid line: {line}")
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
