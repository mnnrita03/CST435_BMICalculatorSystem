FROM python:3.10-slim
WORKDIR /app

COPY ../bmi.proto /proto/bmi.proto
COPY client/client.py /app/client.py
COPY client/bmi_data.txt /app/bmi_data.txt

RUN pip install grpcio grpcio-tools
RUN python -m grpc_tools.protoc -I/proto --python_out=. --grpc_python_out=. /proto/bmi.proto

CMD ["python", "client.py"]