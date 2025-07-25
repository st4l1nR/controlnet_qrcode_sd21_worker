FROM nvidia/cuda:11.8-runtime-ubuntu22.04

WORKDIR /

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY handler.py .

# Set environment variables for model caching (container volume)
ENV HF_HOME=/tmp/models
ENV TRANSFORMERS_CACHE=/tmp/models
ENV HF_DATASETS_CACHE=/tmp/models

CMD ["python3", "-u", "/handler.py"]