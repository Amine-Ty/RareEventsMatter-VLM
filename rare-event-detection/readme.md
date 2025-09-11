![Synergy Quote](https://www.azquotes.com/picture-quotes/quote-the-word-synergy-comes-from-the-greek-sin-ergo-meaning-to-work-together-it-describes-r-buckminster-fuller-114-14-41.jpg)


# Rare Event Detection with Few-Shot Multimodal AI

A full-stack application for detecting rare events using few-shot learning with multimodal AI.

> **Note:** In this project, multiple LLM APIs were used because GPT API access was inaccessible. The intended design is to rely on **a single multimodal VLM API (e.g., GPT-5)** for all tasks.

---

## 📄 Abstract
This project addresses the challenge of detecting rare events—such as rare diseases—where data scarcity and long diagnostic delays hinder progress. Traditional AI struggles in these cases due to small, imbalanced datasets and lack of interpretability. Our solution leverages few-shot multimodal learning, combining just a handful of reference images and captions to enable classification, interpretation, and synthetic data generation. This approach demonstrates how modern vision-language models can work with minimal data, with potential impact in accelerating early detection, enriching datasets with synthetic samples, and reducing the diagnostic gap for rare conditions.

---

## 📚 Background
Rare events are inherently difficult to detect because of limited examples and significant data imbalance. This creates a barrier to training effective AI systems. While conventional machine learning requires large datasets, multimodal models offer the opportunity to learn from much smaller samples by combining image and text representations.

---

## ❗ Problem Statement
- **Data Scarcity**: Rare events lack sufficient labeled data for traditional supervised learning.
- **Slow Diagnostics**: Rare diseases and similar conditions often face long delays in identification.
- **AI Limitations**: Standard models fail to generalize with small, imbalanced datasets.

---

## 🌍 Impact
- **Early Detection**: Enables detection of rare conditions with minimal examples.
- **Synthetic Data Generation**: Enriches training datasets with synthetic images.
- **Diagnostic Acceleration**: Reduces delays by providing interpretable AI-driven insights.
- **Broader Applications**: Applicable to healthcare, disaster detection, and other rare event domains.

---

## 📦 Deliverables
- **Backend (FastAPI)** with endpoints for classification, description, and synthetic image generation.
- **Frontend (HTML/CSS/JS with Tailwind)** providing an interactive user interface.
- **Few-Shot Learning Pipeline** leveraging multimodal embeddings.
- **Documentation & Usage Guide** including installation, configuration, and troubleshooting.

---

## 🚀 Features
- **Few-Shot Learning**: Train the model with 4 reference images and captions.
- **Binary Classification**: Detect "Rare Event" vs "Normal" images.
- **Image Interpretation**: Generate descriptive captions for uploaded images.
- **Synthetic Image Generation**: Create rare event images from text prompts.
- **Modern UI**: Responsive interface built with HTML, Tailwind CSS, and Vanilla JS.
- **Adaptive Backend**: Supports GPU acceleration with automatic fallback to CPU.

---

## 🏗️ Architecture

### Backend (FastAPI)
- **VLM API (GPT-5, intended)**: Handles multimodal tasks including classification, description, and synthetic generation.
- **Demonstration Setup**: Multiple LLM APIs were used to illustrate the architecture concept.
- **FastAPI**: REST API with auto-generated documentation.

### Frontend
- **HTML/CSS/JS with Tailwind**: Clean, responsive UI.
- **Drag & Drop Upload**: Intuitive reference and new image uploads.
- **API Communication**: Frontend interacts with backend for all operations.

---

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

---

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

---

## 🎯 Step-by-Step Usage

### Step 1: Upload Reference Images
- Upload 4 images representing rare events.
- Add captions for each.
- Click **Upload** to train the few-shot model.

### Step 2: Classify New Images
- Upload a new image.
- Click **Classify**.
- View prediction (Rare Event vs Normal) and confidence scores.

### Step 3: Describe Images
- Upload or select an image.
- Click **Describe**.
- View AI-generated captions.

### Step 4: Generate Synthetic Images
- Enter a text prompt.
- Click **Generate**.
- View synthetic image output.

---

## 🔧 API Endpoints
- **Health Check**: `GET /health`
- **Upload References**: `POST /upload_references`
- **Classify Image**: `POST /classify`
- **Describe Image**: `POST /describe`
- **Generate Image**: `POST /generate`

---

## ⚙️ Configuration
- **Classification Threshold**: `backend/app.py`, `threshold = 0.7`
- **Stable Diffusion Generation**: Adjust `num_inference_steps`, `guidance_scale`, `height`, `width`

---

## 🔬 Technical Notes
- **Few-Shot Learning**: Reference images encoded and compared with new images using similarity.
- **Intended Architecture**: Single VLM API (GPT-5) for all multimodal tasks.
- **Demonstration Setup**: Multiple LLM APIs used due to GPT API unavailability.

> **Note:** In this project, multiple LLM APIs were used because GPT API access was unavailable. The intended design is to rely on a single multimodal VLM API (e.g., GPT-5) for all tasks.

---

## 🤝 Contributing
Hackathon project. Contributions and improvements are welcome.

---

**Happy Hacking! 🚀**

