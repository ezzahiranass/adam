import os
import uuid
import trimesh
import numpy as np

def export_cube_gltf(size=1.0, output_dir="output"):
    """
    Create a cube using trimesh and export it as GLTF
    
    Args:
        size: Size of the cube
        output_dir: Directory to save the output file
        
    Returns:
        tuple: (filename, filepath)
    """
    # Create cube mesh using trimesh
    cube = trimesh.creation.box(extents=[size, size, size])
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate unique filename
    filename = f"cube_{uuid.uuid4().hex[:8]}.glb"
    filepath = os.path.join(output_dir, filename)
    
    # Export as GLTF
    cube.export(filepath)
    
    return filename, filepath
