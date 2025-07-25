import runpod
import base64
import io
import torch
from PIL import Image
from diffusers import StableDiffusionControlNetImg2ImgPipeline, ControlNetModel, DDIMScheduler
from diffusers.utils import load_image

# Global variables for model caching
controlnet = None
pipe = None

def initialize_models():
    """Initialize models once for reuse"""
    global controlnet, pipe
    
    if controlnet is None:
        controlnet = ControlNetModel.from_pretrained("DionTimmer/controlnet_qrcode-control_v11p_sd21",
                                                     torch_dtype=torch.float16)
    
    if pipe is None:
        pipe = StableDiffusionControlNetImg2ImgPipeline.from_pretrained(
            "stabilityai/stable-diffusion-2-1",
            controlnet=controlnet,
            safety_checker=None,
            torch_dtype=torch.float16
        )
        
        pipe.enable_xformers_memory_efficient_attention()
        pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
        pipe.enable_model_cpu_offload()
    
    return pipe

def resize_for_condition_image(input_image: Image, resolution: int):
    input_image = input_image.convert("RGB")
    W, H = input_image.size
    k = float(resolution) / min(H, W)
    H *= k
    W *= k
    H = int(round(H / 64.0)) * 64
    W = int(round(W / 64.0)) * 64
    img = input_image.resize((W, H), resample=Image.LANCZOS)
    return img

def generate_qr_image(
    prompt="a billboard in NYC with a qrcode",
    negative_prompt="ugly, disfigured, low quality, blurry, nsfw",
    qr_code_url="https://s3.amazonaws.com/moonup/production/uploads/6064e095abd8d3692e3e2ed6/A_RqHaAM6YHBodPLwqtjn.png",
    init_image_url="https://s3.amazonaws.com/moonup/production/uploads/noauth/KfMBABpOwIuNolv1pe3qX.jpeg",
    guidance_scale=20,
    controlnet_conditioning_scale=1.5,
    strength=0.9,
    num_inference_steps=150,
    seed=123121231
):
    """Generate QR code image with given parameters"""
    
    # Initialize models
    pipe = initialize_models()
    
    # Load images
    source_image = load_image(qr_code_url)
    init_image = load_image(init_image_url)
    
    # Resize images
    condition_image = resize_for_condition_image(source_image, 768)
    init_image = resize_for_condition_image(init_image, 768)
    
    # Generate image
    generator = torch.manual_seed(seed)
    result = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=init_image,
        control_image=condition_image,
        width=768,
        height=768,
        guidance_scale=guidance_scale,
        controlnet_conditioning_scale=controlnet_conditioning_scale,
        generator=generator,
        strength=strength,
        num_inference_steps=num_inference_steps,
    )
    
    return result.images[0]

async def handler(job):
    """
    RunPod serverless handler function for QR code generation
    """
    try:
        # Extract input data from the request
        input_data = job["input"]
        
        # Extract parameters
        prompt = input_data.get('prompt', 'a billboard in NYC with a qrcode')
        negative_prompt = input_data.get('negative_prompt', 'ugly, disfigured, low quality, blurry, nsfw')
        qr_code_url = input_data.get('qr_code_url', 'https://s3.amazonaws.com/moonup/production/uploads/6064e095abd8d3692e3e2ed6/A_RqHaAM6YHBodPLwqtjn.png')
        init_image_url = input_data.get('init_image_url', 'https://s3.amazonaws.com/moonup/production/uploads/noauth/KfMBABpOwIuNolv1pe3qX.jpeg')
        guidance_scale = input_data.get('guidance_scale', 20)
        controlnet_conditioning_scale = input_data.get('controlnet_conditioning_scale', 1.5)
        strength = input_data.get('strength', 0.9)
        num_inference_steps = input_data.get('num_inference_steps', 150)
        seed = input_data.get('seed', 123121231)
        
        # Generate image
        image = generate_qr_image(
            prompt=prompt,
            negative_prompt=negative_prompt,
            qr_code_url=qr_code_url,
            init_image_url=init_image_url,
            guidance_scale=guidance_scale,
            controlnet_conditioning_scale=controlnet_conditioning_scale,
            strength=strength,
            num_inference_steps=num_inference_steps,
            seed=seed
        )
        
        # Convert image to base64
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        image_b64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Return the result
        return {
            'success': True,
            'image': image_b64,
            'format': 'PNG'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

runpod.serverless.start({"handler": handler})