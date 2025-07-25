# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a QR code AI image generation project that uses Stable Diffusion 2.1 with ControlNet to create artistic images that contain functional QR codes. The project leverages the DionTimmer controlnet_qrcode-control_v11p_sd21 model to maintain QR code readability while applying artistic transformations.

## Architecture

- **Single-file application**: The entire functionality is contained in `main.py`
- **Pipeline setup**: Uses `StableDiffusionControlNetImg2ImgPipeline` with ControlNet for QR code preservation
- **Image processing**: Includes image resizing functionality to ensure proper aspect ratios for the model
- **Memory optimization**: Configured with xformers memory efficient attention and CPU offloading

## Key Dependencies

The project requires:
- `torch` - PyTorch for deep learning operations
- `diffusers` - Hugging Face Diffusers library for Stable Diffusion pipeline
- `PIL` (Pillow) - Image processing library

## Running the Application

To run the QR code generation:
```bash
python main.py
```

## Key Parameters for QR Code Generation

The main generation function uses these critical parameters:
- `guidance_scale`: Controls how closely the model follows the prompt (set to 20)
- `controlnet_conditioning_scale`: Controls QR code preservation strength (set to 1.5)
- `strength`: Controls how much the initial image is transformed (set to 0.9)
- `num_inference_steps`: Number of denoising steps (set to 150)

## Model Configuration

- **Base model**: stabilityai/stable-diffusion-2-1
- **ControlNet**: DionTimmer/controlnet_qrcode-control_v11p_sd21
- **Scheduler**: DDIMScheduler
- **Resolution**: 768x768 pixels
- **Precision**: float16 for memory efficiency

## Image Processing

The `resize_for_condition_image()` function ensures images are properly sized:
- Converts to RGB format
- Maintains aspect ratio
- Rounds dimensions to multiples of 64 (required by the model)
- Uses LANCZOS resampling for quality

## RunPod Hub Deployment

This project is configured for RunPod Hub deployment with:

### Required Files
- `.runpod/hub.json` - Hub configuration and metadata
- `.runpod/tests.json` - Test cases for validation
- `handler.py` - Main serverless function
- `Dockerfile` - Container configuration
- `README.md` - Documentation

### Deployment Process
1. Create GitHub release
2. RunPod Hub automatically indexes the release
3. Manual review by RunPod team
4. Published to RunPod Hub marketplace

### Configuration
- **Machine**: RTX A4000 with 16GB RAM, 4 CPU cores
- **Container**: 20GB disk space
- **Models**: Pre-cached during build for faster cold starts
- **Environment**: CUDA 11.8 compatible

## Development Notes

- Generator seed is configurable via API (default: 123121231)
- Safety checker is disabled in the pipeline configuration
- Memory optimizations are enabled with CPU offloading
- Models are cached globally to reduce cold start times