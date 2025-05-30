from adam.components.Core.DataTree import CreateDataTree, Branch, Atomic
from adam.components.Core.Style import Style
from adam.components.Core.AtomicTypes.AtomicBrep import AtomicBrep


from shapely.geometry import Polygon
from shapely.ops import triangulate

# -------------------------------------------------------------------------
# helper: triangulate a (planar) polyline -> vertices, faces  (0-based idx)
# -------------------------------------------------------------------------
def triangulate_polyline(points):
    """
    pts : list[(x, y)]  or  list[(x, y, z)]
    Returns (vertices, faces) ready for AtomicBrep.
    """
    pts = []
    for pt in points:
        pts.append((pt.x, pt.y, pt.z))

    # --- 2-D ring for Shapely ------------------------------------------------
    ring_xy = [(x, y) for x, y, *_ in pts]          # ignore Z for triangulation
    if ring_xy[0] != ring_xy[-1]:                   # make ring closed
        ring_xy.append(ring_xy[0])

    poly = Polygon(ring_xy).buffer(0)               # buffer(0) → clean self-intersections

    # --- triangulate --------------------------------------------------------
    tris = triangulate(poly, tolerance=0.0)

    # --- build vertices/faces ----------------------------------------------
    vert_index = {}          # dict[(x, y)] → idx
    vertices   = []          # list[(x, y, z)]
    faces      = []          # list[[i, j, k]]

    # use a single Z for every vertex (planar assumption)
    default_z = pts[0][2] if len(pts[0]) == 3 else 0.0

    for tri in tris:
        # Shapely exterior gives 4 coords (last == first) → take first 3
        tri_xy = list(tri.exterior.coords)[:3]
        face = []
        for x, y in tri_xy:
            key = (x, y)
            if key not in vert_index:
                vert_index[key] = len(vertices)
                vertices.append((x, y, default_z))
            face.append(vert_index[key])
        faces.append(face)

    return vertices, faces

# -------------------------------------------------------------------------
# the component
# -------------------------------------------------------------------------
class BoundarySurface(CreateDataTree):
    """
    Converts any (planar) polyline into a brep surface by triangulating it.
    Works for convex or concave shapes; holes would require extra handling.
    """
    path_mode = 'preserve'

    def compute(self, *branches: Branch, style: Style | None = None) -> Branch:
        path  = branches[0].path
        polyline = branches[0].elements[0]          # take first polyline in branch

        # 1) get raw points from your atomic polyline class
        pts = polyline.get_points()                 # list of tuples

        # 2) triangulate
        vertices, faces = triangulate_polyline(pts)

        # 3) wrap in your atomic Brep
        brep = AtomicBrep(vertices=vertices, faces=faces, style=style)

        return Branch(path, [brep])
