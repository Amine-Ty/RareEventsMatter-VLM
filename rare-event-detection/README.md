# Rare Event Detection with Few-Shot Multimodal AI

A full-stack application for detecting rare events using few-shot learning with multimodal AI models (CLIP, BLIP, Stable Diffusion).

## 🚀 Features

- **Few-Shot Learning**: Upload 4 reference images with captions to train the model
- **Binary Classification**: Classify new images as "Rare Event" or "Normal" with confidence scores
- **Image Interpretation**: Generate descriptive captions for uploaded images using BLIP
- **Synthetic Generation**: Create synthetic rare event images from text descriptions using Stable Diffusion
- **Modern UI**: Clean, responsive web interface built with HTML/CSS/JavaScript and Tailwind CSS
- **GPU/CPU Support**: Automatic fallback from GPU to CPU based on availability

## 🏗️ Architecture

### Backend (FastAPI)
- **CLIP** (openai/clip-vit-base-patch32): For image embeddings and similarity computation
- **BLIP** (Salesforce/blip-image-captioning-base): For image-to-text interpretation
- **Stable Diffusion v1-5** (runwayml/stable-diffusion-v1-5): For synthetic image generation
- **FastAPI**: REST API with automatic documentation

### Frontend (HTML/CSS/JavaScript)
- **Tailwind CSS**: For modern, responsive styling
- **Vanilla JavaScript**: For API interactions and UI management
- **Drag & Drop**: Intuitive file upload interface

## 📋 Requirements

### System Requirements
- Python 3.8+
- CUDA-compatible GPU (optional, will fallback to CPU)
- 8GB+ RAM (16GB+ recommended for GPU usage)
- 10GB+ free disk space (for model downloads)

### Python Dependencies
All dependencies are listed in `backend/requirements.txt`:
- FastAPI & Uvicorn
- PyTorch & Torchvision
- Transformers (Hugging Face)
- Diffusers
- Pillow, NumPy, OpenCV

## 🛠️ Installation & Setup

### 1. Clone/Download the Project
```bash
# If you have the project files
cd rare-event-detection
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start the Backend Server
```bash
# From the backend directory
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The backend will start downloading models on first run (this may take 5-10 minutes):
- CLIP model (~600MB)
- BLIP model (~1GB)
- Stable Diffusion model (~4GB)

### 4. Start the Frontend
```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Option 1: Use Python's built-in server
python -m http.server 3000

# Option 2: Use Node.js http-server (if installed)
npx http-server -p 3000

# Option 3: Simply open index.html in your browser
```

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🎯 Usage Guide

### Step 1: Upload Reference Images
1. Upload 4 reference images that represent "rare events"
2. Add descriptive captions for each image
3. Click "Upload Reference Images" to train the few-shot model

### Step 2: Classify New Images
1. Upload a new image in the "Classify New Image" section
2. Click "Classify Image" to get a prediction ("Rare Event" or "Normal")
3. View the confidence score and similarity metrics

### Step 3: Interpret Images
1. Use the same uploaded image or upload a new one
2. Click "Describe Image" to generate a descriptive caption
3. View the AI-generated description

### Step 4: Generate Synthetic Images
1. Enter a text description in the generation section
2. Click "Generate" to create a synthetic image
3. View the generated image based on your caption

## 🔧 API Endpoints

### Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

### Upload Reference Images
```bash
curl -X POST "http://localhost:8000/upload_references" \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg" \
  -F "files=@image3.jpg" \
  -F "files=@image4.jpg" \
  -F "captions=Volcanic eruption with red lava" \
  -F "captions=Tornado touching down in field" \
  -F "captions=Massive wildfire spreading" \
  -F "captions=Severe flooding in city"
```

### Classify Image
```bash
curl -X POST "http://localhost:8000/classify" \
  -F "file=@test_image.jpg"
```

### Describe Image
```bash
curl -X POST "http://localhost:8000/describe" \
  -F "file=@test_image.jpg"
```

### Generate Synthetic Image
```bash
curl -X POST "http://localhost:8000/generate" \
  -F "caption=A rare purple lightning storm over mountains"
```

## 📊 Example API Responses

### Classification Response
```json
{
  "label": "Rare Event",
  "similarity": 0.8234,
  "all_similarities": [0.8234, 0.7123, 0.6789, 0.5432]
}
```

### Description Response
```json
{
  "description": "a large volcano erupting with lava and smoke"
}
```

### Generation Response
```json
{
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "caption": "A rare purple lightning storm over mountains"
}
```

## ⚙️ Configuration

### Adjusting Classification Threshold
Edit `backend/app.py` line ~150:
```python
threshold = 0.7  # Adjust between 0.0-1.0
```

### Changing Model Parameters
For Stable Diffusion generation, modify parameters in `backend/app.py`:
```python
result = sd_pipeline(
    caption,
    num_inference_steps=20,    # Increase for better quality
    guidance_scale=7.5,        # Adjust creativity vs accuracy
    height=512,                # Image dimensions
    width=512
)
```

## 🐛 Troubleshooting

### Common Issues

1. **Models not downloading**
   - Ensure stable internet connection
   - Check available disk space (10GB+ needed)
   - Try restarting the backend server

2. **CUDA out of memory**
   - Reduce batch size or use CPU mode
   - Close other GPU-intensive applications
   - The system will automatically fallback to CPU

3. **Frontend can't connect to backend**
   - Ensure backend is running on port 8000
   - Check CORS settings in `backend/app.py`
   - Verify firewall settings

4. **Slow image generation**
   - This is normal for CPU mode (2-5 minutes)
   - GPU mode is much faster (10-30 seconds)
   - Consider reducing inference steps for faster generation

### Performance Tips

- **GPU Usage**: Ensure CUDA is properly installed for faster inference
- **Memory**: Close unnecessary applications to free up RAM
- **Storage**: Use SSD for faster model loading
- **Network**: Stable internet connection for initial model downloads

## 🔬 Technical Details

### Model Information
- **CLIP**: Used for computing image embeddings and similarity scores
- **BLIP**: Generates natural language descriptions of images
- **Stable Diffusion**: Creates synthetic images from text prompts

### Few-Shot Learning Approach
1. Reference images are encoded using CLIP
2. New images are compared against reference embeddings
3. Cosine similarity determines classification
4. Threshold-based binary classification (Rare Event vs Normal)

### Security Considerations
- CORS is enabled for all origins (development only)
- No authentication implemented (add for production)
- File uploads are processed in memory (consider disk storage for production)

## 📝 Development Notes

### Adding New Features
- Extend API endpoints in `backend/app.py`
- Add corresponding frontend functions in `frontend/script.js`
- Update UI components in `frontend/index.html`

### Model Customization
- Replace model names in `load_models()` function
- Adjust preprocessing in `preprocess_image()` function
- Modify similarity computation in `compute_similarity()` function

## 📄 License

This project is created for hackathon purposes. Feel free to use and modify as needed.

## 🤝 Contributing

This is a hackathon project, but contributions and improvements are welcome!

---

**Happy Hacking! 🚀**