FROM python:3.9.7-slim-buster

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    ffmpeg \
    aria2 \
    build-essential \
    libmediainfo-dev \
    python3-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

EXPOSE 5000

CMD ["python", "./main.py"]
