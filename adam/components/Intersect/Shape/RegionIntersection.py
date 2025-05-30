from adam.components.Core.DataTree import CreateDataTree, Branch
from adam.components.Core.Style import Style
from adam.components.Core.AtomicTypes.AtomicPolyline import AtomicPolyline
from adam.components.Core.AtomicTypes.AtomicVector import AtomicPoint


from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from typing import List

# --- utility --------------------------------------------------------------

def polygon_from_points(pts):
    """
    pts: list[tuple[float, float]]
    Returns a Shapely Polygon.  Assumes pts are in order and form a closed loop.
    """
    # Ensure first == last for Shapely
    if pts[0] != pts[-1]:
        pts = pts + [pts[0]]
    return Polygon(pts)

def polyline_from_coords(coords_seq):
    """
    coords_seq : shapely CoordinateSequence | iterable
    cls        : your Polyline class (needs .from_points(list_of_xy))
    """
    # Convert to a plain list of tuples and strip any Z-value if present
    pts = [(x, y) for *xy, _ in [(*c, 0) if len(c) == 2 else c for c in coords_seq] for x, y in [xy]]

    # Drop duplicate closing point if the ring is already closed
    if len(pts) > 1 and pts[0] == pts[-1]:
        pts = pts[:-1]

    points = []
    for pt in pts:
        p = AtomicPoint(pt[0], pt[1], 0)
        points.append(p)
    
    points.append(points[0])


    polyline = AtomicPolyline(points)

    return polyline


# --- the component --------------------------------------------------------

class RegionIntersection(CreateDataTree):
    """
    Keeps only the parts of A-curves that fall inside the B-curve,  
    clipping partially-overlapping rectangles to the circle boundary.
    """
    path_mode = 'preserve'
    structure_input_index = [0, 1]      # A-curves & B-curves define structure

    def compute(self, *branches: Branch, style: Style) -> Branch:
        a_curves = branches[0].elements   # list[RectangleCurve]
        b_curves = branches[1].elements   # list[CircleCurve]
        normals  = branches[2].elements   # ignored for 2-D clip

        path   = branches[0].path
        output = []

        for a_curve, b_curve, _ in zip(a_curves, b_curves, normals):
            # --- Shapely geometry -----------------------------------------
            rect_poly  = polygon_from_points(a_curve.get_points())
            circle_poly = polygon_from_points(b_curve.get_points())

            inter = rect_poly.intersection(circle_poly)

            # Nothing inside the circle → skip
            if inter.is_empty:
                continue

            # Fully inside → keep original rectangle polyline unchanged
            if inter.equals(rect_poly):
                output.append(a_curve)          # unchanged
                continue

            # Partial overlap ------------------------------------------------
            # inter can be Polygon or MultiPolygon
            pieces = [inter] if isinstance(inter, Polygon) else list(inter)

            for piece in pieces:
                # Build a polyline for every connected piece
                new_poly = polyline_from_coords(piece.exterior.coords)
                output.append(new_poly)

        return Branch(path, output)
