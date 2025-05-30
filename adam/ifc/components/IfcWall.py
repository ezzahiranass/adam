import ifcopenshell
import ifcopenshell.api.root
import ifcopenshell.api.geometry
import ifcopenshell.api.spatial
import numpy as np
from adam.ifc.spatial.base import IfcSpatialElement


import numpy as np
import ifcopenshell.api.geometry

def apply_rotation_placement(model, product, location=(0, 0, 0), rotation_degrees=(0, 0, 0)):
    # Create identity 4x4 matrix
    matrix = np.eye(4)

    matrix[:3, 3] = location
    # Set rotation: around Z-axis
    z_rotation = rotation_degrees[2]
    y_rotation = rotation_degrees[1]
    x_rotation = rotation_degrees[0]

    angle_rad = np.radians(z_rotation)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)

    # Rotation matrix around Z
    matrix[:3, :3] = [
        [cos_a, -sin_a, 0],
        [sin_a,  cos_a, 0],
        [0,      0,     1]
    ]
    # Apply placement to the product
    ifcopenshell.api.geometry.edit_object_placement(model, product=product, matrix=matrix)



class IfcWall:
    def __init__(self, model, *args, **kwargs):
        self.model = model
        self.context = kwargs.get("context", None)
        self.wall_data = kwargs.get("wall_data", None)
        self.name = self.wall_data.get("name", "Unnamed Wall")
        self.length = self.wall_data.get("length", 1)
        self.height = self.wall_data.get("height", 1)
        self.thickness = self.wall_data.get("thickness", 0.2)
        self.location = self.wall_data.get("location", (0, 0, 0))
        self.rotation = self.wall_data.get("rotation", (0, 0, 0))

        if not self.context:
            raise ValueError("Context is required")
        
        self.entity = ifcopenshell.api.root.create_entity(model, ifc_class="IfcWall", name=self.name)

        # Give our wall a local origin at (0, 0, 0)
        apply_rotation_placement(model, self.entity, location=self.location, rotation_degrees=self.rotation)

        # Add a new wall-like body geometry, 5 meters long, 3 meters high, and 200mm thick
        
        representation = ifcopenshell.api.geometry.add_wall_representation(
            model, 
            context=self.context.body_context, 
            length=self.length, 
            height=self.height, 
            thickness=self.thickness
            )
        # Assign our new body geometry back to our wall
        ifcopenshell.api.geometry.assign_representation(model, product=self.entity, representation=representation)

