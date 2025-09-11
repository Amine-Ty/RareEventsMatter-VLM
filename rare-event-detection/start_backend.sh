#!/bin/bash

# Rare Event Detection Backend Startup Script

echo "🚀 Starting Rare Event Detection Backend"
echo "========================================"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the backend directory."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🔥 Starting FastAPI server..."
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "⚠️  Note: Models will download on first run (may take 5-10 minutes)"
echo "   - CLIP model (~600MB)"
echo "   - BLIP model (~1GB)" 
echo "   - Stable Diffusion model (~4GB)"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
uvicorn app:app --reload --host 0.0.0.0 --port 8000