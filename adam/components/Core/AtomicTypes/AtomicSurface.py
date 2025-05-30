from adam.components.Core.AtomicTypes.Atomic import Atomic
from adam.components.Core.AtomicTypes.AtomicVector import AtomicPoint, AtomicVector
from adam.components.Core.CadQuery import _CQProxy
import cadquery as cq
from cadquery import Face as CQFace, Wire as CQWire, Shell as CQShell
import math
from shapely.geometry import Polygon as ShapelyPolygon

class AtomicSurface:
    def __init__(self,
                 vertices: list[AtomicPoint],
                 faces: list[list[int]],
                 uvs: list[tuple[float, float]] = None,
                 style=None,
                 origin="manual"):
        self.vertices = vertices              # 3D positions
        self.faces = faces                    # face indices (usually tris or quads)
        self.uvs = uvs                        # optional, for textures or surface params
        self.style = style
        self.origin = origin
        self.metadata = {}
        self._cq = _CQProxy(self._to_cq)

    def _to_cq(self):
        # convert to cadquery Face/Shell
        vlist = [cq.Vector(p.x, p.y, p.z) for p in self.vertices]

        face_objs = []
        for f in self.faces:
            wire = CQWire.makePolygon([vlist[i] for i in f] + [vlist[f[0]]])
            face_objs.append(CQFace.makeFromWires(wire))

        shell = CQShell.makeShell(face_objs)
        return shell if shell.isValid() else face_objs[0]

    @property
    def cq(self):
        return self._cq.obj

    def serialize(self):
        json = {
            "type": "Surface",
            "subtype": self.subtype,
            "vertices": [v.to_vector() for v in self.vertices],
            "faces": self.faces,
            "uvs": self.uvs,
        }
        if self.extra_data:
            json.update(self.extra_data)
        return json




class AtomicPolygon(AtomicSurface):
    def __init__(self, center, normal, radius, segments, fillet_radius=3):
        self.center = center              # AtomicPoint
        self.normal = normal.normalized()  # AtomicVector
        self.radius = radius
        self.segments = segments
        self.fillet_radius = fillet_radius

        self.points = self.get_points()
        self.subtype = "Polygon"
        self.extra_data = {
            "center": self.center.to_vector(),
            "normal": self.normal.to_vector(),
            "radius": self.radius,
            "segments": self.segments,
            "fillet_radius": self.fillet_radius,
        }

    def __repr__(self):
        return f"<{self.subtype} @ {self.center}, radius={self.radius}>"

    def get_points(self):

        angle_step = 2 * math.pi / self.segments
        raw_2d = [
            (self.radius * math.cos(i * angle_step), self.radius * math.sin(i * angle_step))
            for i in range(self.segments)
        ]

        poly = ShapelyPolygon(raw_2d)

        if self.fillet_radius > 0:
            poly = poly.buffer(-self.fillet_radius).buffer(self.fillet_radius)

        # --- Create orthonormal basis from normal ---
        z_axis = self.normal.normalized()
        if abs(z_axis.x) < 0.99:
            temp = AtomicVector(1, 0, 0)
        else:
            temp = AtomicVector(0, 1, 0)

        x_axis = z_axis.cross(temp).normalized()
        y_axis = z_axis.cross(x_axis).normalized()

        # --- Transform 2D points into 3D using the basis ---
        result = []
        for x2d, y2d in poly.exterior.coords:
            vec = x_axis * x2d + y_axis * y2d
            point = self.center + vec
            result.append(AtomicPoint(point.x, point.y, point.z))

        return result