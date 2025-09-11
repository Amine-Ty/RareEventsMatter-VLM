# 🚀 Quick Start Guide

## 📁 Project Structure
```
rare-event-detection/
├── README.md              # Comprehensive documentation
├── QUICK_START.md         # This quick start guide
├── test_backend.py        # Backend testing script
├── start_backend.sh       # Backend startup script
├── start_frontend.sh      # Frontend startup script
├── backend/
│   ├── app.py            # FastAPI application
│   └── requirements.txt  # Python dependencies
└── frontend/
    ├── index.html        # Main web interface
    ├── script.js         # Frontend JavaScript
    └── package.json      # Node.js dependencies
```

## ⚡ Quick Setup (2 minutes)

### 1. Start Backend
```bash
cd rare-event-detection/backend
./start_backend.sh
```
**Note**: First run will download AI models (~6GB) - this takes 5-10 minutes.

### 2. Start Frontend (New Terminal)
```bash
cd rare-event-detection/frontend
./start_frontend.sh
```

### 3. Open Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🎯 How to Use

### Step 1: Upload Reference Images
1. Upload 4 images that represent "rare events"
2. Add descriptive captions for each
3. Click "Upload Reference Images"

### Step 2: Test Classification
1. Upload a test image
2. Click "Classify Image" → Get "Rare Event" or "Normal"
3. Click "Describe Image" → Get AI-generated description

### Step 3: Generate Synthetic Images
1. Enter a text description (e.g., "A rare purple lightning storm")
2. Click "Generate" → AI creates a synthetic image

## 🧪 Test the Backend
```bash
cd rare-event-detection
python test_backend.py
```

## 🔧 Manual Setup (Alternative)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
python -m http.server 3000
# OR: npx http-server -p 3000
# OR: Open index.html directly in browser
```

## 📊 Example API Usage

### Upload References
```bash
curl -X POST "http://localhost:8000/upload_references" \
  -F "files=@image1.jpg" -F "files=@image2.jpg" \
  -F "files=@image3.jpg" -F "files=@image4.jpg" \
  -F "captions=Fire spreading" -F "captions=Severe flood" \
  -F "captions=Lightning storm" -F "captions=Volcanic eruption"
```

### Classify Image
```bash
curl -X POST "http://localhost:8000/classify" -F "file=@test.jpg"
```

### Generate Image
```bash
curl -X POST "http://localhost:8000/generate" -F "caption=A rare meteor shower"
```

## 🐛 Troubleshooting

**Backend won't start?**
- Check Python 3.8+ is installed
- Ensure 10GB+ free disk space for models
- Try: `pip install --upgrade pip`

**Frontend can't connect?**
- Ensure backend is running on port 8000
- Check firewall settings
- Try opening index.html directly

**Models downloading slowly?**
- This is normal on first run
- Models are cached after first download
- Stable internet connection required

**Out of memory errors?**
- Close other applications
- System will automatically fallback to CPU
- Consider using smaller batch sizes

## 🎉 You're Ready!

Your hackathon project is now running! The system uses:
- **CLIP** for image similarity and classification
- **BLIP** for image-to-text description
- **Stable Diffusion** for synthetic image generation

Perfect for demonstrating few-shot multimodal AI capabilities!

---
**Need help?** Check the full README.md for detailed documentation.