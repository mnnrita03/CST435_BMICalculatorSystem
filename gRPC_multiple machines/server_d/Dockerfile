FROM python:3.10-slim
WORKDIR /app

COPY ../bmi.proto /proto/bmi.proto
COPY server_d/server_d.py /app/server_d.py

RUN pip install grpcio grpcio-tools
RUN python -m grpc_tools.protoc -I/proto --python_out=. --grpc_python_out=. /proto/bmi.proto

EXPOSE 50054
CMD ["python", "server_d.py"]