# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a QR code AI image generation project that uses Stable Diffusion 2.1 with ControlNet to create artistic images that contain functional QR codes. The project is designed as a RunPod serverless function that leverages the DionTimmer controlnet_qrcode-control_v11p_sd21 model to maintain QR code readability while applying artistic transformations.

## Core Architecture

- **Serverless handler**: Main functionality in `handler.py` with RunPod serverless architecture
- **Global model caching**: Models are loaded once and cached globally (`controlnet` and `pipe` variables)
- **Pipeline setup**: Uses `StableDiffusionControlNetImg2ImgPipeline` with ControlNet for QR code preservation
- **Image processing**: Custom `resize_for_condition_image()` function ensures proper aspect ratios
- **Memory optimization**: Configured with xformers memory efficient attention and CPU offloading

## Development Commands

### Testing
```bash
# Test the handler function locally
python test.py

# Test imports and dependencies
python -c "from test import test_imports; test_imports()"
```

### Dependencies Installation
```bash
# Install all required packages
pip install -r requirements.txt
```

### Docker Development
```bash
# Build the container
docker build -t qr-ai-generator .

# Run locally (requires NVIDIA Docker runtime)
docker run --gpus all qr-ai-generator
```

## Key Dependencies

Critical packages from `requirements.txt`:
- `torch` - PyTorch for deep learning operations  
- `diffusers` - Hugging Face Diffusers library for Stable Diffusion pipeline
- `transformers` - Model loading and tokenization
- `accelerate` - Hardware acceleration
- `xformers` - Memory efficient attention
- `Pillow` - Image processing
- `runpod` - Serverless runtime

## Model Configuration Details

- **Base model**: stabilityai/stable-diffusion-2-1
- **ControlNet**: DionTimmer/controlnet_qrcode-control_v11p_sd21  
- **Scheduler**: DDIMScheduler
- **Resolution**: 768x768 pixels
- **Precision**: float16 for memory efficiency
- **Model initialization**: Happens in `initialize_models()` with global caching

## Handler Function Structure

The `handler(event)` function in `handler.py`:
1. Extracts parameters from `event["input"]`
2. Calls `generate_qr_image()` with parameters
3. Converts PIL image to base64 PNG
4. Returns JSON response with success status

### Key Parameters
- `guidance_scale`: Controls prompt adherence (default: 20)
- `controlnet_conditioning_scale`: QR code preservation strength (default: 1.5)
- `strength`: Image transformation amount (default: 0.9)
- `num_inference_steps`: Generation quality/speed trade-off (default: 150)
- `seed`: Reproducible generation (default: 123121231)

## Image Processing Pipeline

The `resize_for_condition_image()` function:
- Converts to RGB format
- Maintains aspect ratio  
- Rounds dimensions to multiples of 64 (model requirement)
- Uses LANCZOS resampling for quality

## Testing Strategy

The `test.py` provides:
- Import validation for all dependencies
- Handler function testing with sample inputs
- Automatic test image generation (`test_output.png`)
- Error handling and debugging information

## RunPod Deployment Architecture

### Container Configuration
- **Base**: NVIDIA CUDA 11.8 runtime on Ubuntu 22.04
- **Python**: 3.x with pip and development tools
- **Model caching**: `/tmp/models` directory for HuggingFace cache
- **Entry point**: `handler.py` as serverless function

### Environment Variables
- `HF_HOME=/tmp/models` - HuggingFace model cache
- `TRANSFORMERS_CACHE=/tmp/models` - Transformers cache
- `HF_DATASETS_CACHE=/tmp/models` - Datasets cache

## Memory and Performance Optimizations

- Global model caching prevents cold start penalties
- CPU offloading (`pipe.enable_model_cpu_offload()`) manages GPU memory
- XFormers attention (`pipe.enable_xformers_memory_efficient_attention()`) reduces memory usage
- float16 precision balances quality and performance
- Safety checker disabled for faster inference

## API Input/Output Format

### Input Structure
```json
{
  "input": {
    "prompt": "string",
    "negative_prompt": "string", 
    "qr_code_url": "string",
    "init_image_url": "string",
    "guidance_scale": 20,
    "controlnet_conditioning_scale": 1.5,
    "strength": 0.9,
    "num_inference_steps": 150,
    "seed": 123121231
  }
}
```

### Output Structure
```json
{
  "success": true/false,
  "image": "base64_encoded_png",
  "format": "PNG",
  "error": "error_message_if_failed"
}