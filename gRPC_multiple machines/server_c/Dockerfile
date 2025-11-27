FROM python:3.10-slim
WORKDIR /app

COPY ../bmi.proto /proto/bmi.proto
COPY server_c/server_c.py /app/server_c.py

RUN pip install grpcio grpcio-tools
RUN python -m grpc_tools.protoc -I/proto --python_out=. --grpc_python_out=. /proto/bmi.proto

EXPOSE 50053
CMD ["python", "server_c.py"]