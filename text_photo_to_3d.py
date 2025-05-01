import os
import sys
import argparse
import numpy as np
import torch
from PIL import Image
import trimesh
import matplotlib.pyplot as plt
from pathlib import Path
import shap_e.util.notebooks
from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import create_pan_cameras, decode_latent_mesh, gif_widget
from shap_e.util.image_util import load_image


class TextPhotoTo3D:
    def __init__(self, device=None):
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = device
        
        print(f"Using device: {self.device}")
        
        # Load models
        self.xm = load_model('transmitter', self.device)
        self.model = load_model('text300M', self.device)
        self.diffusion = diffusion_from_config(load_config('diffusion'))
        
        # Create output directory
        Path("output").mkdir(exist_ok=True)
    
    def generate_from_text(self, text_prompt, output_path=None, batch_size=4):
        """Generate a 3D model from a text prompt."""
        print(f"Generating 3D model from text prompt: '{text_prompt}'")
        
        # Generate latents from text conditioning
        latents = sample_latents(
            batch_size=batch_size,
            model=self.model,
            diffusion=self.diffusion,
            guidance_scale=15.0,
            model_kwargs=dict(texts=[text_prompt] * batch_size),
            progress=True,
            clip_denoised=True,
            use_fp16=True,
            use_karras=True,
            karras_steps=64,
            sigma_min=1e-3,
            sigma_max=160,
            s_churn=0,
        )
        
        return self._process_latents(latents, text_prompt, output_path)
    
    def generate_from_image(self, image_path, output_path=None, batch_size=4):
        """Generate a 3D model from an image."""
        print(f"Generating 3D model from image: {image_path}")
        
        # Load and preprocess the image
        image = load_image(image_path)
        
        # Generate latents from image conditioning
        latents = sample_latents(
            batch_size=batch_size,
            model=self.xm,
            diffusion=self.diffusion,
            guidance_scale=3.0,
            model_kwargs=dict(images=[image] * batch_size),
            progress=True,
            clip_denoised=True,
            use_fp16=True,
            use_karras=True,
            karras_steps=64,
            sigma_min=1e-3,
            sigma_max=160,
            s_churn=0,
        )
        
        base_name = os.path.basename(image_path).split('.')[0]
        return self._process_latents(latents, base_name, output_path)
    
    def _process_latents(self, latents, name_base, output_path=None):
        """Process latents to create 3D models."""
        # Create default output path if none provided
        if output_path is None:
            name_base = name_base.replace(' ', '_')
            output_path = f"output/{name_base}"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # We'll use the first latent (best result)
        latent = latents[0]
        
        # Create mesh
        mesh = decode_latent_mesh(self.xm, latent)
        
        # Save as obj
        obj_path = f"{output_path}.obj"
        mesh_obj = mesh.tri_mesh()
        mesh_obj.write_obj(obj_path)
        
        # Save as stl
        stl_path = f"{output_path}.stl"
        mesh_trimesh = trimesh.Trimesh(
            vertices=mesh_obj.verts, 
            faces=mesh_obj.faces, 
            vertex_normals=mesh_obj.normals
        )
        mesh_trimesh.export(stl_path)
        
        print(f"Models saved to {obj_path} and {stl_path}")
        return obj_path, stl_path
    
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
    parser = argparse.ArgumentParser(description="Generate 3D models from text or images.")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--text', type=str, help='Text prompt for 3D model generation')
    input_group.add_argument('--image', type=str, help='Path to input image for 3D model generation')
    parser.add_argument('--output', type=str, help='Path for output files (without extension)')
    parser.add_argument('--no-viz', action='store_true', help='Skip visualization')
    
    args = parser.parse_args()
    
    # Initialize the converter
    converter = TextPhotoTo3D()
    
    # Generate 3D model based on input type
    if args.text:
        obj_path, stl_path = converter.generate_from_text(args.text, args.output)
    else:
        obj_path, stl_path = converter.generate_from_image(args.image, args.output)
    
    # Visualize if not disabled
    if not args.no_viz:
        viz_path = converter.visualize_model(obj_path)
        print(f"Complete! Generated files: {obj_path}, {stl_path}, {viz_path}")
    else:
        print(f"Complete! Generated files: {obj_path}, {stl_path}")


if __name__ == "__main__":
    main() 