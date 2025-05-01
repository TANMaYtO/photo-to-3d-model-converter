#!/bin/bash

echo "Setting up the Photo/Text to 3D Model Converter environment..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies (this may take a while)..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p output
mkdir -p samples

echo
echo "Setup complete!"
echo
echo "To generate a 3D model from text:"
echo "python text_photo_to_3d.py --text \"A small toy car\""
echo
echo "To generate a 3D model from an image:"
echo "python text_photo_to_3d.py --image path/to/your/image.jpg"
echo
echo "To run the sample script:"
echo "python sample_usage.py"
echo 