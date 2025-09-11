import os
import io
import base64
import numpy as np
from typing import List, Optional
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel, BlipProcessor, BlipForConditionalGeneration
from diffusers import StableDiffusionPipeline
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Rare Event Detection API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for models and reference data
clip_model = None
clip_processor = None
blip_model = None
blip_processor = None
sd_pipeline = None
device = None
reference_embeddings = []
reference_captions = []

def get_device():
    """Determine the best available device (GPU if available, else CPU)"""
    if torch.cuda.is_available():
        return torch.device("cuda")
    else:
        return torch.device("cpu")

def load_models():
    """Load all required models at startup"""
    global clip_model, clip_processor, blip_model, blip_processor, sd_pipeline, device
    
    device = get_device()
    logger.info(f"Using device: {device}")
    
    try:
        # Load CLIP model for embeddings and similarity
        logger.info("Loading CLIP model...")
        clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        clip_model.to(device)
        
        # Load BLIP model for image captioning
        logger.info("Loading BLIP model...")
        blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        blip_model.to(device)
        
        # Load Stable Diffusion for image generation
        logger.info("Loading Stable Diffusion model...")
        sd_pipeline = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16 if device.type == "cuda" else torch.float32
        )
        sd_pipeline.to(device)
        
        logger.info("All models loaded successfully!")
        
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        raise e

@app.on_event("startup")
async def startup_event():
    """Load models when the application starts"""
    load_models()

def preprocess_image(image_bytes: bytes) -> Image.Image:
    """Convert bytes to PIL Image"""
    image = Image.open(io.BytesIO(image_bytes))
    if image.mode != 'RGB':
        image = image.convert('RGB')
    return image

def compute_clip_embedding(image: Image.Image) -> np.ndarray:
    """Compute CLIP embedding for an image"""
    inputs = clip_processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        image_features = clip_model.get_image_features(**inputs)
        # Normalize the features
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
    return image_features.cpu().numpy()

def compute_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """Compute cosine similarity between two embeddings"""
    return float(np.dot(embedding1.flatten(), embedding2.flatten()))

@app.post("/upload_references")
async def upload_references(
    files: List[UploadFile] = File(...),
    captions: List[str] = Form(...)
):
    """
    Upload reference images with captions for few-shot learning
    """
    global reference_embeddings, reference_captions
    
    if len(files) != len(captions):
        raise HTTPException(
            status_code=400, 
            detail="Number of files must match number of captions"
        )
    
    try:
        reference_embeddings = []
        reference_captions = []
        
        for file, caption in zip(files, captions):
            # Read and preprocess image
            image_bytes = await file.read()
            image = preprocess_image(image_bytes)
            
            # Compute embedding
            embedding = compute_clip_embedding(image)
            
            reference_embeddings.append(embedding)
            reference_captions.append(caption)
        
        logger.info(f"Uploaded {len(reference_embeddings)} reference images")
        
        return JSONResponse({
            "status": "success",
            "count": len(reference_embeddings),
            "message": f"Successfully uploaded {len(reference_embeddings)} reference images"
        })
        
    except Exception as e:
        logger.error(f"Error uploading references: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/classify")
async def classify_image(file: UploadFile = File(...)):
    """
    Classify a new image as 'Rare Event' or 'Normal'
    """
    if not reference_embeddings:
        raise HTTPException(
            status_code=400,
            detail="No reference images uploaded. Please upload references first."
        )
    
    try:
        # Read and preprocess image
        image_bytes = await file.read()
        image = preprocess_image(image_bytes)
        
        # Compute embedding for the new image
        new_embedding = compute_clip_embedding(image)
        
        # Compute similarities with all reference images
        similarities = []
        for ref_embedding in reference_embeddings:
            similarity = compute_similarity(new_embedding, ref_embedding)
            similarities.append(similarity)
        
        # Get the maximum similarity
        max_similarity = max(similarities)
        
        # Classification threshold (you can adjust this)
        threshold = 0.7
        
        if max_similarity > threshold:
            label = "Rare Event"
        else:
            label = "Normal"
        
        return JSONResponse({
            "label": label,
            "similarity": float(max_similarity),
            "all_similarities": [float(s) for s in similarities]
        })
        
    except Exception as e:
        logger.error(f"Error classifying image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/describe")
async def describe_image(file: UploadFile = File(...)):
    """
    Generate a descriptive caption for an uploaded image
    """
    try:
        # Read and preprocess image
        image_bytes = await file.read()
        image = preprocess_image(image_bytes)
        
        # Generate caption using BLIP
        inputs = blip_processor(image, return_tensors="pt").to(device)
        
        with torch.no_grad():
            out = blip_model.generate(**inputs, max_length=50, num_beams=5)
        
        description = blip_processor.decode(out[0], skip_special_tokens=True)
        
        return JSONResponse({
            "description": description
        })
        
    except Exception as e:
        logger.error(f"Error describing image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
async def generate_image(caption: str = Form(...)):
    """
    Generate a synthetic image based on a text caption
    """
    try:
        # Generate image using Stable Diffusion
        with torch.no_grad():
            result = sd_pipeline(
                caption,
                num_inference_steps=20,
                guidance_scale=7.5,
                height=512,
                width=512
            )
        
        generated_image = result.images[0]
        
        # Convert to base64
        buffer = io.BytesIO()
        generated_image.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return JSONResponse({
            "image": f"data:image/png;base64,{img_base64}",
            "caption": caption
        })
        
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({
        "status": "healthy",
        "device": str(device),
        "models_loaded": {
            "clip": clip_model is not None,
            "blip": blip_model is not None,
            "stable_diffusion": sd_pipeline is not None
        },
        "reference_count": len(reference_embeddings)
    })

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return JSONResponse({
        "message": "Rare Event Detection API",
        "version": "1.0.0",
        "endpoints": [
            "/upload_references - POST: Upload reference images with captions",
            "/classify - POST: Classify an image as Rare Event or Normal",
            "/describe - POST: Generate description for an image",
            "/generate - POST: Generate synthetic image from caption",
            "/health - GET: Health check"
        ]
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)