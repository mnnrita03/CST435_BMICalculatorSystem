FROM python:3.10-slim
WORKDIR /app
COPY client.py .
COPY bmi_data.txt .
RUN pip install requests
CMD ["python", "client.py"]
