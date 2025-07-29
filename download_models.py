#!/usr/bin/env python3
"""
Download required models for QR code AI image generation.

This script downloads the required models for the controlnet_qrcode_sd21_worker
and caches them locally to avoid cold start penalties during serverless execution.
"""

import os
import sys
from pathlib import Path
import torch
from diffusers import StableDiffusionControlNetImg2ImgPipeline, ControlNetModel, DDIMScheduler
from huggingface_hub import snapshot_download

def create_model_directories():
    """Create necessary model directories"""
    base_path = Path("/workspace/models")
    controlnet_path = base_path / "controlnet-qr"
    sd21_path = base_path / "sd21"
    
    base_path.mkdir(parents=True, exist_ok=True)
    controlnet_path.mkdir(parents=True, exist_ok=True)
    sd21_path.mkdir(parents=True, exist_ok=True)
    
    return controlnet_path, sd21_path

def download_controlnet_model(cache_dir):
    """Download ControlNet QR code model"""
    print("Downloading ControlNet QR code model...")
    
    try:
        # Download the ControlNet model
        controlnet = ControlNetModel.from_pretrained(
            "DionTimmer/controlnet_qrcode-control_v11p_sd21",
            torch_dtype=torch.float16,
            cache_dir=str(cache_dir)
        )
        
        # Save to local directory
        controlnet.save_pretrained(str(cache_dir))
        print(f"✓ ControlNet model downloaded and saved to {cache_dir}")
        
    except Exception as e:
        print(f"✗ Failed to download ControlNet model: {e}")
        sys.exit(1)

def download_stable_diffusion_model(cache_dir):
    """Download Stable Diffusion 2.1 model"""
    print("Downloading Stable Diffusion 2.1 model...")
    
    try:
        # Download using snapshot_download for better control
        snapshot_download(
            repo_id="stabilityai/stable-diffusion-2-1",
            cache_dir=str(cache_dir),
            local_dir=str(cache_dir),
            local_dir_use_symlinks=False
        )
        print(f"✓ Stable Diffusion 2.1 model downloaded to {cache_dir}")
        
    except Exception as e:
        print(f"✗ Failed to download Stable Diffusion model: {e}")
        sys.exit(1)

def verify_models(controlnet_path, sd21_path):
    """Verify that models can be loaded successfully"""
    print("Verifying model downloads...")
    
    try:
        # Test ControlNet loading
        controlnet = ControlNetModel.from_pretrained(
            str(controlnet_path),
            torch_dtype=torch.float16
        )
        print("✓ ControlNet model verified")
        
        # Test Stable Diffusion pipeline loading
        pipe = StableDiffusionControlNetImg2ImgPipeline.from_pretrained(
            str(sd21_path),
            controlnet=controlnet,
            safety_checker=None,
            torch_dtype=torch.float16
        )
        print("✓ Stable Diffusion pipeline verified")
        
        # Configure scheduler
        pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
        print("✓ DDIM scheduler configured")
        
        return True
        
    except Exception as e:
        print(f"✗ Model verification failed: {e}")
        return False

def main():
    """Main download function"""
    print("Starting model download for QR code AI image generation...")
    print("=" * 60)
    
    # Create model directories
    controlnet_path, sd21_path = create_model_directories()
    
    # Download models
    download_controlnet_model(controlnet_path)
    download_stable_diffusion_model(sd21_path)
    
    # Verify downloads
    if verify_models(controlnet_path, sd21_path):
        print("=" * 60)
        print("✓ All models downloaded and verified successfully!")
        print(f"  - ControlNet: {controlnet_path}")
        print(f"  - Stable Diffusion 2.1: {sd21_path}")
        print("\nModels are ready for use in the serverless handler.")
    else:
        print("✗ Model verification failed. Please check the downloads.")
        sys.exit(1)

if __name__ == "__main__":
    main()