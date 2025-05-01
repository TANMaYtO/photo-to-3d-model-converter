"""
Simple 3D model viewer for generated models.
This script opens and displays .obj or .stl files in a simple viewer.
"""

import argparse
import trimesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def view_model(model_path):
    """View a 3D model using matplotlib."""
    # Load the mesh
    try:
        mesh = trimesh.load(model_path)
        print(f"Loaded model: {model_path}")
        print(f"Vertices: {len(mesh.vertices)}, Faces: {len(mesh.faces)}")
    except Exception as e:
        print(f"Error loading model: {e}")
        return
    
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
    ax.set_title(f'Model: {model_path}')
    
    # Set equal aspect ratio
    ax.set_box_aspect([1, 1, 1])
    
    # Show the plot
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="View 3D models (.obj or .stl files).")
    parser.add_argument('model_path', type=str, help='Path to the 3D model file (.obj or .stl)')
    
    args = parser.parse_args()
    view_model(args.model_path)

if __name__ == "__main__":
    main() 