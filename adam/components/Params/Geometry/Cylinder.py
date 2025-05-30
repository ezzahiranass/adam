import numpy as np
import trimesh



class Cylinder:
    def __init__(self, center, radius, thickness=0.01, width=0.01, segments=64):
        """
        Create a ribbon around a circular path.
        
        Args:
            center (array-like): Center of the circle [x, y, z].
            radius (float): Radius of the circle.
            thickness (float): Ribbon's thickness along Z (like height).
            width (float): Width of the ribbon outward from the circle path.
            segments (int): Number of segments to approximate the circle.
        """
        self.center = np.array(center)
        self.radius = radius
        self.thickness = thickness
        self.width = width
        self.segments = segments
        self.geometrize()

    def geometrize(self):
        # Create a compas circle
        self.geometry = trimesh.creation.cylinder(radius=self.radius, height=self.thickness, sections=self.segments)

        return self.geometry

