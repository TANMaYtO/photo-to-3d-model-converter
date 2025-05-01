import os
import argparse
import numpy as np
import trimesh
import matplotlib.pyplot as plt
from pathlib import Path

class SimpleDemoGenerator:
    """
    A simplified demo that creates basic 3D shapes based on text prompts
    without requiring large model downloads.
    """

    def __init__(self):
        # Create output directory
        Path("output").mkdir(exist_ok=True)
        print("Initialized SimpleDemoGenerator")
    
    def generate_from_text(self, text_prompt, output_path=None):
        """Generate a simple 3D model based on text prompt keywords."""
        print(f"Generating simple 3D model from text prompt: '{text_prompt}'")
        
        # Simplified rules-based approach
        text_lower = text_prompt.lower()
        
        # Choose shape based on keywords
        if any(word in text_lower for word in ["sphere", "ball", "round"]):
            mesh = trimesh.creation.icosphere(subdivisions=3, radius=1.0)
        elif any(word in text_lower for word in ["cube", "box", "square"]):
            mesh = trimesh.creation.box(extents=[1, 1, 1])
        elif any(word in text_lower for word in ["cylinder", "tube"]):
            mesh = trimesh.creation.cylinder(radius=0.5, height=1.0)
        elif any(word in text_lower for word in ["cone"]):
            mesh = trimesh.creation.cone(radius=0.5, height=1.0)
        elif any(word in text_lower for word in ["mug", "cup", "glass"]):
            # Create a simple cup shape using multiple primitives
            bottom = trimesh.creation.cylinder(radius=0.5, height=0.1)
            
            # Side wall - just use a cylinder for simplicity
            side = trimesh.creation.cylinder(radius=0.5, height=0.9)
            side.vertices[:, 2] += 0.1  # Move up
            
            # Handle - use a simple cylinder
            handle = trimesh.creation.cylinder(radius=0.05, height=0.4)
            # Rotate the handle using rotation matrix
            rotation = trimesh.transformations.rotation_matrix(np.radians(90), [1, 0, 0])
            handle.apply_transform(rotation)
            # Move the handle to the side of the cup
            handle.vertices[:, 0] += 0.5  # Move to the side
            handle.vertices[:, 2] += 0.5  # Move up
            
            # Combine all parts
            mesh = trimesh.util.concatenate([bottom, side, handle])
        elif any(word in text_lower for word in ["car", "auto", "vehicle"]):
            # Create a simple car shape
            body = trimesh.creation.box(extents=[2.0, 1.0, 0.5])
            body.vertices[:, 2] += 0.25  # Move up
            
            # Add a cabin on top
            cabin = trimesh.creation.box(extents=[1.0, 0.8, 0.4])
            cabin.vertices[:, 2] += 0.7  # Move up
            
            # Add wheels
            wheel1 = trimesh.creation.cylinder(radius=0.25, height=0.1, sections=16)
            rotation = trimesh.transformations.rotation_matrix(np.radians(90), [0, 1, 0])
            wheel1.apply_transform(rotation)
            wheel1.vertices[:, 0] += 0.5  # Move x
            wheel1.vertices[:, 1] += 0.5  # Move y
            wheel1.vertices[:, 2] += 0.25  # Move z
            
            wheel2 = trimesh.creation.cylinder(radius=0.25, height=0.1, sections=16)
            wheel2.apply_transform(rotation)
            wheel2.vertices[:, 0] += 0.5  # Move x
            wheel2.vertices[:, 1] -= 0.5  # Move y
            wheel2.vertices[:, 2] += 0.25  # Move z
            
            wheel3 = trimesh.creation.cylinder(radius=0.25, height=0.1, sections=16)
            wheel3.apply_transform(rotation)
            wheel3.vertices[:, 0] -= 0.5  # Move x
            wheel3.vertices[:, 1] += 0.5  # Move y
            wheel3.vertices[:, 2] += 0.25  # Move z
            
            wheel4 = trimesh.creation.cylinder(radius=0.25, height=0.1, sections=16)
            wheel4.apply_transform(rotation)
            wheel4.vertices[:, 0] -= 0.5  # Move x
            wheel4.vertices[:, 1] -= 0.5  # Move y
            wheel4.vertices[:, 2] += 0.25  # Move z
            
            mesh = trimesh.util.concatenate([body, cabin, wheel1, wheel2, wheel3, wheel4])
        else:
            # Default to a basic shape
            mesh = trimesh.creation.box(extents=[1, 1, 1])
        
        # Create default output path if none provided
        if output_path is None:
            name_base = text_prompt.replace(' ', '_')
            output_path = f"output/{name_base}"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save as obj
        obj_path = f"{output_path}.obj"
        mesh.export(obj_path)
        
        # Save as stl
        stl_path = f"{output_path}.stl"
        mesh.export(stl_path)
        
        print(f"Models saved to {obj_path} and {stl_path}")
        return obj_path, stl_path
    
    def generate_from_image(self, image_path, output_path=None):
        """Generate a simple 3D model based on the image filename as a fallback."""
        print(f"Simulating 3D model generation from image: {image_path}")
        
        # In a real implementation, we would analyze the image
        # For this demo, we'll use the filename as text input
        base_name = os.path.basename(image_path).split('.')[0]
        print(f"Using filename as fallback prompt: {base_name}")
        
        return self.generate_from_text(base_name, output_path)
    
    def visualize_model(self, obj_path):
        """Visualize the generated 3D model using matplotlib."""
        # Load the mesh with trimesh
        mesh = trimesh.load(obj_path)
        
        # Create a new figure
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Get mesh data
        vertices = mesh.vertices
        faces = mesh.faces
        
        # Plot the mesh
        ax.plot_trisurf(vertices[:, 0], vertices[:, 1], vertices[:, 2], 
                       triangles=faces, alpha=0.5, color='blue')
        
        # Set labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Model: {obj_path}')
        
        # Set equal aspect ratio
        ax.set_box_aspect([1, 1, 1])
        
        # Show the plot
        plt.tight_layout()
        
        # Save visualization
        viz_path = obj_path.replace('.obj', '_viz.png')
        plt.savefig(viz_path)
        plt.close()
        
        print(f"Visualization saved to {viz_path}")
        return viz_path


def main():
    parser = argparse.ArgumentParser(description="Generate simple 3D models from text or images (demo).")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--text', type=str, help='Text prompt for 3D model generation')
    input_group.add_argument('--image', type=str, help='Path to input image for 3D model generation')
    parser.add_argument('--output', type=str, help='Path for output files (without extension)')
    parser.add_argument('--no-viz', action='store_true', help='Skip visualization')
    
    args = parser.parse_args()
    
    # Initialize the generator
    generator = SimpleDemoGenerator()
    
    # Generate 3D model based on input type
    if args.text:
        obj_path, stl_path = generator.generate_from_text(args.text, args.output)
    else:
        obj_path, stl_path = generator.generate_from_image(args.image, args.output)
    
    # Visualize if not disabled
    if not args.no_viz:
        viz_path = generator.visualize_model(obj_path)
        print(f"Complete! Generated files: {obj_path}, {stl_path}, {viz_path}")
    else:
        print(f"Complete! Generated files: {obj_path}, {stl_path}")


if __name__ == "__main__":
    main() 