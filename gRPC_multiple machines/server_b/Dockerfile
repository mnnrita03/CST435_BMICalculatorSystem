FROM python:3.10-slim
WORKDIR /app

COPY ../bmi.proto /proto/bmi.proto
COPY server_b/server_b.py /app/server_b.py

RUN pip install grpcio grpcio-tools
RUN python -m grpc_tools.protoc -I/proto --python_out=. --grpc_python_out=. /proto/bmi.proto

EXPOSE 50052
CMD ["python", "server_b.py"]