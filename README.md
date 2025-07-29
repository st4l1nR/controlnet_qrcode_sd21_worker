# QR Code AI Art Generator

Generate artistic images containing functional QR codes using Stable Diffusion 2.1 with ControlNet. This serverless function creates stunning visuals that seamlessly blend QR codes with artistic elements while maintaining scannability.

## Features

- **AI-Powered QR Integration**: Uses ControlNet to preserve QR code functionality while applying artistic transformations
- **Stable Diffusion 2.1**: High-quality image generation with artistic control
- **Customizable Parameters**: Fine-tune generation settings for different artistic styles
- **Fast Generation**: Optimized for serverless deployment with model caching
- **Multiple Presets**: Pre-configured settings for different use cases

## How It Works

1. **Input**: Provide a text prompt describing your desired artistic style
2. **QR Code Integration**: The system uses ControlNet to maintain QR code readability
3. **AI Generation**: Stable Diffusion 2.1 creates the artistic image
4. **Output**: Returns a base64-encoded PNG image

## API Usage

### Basic Request
```json
{
  "input": {
    "prompt": "a billboard in NYC with a qrcode"
  }
}
```

### Advanced Request
```json
{
  "input": {
    "prompt": "futuristic neon qr code in cyberpunk city",
    "guidance_scale": 15,
    "controlnet_conditioning_scale": 1.2,
    "strength": 0.8,
    "num_inference_steps": 100,
    "seed": 42
  }
}
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | "a billboard in NYC with a qrcode" | Text describing the desired artistic style |
| `negative_prompt` | string | "ugly, disfigured, low quality..." | Elements to avoid in generation |
| `qr_code_url` | string | Default QR image | URL to QR code image to integrate |
| `init_image_url` | string | Default image | URL to initial/reference image |
| `guidance_scale` | number | 20 | How closely to follow the prompt (1-30) |
| `controlnet_conditioning_scale` | number | 1.5 | QR code preservation strength (0.1-2.0) |
| `strength` | number | 0.9 | Initial image transformation amount (0.1-1.0) |
| `num_inference_steps` | number | 150 | Generation steps - higher = better quality (20-300) |
| `seed` | integer | 123121231 | Random seed for reproducible results |

## Output Format

```json
{
  "success": true,
  "image": "base64_encoded_png_data",
  "format": "PNG"
}
```

## Presets

### Billboard Style
Perfect for advertising and promotional materials:
- High guidance scale (20)
- Strong QR preservation (1.5)
- Heavy transformation (0.9)

### Artistic QR
Balanced artistic interpretation:
- Moderate guidance (15)
- Balanced QR visibility (1.2)
- Medium transformation (0.7)

### High Quality
Maximum quality with longer processing:
- Maximum guidance (25)
- Strongest QR preservation (1.8)
- Nearly complete transformation (0.95)

## Technical Specifications

- **Base Model**: stabilityai/stable-diffusion-2-1
- **ControlNet**: DionTimmer/controlnet_qrcode-control_v11p_sd21
- **Resolution**: 768x768 pixels
- **Precision**: float16 for memory efficiency
- **GPU Requirements**: 8GB+ VRAM recommended
- **Processing Time**: 30-120 seconds depending on steps

## Examples

### Knight Pixel Art Request
```json
{
  "input": {
    "prompt": "a knight holding a sword on pixel art",
    "qr_code_url": "https://media.discordapp.net/attachments/1364954116887023618/1398733806852378654/qr-code.png?ex=688912de&is=6887c15e&hm=fb92911efbcfa3a772bfcaf258e0a393adeb76bd287b4222ae5fe8380050d21f&=&format=webp&quality=lossless&width=480&height=480",
    "init_image_url": "https://media.discordapp.net/attachments/1364954116887023618/1398733807108227192/init_image_qr.jpg?ex=688912de&is=6887c15e&hm=b77c063c503aaa25c8b06944925a23f9325befff9a924a6803aaeda4c56e7e27&=&format=webp&width=480&height=480"
  }
}
```

**Response:**
```json
{
  "success": true,
  "image": "iVBORw0KGgoAAAANSUhEUgAAAwAAAAMACAYAAAC6uhUNAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4xLjMsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy+AADFEAAAgAElEQVR4nOy9eZhlV1k...",
  "format": "PNG"
}
```

### NYC Billboard
```json
{"input": {"prompt": "a billboard in NYC with a qrcode"}}
```

### Cyberpunk Style
```json
{"input": {"prompt": "futuristic neon qr code in cyberpunk city, glowing, high-tech"}}
```

### Nature Integration
```json
{"input": {"prompt": "qr code integrated into forest scene, natural, organic, moss-covered"}}
```

### Minimalist Design
```json
{"input": {"prompt": "minimal modern qr code design, clean, geometric, white background"}}
```

## Environment Variables

For S3 bucket functionality to work with `rp_upload.upload_image()`, configure these environment variables in your RunPod template:

**Required S3 Environment Variables:**
- `BUCKET_ENDPOINT_URL` - Your S3 bucket endpoint URL
- `BUCKET_ACCESS_KEY_ID` - S3 access key ID  
- `BUCKET_SECRET_ACCESS_KEY` - S3 secret access key

**For AWS S3 specifically:**
- `AWS_ACCESS_KEY_ID` - Your AWS access key
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret access key

Set these in your RunPod template's Environment Variables section to enable automatic image uploads to your configured S3 bucket.

## Deployment

This function is optimized for RunPod serverless deployment with:
- Pre-cached models for faster cold starts
- Memory optimization with CPU offloading
- CUDA 11.8 compatibility
- Automatic model downloading during build

### Building and Pushing Docker Image

```bash
docker buildx build \
  --platform linux/amd64 \
  -t st4lin/controlnet_qrcode_sd21_worker:latest \
  -t st4lin/controlnet_qrcode_sd21_worker:stable \
  --push \
  .
```

## License

This project uses the following models:
- Stable Diffusion 2.1 (CreativeML Open RAIL++-M License)
- ControlNet QR Code (Apache 2.0 License)

## Support

For issues and questions, please refer to the RunPod documentation or create an issue in the project repository.

