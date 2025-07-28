FROM runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04

WORKDIR /

# Copy application code
COPY handler.py .
COPY requirements.txt .

# Install Python packages
RUN pip install -r requirements.txt

CMD ["python3", "-u", "/handler.py"]