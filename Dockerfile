FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    tshark nmap libpcap0.8 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install uv
COPY requirements.txt .
RUN uv pip install -r requirements.txt

COPY app/ app/
COPY app/cli.py cli.py

ENTRYPOINT ["python", "cli.py"]
