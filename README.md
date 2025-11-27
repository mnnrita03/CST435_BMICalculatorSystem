# CST435_BMICalculatorSystem: Cloud and Parallel Computing Assignment 1

School of Computer Sciences - University Sains Malaysia
CST435 Cloud and Parallel Computing

Lecturer: Associate Professor Dr. Chan Huah Yong

Prepared by:
| NAME                                | MATRIC NUMBER |
|-------------------------------------|---------------|
| Asilah Zarifah Binti Rosli          | 160458        |
| Norita Binti Muin                   | 160453        |
| Nurul Afiqah Binti Azhar            | 160335        |
| Siti Nawwarah Binti Mohd Abd Hadi   | 160304        |
| Siti Nur Izzah Binti Abdul Rahman   | 160302        |

---

### **1. Introduction**

This repository contains the source code and configuration files for a multi-server **Body Mass Index (BMI) processing system** developed for the Cloud and Parallel Computing (CST435) course.

The primary goal is to compare the performance of three communication protocols (**gRPC, REST, and XML-RPC**) within a **Pipeline Parallelism** architecture, tested across two environments: a single-machine local setup and a multi-machine simulation using **Docker containers**.

---

### **2. System Architecture: 4-Stage Pipeline Parallelism**

The system processes data records (105 inputs) through a four-stage pipeline, maximizing **throughput** by allowing all servers to work concurrently on different data records. 
| Stage | Server | Function | Communication Protocol |
| :--- | :--- | :--- | :--- |
| **Stage 1** | `server_a` | **Data Storage** (Inserts into SQLite DB) | Receives from Client |
| **Stage 2** | `server_b` | **BMI Calculation** | Receives from A, Sends to C |
| **Stage 3** | `server_c` | **BMI Categorization** | Receives from B, Sends to D |
| **Stage 4** | `server_d` | **Recommendation Generation** | Receives from C, Sends result to Client |

---

### **3. Repository Structure**

The repository is organized by protocol and deployment environment:

* **`gRPC_single_machine`**: Code for gRPC protocol deployed locally on a single host.
* **`gRPC_multiple_machines`**: Code and `Dockerfile`s for gRPC deployed via Docker Compose.
* **`REST_single_machine`**: Code for REST API deployed locally on a single host.
* **`REST_multiple_machines`**: Code and `Dockerfile`s for REST API deployed via Docker Compose.
* **`XML_RPC_single_machine`**: Code for XML-RPC deployed locally on a single host.
* **`XML_RPC_multiple_machines`**: Code and `Dockerfile`s for XML-RPC deployed via Docker Compose.

---

### **4. How to Run the Experiments**

#### **A. Multiple Machine (Docker) Deployment (Recommended)**

This method simulates a real distributed system and requires Docker and Docker Compose installed.

1.  **Navigate** to the desired protocol folder (e.g., `REST_multiple_machines`).
    ```bash
    cd REST_multiple_machines
    ```
2.  **Build and Run** all services (4 servers + 1 client) simultaneously:
    ```bash
    docker compose up --build
    ```
3.  The client will execute the batch job and print the final **Total Time** and **Throughput**.
4.  To stop the services:
    ```bash
    docker compose down
    ```

#### **B. Single Machine Deployment**

This requires setting up dependencies manually and running each server in a separate terminal window.

1.  **Install dependencies** (Flask, Requests, gRPC, etc. - depends on the folder).
2.  Open **five separate terminal windows**.
3.  In the first four windows, run the servers:
    ```bash
    python3 server_a.py
    python3 server_b.py
    python3 server_c.py
    python3 server_d.py
    ```
4.  In the fifth window, run the client:
    ```bash
    python3 client.py
    ```

---

### **5. Key Findings Summary**

<img width="568" height="227" alt="image" src="https://github.com/user-attachments/assets/c7856e2f-bcf9-4f03-b414-8dc593b1a0ef" />

* **Fastest Protocol:** **gRPC** provided the highest throughput due to its binary messaging and HTTP/2 usage.
* **Best Environment:** The **Docker container** deployment proved nearly **2x faster** than the single-machine local setup, validating the benefits of resource isolation for parallel workloads.
