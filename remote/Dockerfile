FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends adb && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY server.py ./
COPY static ./static
# config.json and the ADB key folder are mounted from the host, see docker-compose.yml.
ENV TV_REMOTE_CONFIG=/config/config.json TV_REMOTE_PROGRESS=/config/PROGRESS.md HOME=/root
EXPOSE 8080
CMD ["sh", "-c", "adb start-server && exec python3 server.py"]
