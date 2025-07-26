FROM runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04

WORKDIR /

# Copy application code
COPY handler.py .

# Set environment variables for model caching and Python packages (network volume)
ENV HF_HOME=/runpod-volume
ENV TRANSFORMERS_CACHE=/runpod-volume
ENV HF_DATASETS_CACHE=/runpod-volume
ENV PYTHONPATH=/runpod-volume:$PYTHONPATH

CMD ["python3", "-u", "/handler.py"]