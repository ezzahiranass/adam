from adam.components.Core.DataTree import CreateDataTree, Branch
from adam.components.Core.AtomicTypes.AtomicVector import AtomicPoint, AtomicVector
from adam.components.Core.AtomicTypes.AtomicPolyline import AtomicCircle, AtomicArc, AtomicLine
from adam.components.Core.AtomicTypes.AtomicBrep import AtomicBrep
from adam.components.Core.Style import Style
import math





def apply_rotate(geom, angle_rad, origin: AtomicPoint, axis: AtomicVector, style=None):
    def rotate_point(p: AtomicPoint):
        # Translate to origin
        p_vec = AtomicVector(p.x - origin.x, p.y - origin.y, p.z - origin.z)
        axis_n = axis.normalized()

        # Rodrigues’ rotation formula
        cos_theta = math.cos(angle_rad)
        sin_theta = math.sin(angle_rad)
        dot = axis_n.dot(p_vec)
        cross = axis_n.cross(p_vec)

        rotated = (p_vec * cos_theta +
                   cross * sin_theta +
                   axis_n * dot * (1 - cos_theta))

        rotated_point = AtomicPoint(
            origin.x + rotated.x,
            origin.y + rotated.y,
            origin.z + rotated.z
        )
        if style:
            rotated_point._style = style
        
        return rotated_point

    if isinstance(geom, AtomicPoint):
        return rotate_point(geom)

    elif isinstance(geom, AtomicLine):
        return AtomicLine(
            start=rotate_point(geom.start),
            end=rotate_point(geom.end),
            style=style
        )

    elif isinstance(geom, AtomicCircle):
        return AtomicCircle(
            center=rotate_point(geom.center),
            normal=axis,
            radius=geom.radius,
            segments=geom.segments,
            style=style
        )

    elif isinstance(geom, AtomicArc):
        rotated_points = [rotate_point(pt) for pt in geom.get_points()]

        rotated_arc = AtomicArc(
            center=rotate_point(geom.center),
            normal=axis,
            radius=geom.radius,       # radius isn't rotated, only orientation matters
            angle_rad=geom.angle,
            segments=geom.segments,
            style=style
        )
        rotated_arc.set_points(rotated_points)

        return rotated_arc


    elif isinstance(geom, AtomicBrep):
        return geom.rotate(angle_rad, origin, axis, style)
    else:
        raise TypeError(f"Rotate not implemented for {type(geom).__name__}")

class Rotate(CreateDataTree):
    """
    Rotates geometry around a given axis.

    Inputs:
    - Geometry: DataTree of AtomicPoint, AtomicLine, AtomicArc, etc.
    - Angle: DataTree of float (radians)
    - Axis: DataTree of AtomicVector (defines rotation axis)

    Output:
    - DataTree of Rotated geometry with preserved structure.
    """
    path_mode = 'preserve'
    structure_inputs = [0]


    def compute(self, *branches: Branch, style: Style) -> Branch:
        geom_branch = branches[0]
        angle_branch = branches[1]
        plane_branch = branches[2]

        rotated = []

        for geom, angle, plane in zip(geom_branch.elements, angle_branch.elements, plane_branch.elements):
            
            rotated.append(
                apply_rotate(
                    geom, 
                    angle, 
                    origin=AtomicPoint(0, 0, 0), 
                    axis=AtomicVector(0, 0, 1), 
                    style=style
                )
            )

        return Branch(geom_branch.path, rotated)
