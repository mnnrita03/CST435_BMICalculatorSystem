FROM python:3.10-slim
WORKDIR /app

COPY ../bmi.proto /proto/bmi.proto
COPY server_a/server_a.py /app/server_a.py

RUN pip install grpcio grpcio-tools
RUN python -m grpc_tools.protoc -I/proto --python_out=. --grpc_python_out=. /proto/bmi.proto

RUN mkdir -p /data
ENV DB_PATH=/data/bmi.db \
    B_ADDR=server_b:50052 \
    C_ADDR=server_c:50053 \
    D_ADDR=server_d:50054 \
    PORT=50051
    
EXPOSE 50051
CMD ["python", "server_a.py"]