from adam.components.Core.DataTree import CreateDataTree, Branch
from adam.components.Core.AtomicTypes.AtomicBrep import AtomicBrep
from adam.components.Core.AtomicTypes.AtomicVector import AtomicPoint, AtomicVector
from adam.components.Transform.Euclidean.Move import Move

import math




def sort_ccw(points, normal=AtomicVector(0, 0, 1)):
    """
    Sort a list of AtomicPoints in counter-clockwise order around their centroid,
    projected onto a plane defined by the normal.
    """

    # Calculate centroid
    cx = sum(p.x for p in points) / len(points)
    cy = sum(p.y for p in points) / len(points)
    cz = sum(p.z for p in points) / len(points)
    center = AtomicPoint(cx, cy, cz)

    # Create 2D basis for projection plane
    up = normal.normalized()
    ref = AtomicVector(1, 0, 0) if abs(up.x) < 0.9 else AtomicVector(0, 1, 0)
    x_axis = up.cross(ref).normalized()
    y_axis = up.cross(x_axis).normalized()

    def angle_from_center(p):
        # Vector from center to point
        dx, dy, dz = p.x - cx, p.y - cy, p.z - cz
        vec = AtomicVector(dx, dy, dz)
        # Project onto plane
        px = vec.dot(x_axis)
        py = vec.dot(y_axis)
        return math.atan2(py, px)

    # Sort by angle
    return sorted(points, key=angle_from_center)


# -------------------------------------------------------------------------
# helper: extrude one AtomicBrep by a vector
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# helper: extrude one AtomicBrep by a vector  (boundary-edge aware)
# -------------------------------------------------------------------------
def extrude_brep(base_brep: "AtomicBrep",
                 direction: "AtomicVector",
                 style=None) -> "AtomicBrep":
    """
    Extrudes base_brep by 'direction', creating walls only on boundary edges.
    Works for triangles or n-gon faces.
    """
    base_verts = base_brep.vertices          # list[AtomicPoint]
    n_base     = len(base_verts)

    # -- 1. create top vertices ---------------------------------------------
    top_verts = []
    for v in base_verts:
        v = list(v)
        v[0] += direction.x
        v[1] += direction.y
        v[2] += direction.z
        top_verts.append(AtomicPoint(v[0], v[1], v[2]))
    
    vertices = base_verts + top_verts

    # -- 2. start with caps --------------------------------------------------
    faces: list[list[int]] = []

    # bottom cap (orientation unchanged)
    faces.extend([list(f) for f in base_brep.faces])

    # top cap (reverse orientation, shift indices by n_base)
    faces.extend([[idx + n_base for idx in reversed(f)]
                  for f in base_brep.faces])

    # -- 3. build a frequency map of edges ----------------------------------
    # unordered edge key = tuple(sorted((a, b)))
    edge_count: dict[tuple[int, int], int] = {}

    for f in base_brep.faces:
        m = len(f)
        for i in range(m):
            a = f[i]
            b = f[(i + 1) % m]
            key = tuple(sorted((a, b)))
            edge_count[key] = edge_count.get(key, 0) + 1

    # -- 4. add walls only for boundary edges (count == 1) ------------------
    for (a, b), cnt in edge_count.items():
        if cnt != 1:         # interior edge – skip
            continue
        faces.append([a,             b,       b + n_base])
        faces.append([a, b + n_base, a + n_base])

    return AtomicBrep(vertices=vertices, faces=faces, style=style)








# -------------------------------------------------------------------------
# the component
# -------------------------------------------------------------------------
class Extrude(CreateDataTree):
    """
    Extrudes each AtomicBrep in branch 0 by the matching vector in branch 1.
    Output: Branch of AtomicBreps (side walls + caps built automatically).
    """
    path_mode         = 'preserve'
    structure_inputs  = [0]           # base breps define the tree structure

    def compute(self, *branches: Branch, style=None) -> Branch:
        path       = branches[0].path
        bases      = branches[0].elements          # list[AtomicBrep]
        directions = branches[1].elements          # list[AtomicVector]

        result_breps = []

        for base, vec in zip(bases, directions):
            if not isinstance(base, AtomicBrep):
                raise TypeError(f"Extrude expects AtomicBrep, got {type(base).__name__}")
            if not isinstance(vec, AtomicVector):
                raise TypeError(f"Direction must be AtomicVector, got {type(vec).__name__}")

            extruded_brep = extrude_brep(base, vec, style)
            result_breps.append(extruded_brep)

        return Branch(path, result_breps)
    


    def _extrude_fast(self, brep: AtomicBrep, vec: AtomicVector) -> AtomicBrep:
        # Use the CQ shadow if available; else fall back to numeric routine
        try:
            top = brep.cq.translate((vec.x, vec.y, vec.z))
            solid = brep.cq.union(top)     # fast boolean
            return AtomicBrep(vertices=[], faces=[], cq_obj=solid)
        except Exception:
            # Fallback to numeric triangulation-based extrude_brep you already have
            return extrude_brep(brep, vec)
