"""
Sample usage of the Text/Photo to 3D Model Converter.
This script demonstrates how to use the converter with both text and images.
"""

from text_photo_to_3d import TextPhotoTo3D
import os
from pathlib import Path

# Create samples directory if it doesn't exist
Path("samples").mkdir(exist_ok=True)

def main():
    # Initialize the converter
    converter = TextPhotoTo3D()
    
    # Example 1: Generate from text
    print("\n=== Example 1: Generate from text ===")
    text_prompt = "A simple coffee mug"
    obj_path, stl_path = converter.generate_from_text(
        text_prompt, 
        output_path="output/text_example"
    )
    viz_path = converter.visualize_model(obj_path)
    
    # Example 2: Generate from image (if available)
    # You would need to provide your own image or download one
    # For demonstration purposes, we'll check if a sample image exists
    sample_image = "samples/sample_chair.jpg"
    
    if os.path.exists(sample_image):
        print("\n=== Example 2: Generate from image ===")
        obj_path, stl_path = converter.generate_from_image(
            sample_image, 
            output_path="output/image_example"
        )
        viz_path = converter.visualize_model(obj_path)
    else:
        print(f"\nSkipping image example as {sample_image} does not exist.")
        print("To test with an image, place an image at this path or modify the script.")
    
    print("\nExamples completed. Check the 'output' directory for results.")

if __name__ == "__main__":
    main() 