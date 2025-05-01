"""
Demo script to show how to use the image-to-3D feature.
This script creates a simple sample image and uses it as input.
"""

import os
import numpy as np
from PIL import Image, ImageDraw
from pathlib import Path
from simple_3d_demo import SimpleDemoGenerator

def create_sample_image(output_path, shape_type="car"):
    """Create a simple sample image with a shape."""
    # Create blank image
    img = Image.new('RGB', (400, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw different shapes based on type
    if shape_type == "car":
        # Draw a simple car silhouette
        # Car body
        draw.rectangle([100, 200, 300, 250], fill=(200, 0, 0))
        # Car top
        draw.rectangle([150, 150, 250, 200], fill=(200, 0, 0))
        # Wheels
        draw.ellipse([110, 240, 150, 280], fill=(0, 0, 0))
        draw.ellipse([250, 240, 290, 280], fill=(0, 0, 0))
        # Windows
        draw.rectangle([160, 160, 240, 190], fill=(200, 200, 255))
    elif shape_type == "mug":
        # Draw a simple mug silhouette
        # Cup body
        draw.rectangle([150, 100, 250, 250], fill=(0, 100, 200))
        # Handle
        draw.rectangle([250, 140, 280, 210], fill=(0, 100, 200))
    elif shape_type == "sphere":
        # Draw a circle
        draw.ellipse([100, 100, 300, 300], fill=(100, 200, 100))
    else:
        # Default - draw a box
        draw.rectangle([100, 100, 300, 300], fill=(150, 150, 150))
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save image
    img.save(output_path)
    print(f"Created sample image: {output_path}")
    return output_path

def main():
    # Create samples directory
    Path("samples").mkdir(exist_ok=True)
    
    # Create different sample images
    car_img = create_sample_image("samples/sample_car.jpg", "car")
    mug_img = create_sample_image("samples/sample_mug.jpg", "mug")
    sphere_img = create_sample_image("samples/sample_sphere.jpg", "sphere")
    
    # Initialize generator
    generator = SimpleDemoGenerator()
    
    # Generate 3D models from our sample images
    print("\n=== Generating 3D model from car image ===")
    car_obj, car_stl = generator.generate_from_image(car_img, "output/image_car")
    generator.visualize_model(car_obj)
    
    print("\n=== Generating 3D model from mug image ===")
    mug_obj, mug_stl = generator.generate_from_image(mug_img, "output/image_mug")
    generator.visualize_model(mug_obj)
    
    print("\n=== Generating 3D model from sphere image ===")
    sphere_obj, sphere_stl = generator.generate_from_image(sphere_img, "output/image_sphere")
    generator.visualize_model(sphere_obj)
    
    print("\nAll models generated. Check the 'output' directory for the results.")

if __name__ == "__main__":
    main() 