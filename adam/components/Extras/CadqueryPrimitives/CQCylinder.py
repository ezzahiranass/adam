import math
from adam.components.Core.AtomicTypes.AtomicVector import AtomicPoint
from adam.components.Core.DataTree import CreateDataTree, Branch
from adam.components.Core.AtomicTypes.AtomicPolyline import AtomicCircle
from adam.components.Core.AtomicTypes.AtomicBrep import AtomicBrep

from adam.utils.cadquery_helpers import cq_to_atomicbrep
import math
import cadquery as cq
from cadquery import Vector as cq_Vector


import math
import cadquery as cq
from cadquery import Vector as cq_Vector

# ─────────────────────────────────────────────────────────────
# helper: unwrap workplane and tessellate
# ─────────────────────────────────────────────────────────────
def cq_to_atomicbrep(shape) -> "AtomicBrep":
    if isinstance(shape, cq.Workplane):
        shape = shape.val()
    verts, faces = shape.tessellate(1e-3)          # tolerance = 0.001
    return AtomicBrep([AtomicPoint(*v) for v in verts], faces)

# ─────────────────────────────────────────────────────────────
class AtomicCQCylinder:
    """
    Build a cylinder aligned with `normal`, centred at `center`.
    If `segments` is given and ≥3, the circle is approximated by an n-gon
    profile that is extruded symmetrically by `height`.
    Otherwise it uses CadQuery’s native cylinder primitive.
    """
    __slots__ = ("center", "normal", "radius", "segments", "height", "geometry")

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        self.__init__(*args, **kwargs)
        return self.geometry            # so callers get the AtomicBrep

    def __init__(self, center, normal, radius, segments, height):
        self.center   = center          # AtomicPoint
        self.normal   = normal          # AtomicVector
        self.radius   = radius
        self.segments = segments
        self.height   = height
        self.geometry = self._build()

    # ---------------------------------------------------------
    def _build(self) -> "AtomicBrep":
        wp = cq.Workplane("XY")

        # 1) build the base solid on Z axis
            # polygon → extrude symmetrically
        solid = (wp
                    .polygon(self.segments, self.radius)
                    .extrude(self.height, both=True))
        # solid = wp.cylinder(self.height, self.radius, center=True)

        # origin should be at the bottom of the cylinder
        solid = solid.translate((0, 0, self.height))

        # 2) orient to `normal`
        z_axis = cq_Vector(0, 0, 1)
        n_vec  = cq_Vector(self.normal.x, self.normal.y, self.normal.z)
        n_vec  = n_vec.normalized()

        if not n_vec == z_axis:
            rot_axis = z_axis.cross(n_vec)
            if rot_axis.Length < 1e-9:          # normal is opposite Z
                rot_axis = cq_Vector(1, 0, 0)   # 180° about X
            angle = math.degrees(z_axis.getAngle(n_vec))
            solid = solid.rotate((0, 0, 0), rot_axis.toTuple(), angle)

        # 3) translate to `center`
        solid = solid.translate((self.center.x, self.center.y, self.center.z))

        

        # 4) tessellate → AtomicBrep
        return cq_to_atomicbrep(solid)





class CQCylinder(CreateDataTree):
    """
    create with a center, normal, radius, segments, height
    Builds cylinders whose axes pass through `center` and follow `normal`.
    """
    path_mode = 'preserve'

    def compute(self, *branches: Branch, style=None) -> Branch:
        path     = branches[0].path
        centers  = branches[0].elements      # list[AtomicPoint]
        normals  = branches[1].elements      # list[AtomicVector]
        radii    = branches[2].elements      # list[float]
        segments = branches[3].elements      # list[int]         (can be None)
        heights  = branches[4].elements      # list[float]

        cylinders = []

        z_axis = cq_Vector(0, 0, 1)

        for center, normal, radius, seg, height in zip(
                centers, normals, radii, segments, heights):
            cyl = AtomicCQCylinder(center, normal, radius, seg, height)

            cylinders.append(cyl)

        return Branch(path, cylinders)
