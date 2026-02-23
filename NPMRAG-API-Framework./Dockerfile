FROM ollama/ollama:latest

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv netcat-openbsd tesseract-ocr \
    libsm6 libxext6 libxrender-dev ffmpeg poppler-utils \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn
RUN pip install --no-cache-dir moviepy==1.0.3

COPY . .
RUN chmod +x entrypoint.sh

ENV OLLAMA_HOST=127.0.0.1:11434
EXPOSE 7860

ENTRYPOINT []
CMD ["/bin/bash", "entrypoint.sh"]
