from adam.components.Core.AtomicTypes.Atomic import Atomic
from adam.components.Core.AtomicTypes.AtomicVector import AtomicPoint, AtomicVector
from adam.components.Core.CadQuery import _CQProxy
import cadquery as cq
import math



class AtomicBrep(Atomic):
    __slots__ = ("vertices", "faces", "_cq")

    def __init__(self, vertices, faces, cq_obj=None, style=None):
        super().__init__(style)
        self.vertices = vertices  # List of [x, y, z]
        self.faces = faces        # List of [i1, i2, i3]
        self._style = style
        self.profiles = []
        self.type = "Brep"   
        if cq_obj is not None:
            # caller already built a solid – keep reference
            self._cq = _CQProxy(lambda: cq_obj)
        else:
            # build lazily when/if needed
            self._cq = _CQProxy(self._to_cq)

    def _to_cq(self) -> cq.Shape:
        """
        Rebuild a CadQuery solid from verts/faces only when somebody asks.
        """
        # Build one face per polygon, then stitch into a shell
        faces = []
        vlist = [cq.Vector(p.x, p.y, p.z) for p in self.vertices]

        for poly in self.faces:
            wires = cq.Wire.makePolygon([vlist[i] for i in poly] + [vlist[poly[0]]])
            faces.append(cq.Face.makeFromWires(wires))

        shell = cq.Shell.makeShell(faces)
        solid = cq.Solid.makeSolid(shell) if shell.isValid() else shell
        return solid

    @property
    def cq(self) -> cq.Shape:
        return self._cq.obj


    

    @classmethod
    def from_faces(cls, points: list, face_indices: list, style=None):
        """
        points: List of AtomicPoint or [x, y, z]
        face_indices: List of index triplets (e.g. [[0, 1, 2], ...])
        """
        if isinstance(points[0], AtomicPoint) or isinstance(points[0], AtomicVector):

            verts = [p for p in points]
        else:
            verts = points
        return cls(vertices=verts, faces=face_indices, style=style)

    def from_profiles(self, profiles: list, style=None):
        """
        Construct an AtomicBrep from a 2D list of profile points.
        
        profiles: List of lists of AtomicPoint objects representing cross-sectional profiles
        """
        vertices = []
        faces = []
        self.profiles = profiles
        
        # Extract vertex coordinates from profile points
        for profile in profiles:
            for pt in profile:
                if isinstance(pt, AtomicPoint):
                    vertices.append([pt.x, pt.y, pt.z])
                else:
                    vertices.append(pt)
        
        # Create faces by triangulating between profiles
        rows = len(profiles)
        cols = len(profiles[0]) if rows > 0 else 0
        
        for i in range(rows - 1):
            for j in range(cols - 1):
                a = i * cols + j
                b = a + 1
                c = a + cols
                d = c + 1
                
                # Triangle 1: a → c → b
                faces.append([a, c, b])
                
                # Triangle 2: b → c → d
                faces.append([b, c, d])
        
        brep = AtomicBrep(vertices=vertices, faces=faces, style=style)
        brep.profiles = profiles
        return brep
    
    def assign_type(self, type):
        self.type = type

    def serialize(self):
        verts = [tuple(pt) for pt in self.vertices]
        return {
            "type": "Brep",
            "subtype": self.type,
            "name": self.type,
            "vertices": verts,
            "faces": self.faces,
        }

    def move(self, direction, intensity=1.0):
        verts = [tuple(pt) for pt in self.vertices]
        dx, dy, dz = direction.x * intensity, direction.y * intensity, direction.z * intensity

        moved_vertices = [
            [x + dx, y + dy, z + dz]
            for x, y, z in verts
        ]

        return AtomicBrep(moved_vertices, self.faces, style=self._style)

    def rotate(self, angle_rad, origin, axis, style=None):
        def rotate_point(x, y, z):
            # Vector from origin
            ox, oy, oz = origin.x, origin.y, origin.z
            vx, vy, vz = x - ox, y - oy, z - oz

            # Normalize axis
            ax, ay, az = axis.normalized().to_vector()

            cos_t = math.cos(angle_rad)
            sin_t = math.sin(angle_rad)
            dot = vx * ax + vy * ay + vz * az
            cross = [
                ay * vz - az * vy,
                az * vx - ax * vz,
                ax * vy - ay * vx
            ]

            rx = (vx * cos_t +
                  cross[0] * sin_t +
                  ax * dot * (1 - cos_t))
            ry = (vy * cos_t +
                  cross[1] * sin_t +
                  ay * dot * (1 - cos_t))
            rz = (vz * cos_t +
                  cross[2] * sin_t +
                  az * dot * (1 - cos_t))

            return [ox + rx, oy + ry, oz + rz]

        rotated_vertices = [rotate_point(x, y, z) for x, y, z in self.vertices]

        return AtomicBrep(rotated_vertices, self.faces, style=style or self._style)

    def get_surface_points(self):
        """
        Returns a 2D list of points representing the lofted surface.
        No interpolation — just a grid of profile points.
        """
        return self.profiles