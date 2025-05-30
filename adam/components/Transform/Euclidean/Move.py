from adam.components.Core.DataTree import CreateDataTree
from adam.components.Params.Geometry.Point import AtomicPoint
from adam.components.Curve.Primitive.Line import AtomicLine
from adam.components.Core.DataTree import Branch
from adam.components.Core.Style import Style
from adam.components.Core.AtomicTypes.AtomicPolyline import AtomicCircle, AtomicArc, AtomicPolyline
from adam.components.Core.AtomicTypes.AtomicBrep import AtomicBrep

def apply_move(geom, direction, intensity, style=None):

    def move_point(p: AtomicPoint):
        return AtomicPoint(
            p.x + direction.x * intensity,
            p.y + direction.y * intensity,
            p.z + direction.z * intensity
        )

    if isinstance(geom, AtomicPoint):
        result = AtomicPoint(
            geom.x + direction.x * intensity,
            geom.y + direction.y * intensity,
            geom.z + direction.z * intensity
        )
        if style:
            result._style = style
        return result
    elif isinstance(geom, AtomicLine):
        result = AtomicLine(
            start=apply_move(geom.start, direction, intensity),
            end=apply_move(geom.end, direction, intensity)
        )
        if style:
            result._style = style
        return result
    # Add more as needed: Circle, Mesh, etc.
    elif isinstance(geom, AtomicCircle):
        
        result = AtomicCircle(
            center=apply_move(geom.center, direction, intensity),
            radius=geom.radius,
            segments=geom.segments,
            normal=geom.normal
        )
        if style:
            result._style = style
        return result
    elif isinstance(geom, AtomicArc):
        points = [move_point(p) for p in geom._points]

        result = AtomicArc(
            center=move_point(geom.center),
            angle_rad=geom.angle,
            radius=geom.radius,
            segments=geom.segments,
            normal=geom.normal
        )
        result.set_points(points)
        if style:
            result._style = style
        return result
    
    elif isinstance(geom, AtomicBrep):
        return geom.move(direction, intensity)
    elif isinstance(geom, AtomicPolyline):
        return geom.move(direction, intensity)
    else:
        raise TypeError(f"Move not implemented for {type(geom).__name__}")


class Move(CreateDataTree):
    
    path_mode = 'preserve'  # because 1 branch in → 1 branch out
    structure_input_index = [0]

    def compute(self, *branches: Branch, style: Style) -> Branch:
        geoms = branches[0]
        directions = branches[1]
        intensities = branches[2]

        elements = []
        for geom, direction, intensity in zip(geoms.elements, directions.elements, intensities.elements):
            g = apply_move(geom, direction, intensity, style)
            elements.append(g)

        return Branch(geoms.path, elements)
