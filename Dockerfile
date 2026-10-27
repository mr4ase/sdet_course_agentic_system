FROM python:3.13-slim
RUN pip install --no-cache-dir pytest==9.1.1 requests==2.34.2 httpx==0.28.1
WORKDIR /sandbox
