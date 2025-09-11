# Rare Event Detection with Few-Shot Multimodal AI

A full-stack application for detecting rare events using few-shot learning with multimodal AI.

> **Note:** In this project, multiple LLM APIs were used because GPT API access was unavailable. The intended design is to rely on **a single multimodal VLM API (e.g., GPT-5)** for all tasks.

## 🚀 Key Features

- **Few-Shot Learning**: Train the model with 4 reference images and captions.
- **Binary Classification**: Detect "Rare Event" vs "Normal" images.
- **Image Interpretation**: Generate descriptive captions for uploaded images.
- **Synthetic Image Generation**: Create rare event images from text prompts.
- **Modern UI**: Responsive interface built with HTML, Tailwind CSS, and Vanilla JS.
- **Adaptive Backend**: Supports GPU acceleration with automatic fallback to CPU.

## 🏧 Architecture

### Backend (FastAPI)
- **VLM API (GPT-5, intended)**: Handles multimodal tasks including classification, description, and synthetic generation.
- **Demonstration Setup**: Multiple LLM APIs were used to illustrate the architecture concept.
- **FastAPI**: REST API with auto-generated documentation.

### Frontend
- **HTML/CSS/JS with Tailwind**: Clean, responsive UI.
- **Drag & Drop Upload**: Intuitive reference and new image uploads.
- **API Communication**: Frontend interacts with backend for all operations.

## 📋 Requirements

- Python 3.8+
- CUDA-compatible GPU (optional)
- 8GB+ RAM (16GB+ recommended for GPU usage)
- 10GB+ free disk space

### Python Dependencies
All listed in `backend/requirements.txt`:
- FastAPI, Uvicorn
- PyTorch & Transformers
- Diffusers
- Pillow, NumPy, OpenCV

## 🛠️ Installation & Setup

### 1. Clone Project
```bash
git clone <repo_url>
cd rare-event-detection
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# Activate
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### 3. Start Backend
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
> First run downloads models (~5GB).

### 4. Start Frontend
```bash
cd frontend
python -m http.server 3000
# OR Node.js
npx http-server -p 3000
# OR open index.html directly
```

### 5. Access
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🎯 Usage

1. **Upload Reference Images** – 4 images with captions.
2. **Classify New Images** – Get predictions and confidence scores.
3. **Describe Images** – Generate AI captions.
4. **Generate Synthetic Images** – Create rare event images from text.

## 🛠️ API Endpoints

- **Health Check**: `GET /health`
- **Upload References**: `POST /upload_references`
- **Classify Image**: `POST /classify`
- **Describe Image**: `POST /describe`
- **Generate Image**: `POST /generate`

## ⚙️ Configuration

- **Classification Threshold**: `backend/app.py`, `threshold = 0.7`
- **Stable Diffusion Generation**: Adjust `num_inference_steps`, `guidance_scale`, `height`, `width`

## 🔬 Technical Notes

- **Few-Shot Learning**: Reference images encoded and compared with new images using similarity.
- **Intended Architecture**: Single VLM API (GPT-5) for all multimodal tasks.
- **Demonstration Setup**: Multiple LLM APIs used due to GPT API unavailability.

## 🤝 Contributing

Hackathon project. Contributions and improvements are welcome.

---

**Happy Hacking! 🚀**

