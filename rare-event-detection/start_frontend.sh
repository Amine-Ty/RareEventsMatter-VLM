#!/bin/bash

# Rare Event Detection Frontend Startup Script

echo "🌐 Starting Rare Event Detection Frontend"
echo "========================================="

# Check if we're in the right directory
if [ ! -f "index.html" ]; then
    echo "❌ Error: index.html not found. Please run this script from the frontend directory."
    exit 1
fi

echo "🔧 Starting local web server..."
echo ""
echo "✅ Frontend available at:"
echo "   - http://localhost:3000"
echo ""
echo "📝 Make sure the backend is running at:"
echo "   - http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Try different methods to start a web server
if command -v python3 &> /dev/null; then
    echo "🐍 Using Python 3 built-in server..."
    python3 -m http.server 3000
elif command -v python &> /dev/null; then
    echo "🐍 Using Python built-in server..."
    python -m http.server 3000
elif command -v npx &> /dev/null; then
    echo "📦 Using npx http-server..."
    npx http-server -p 3000
else
    echo "❌ No suitable web server found."
    echo "Please install Python or Node.js, or open index.html directly in your browser."
    echo ""
    echo "Alternative: Open index.html directly in your browser:"
    echo "file://$(pwd)/index.html"
fi