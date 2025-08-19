#!/bin/bash

# Run Classification Validation App Launcher
# This script installs dependencies and launches the Streamlit app

echo "🎯 Starting Run Classification Validation App..."

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.8 or higher."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if installation was successful
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Please check your Python environment."
    exit 1
fi

# Launch the app
echo "🚀 Launching Streamlit app..."
echo "📋 Open your browser to: http://localhost:8501"
echo "⚡ Use Ctrl+C to stop the app"
echo ""

streamlit run app.py