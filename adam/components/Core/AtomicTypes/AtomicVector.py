from .Atomic import Atomic

from adam.components.Core.Style import Style
import math
from shapely.geometry import Point as ShapelyPoint, Polygon as ShapelyPolygon
from collections import defaultdict
from adam.components.Core.CadQuery import _CQProxy

import cadquery as cq

class AtomicVector(Atomic):
    __slots__ = ("x", "y", "z", "_cq")
    def __init__(self, x, y, z, style: Style=None):
        self.x, self.y, self.z = x, y, z
        self._cq = _CQProxy(lambda: cq.Vector(self.x, self.y, self.z))
        self.subtype = "Vector"
        self.extra_data = {}

    # on demand:
    @property
    def cq(self) -> cq.Vector:
        return self._cq.obj

    def __repr__(self):
        return f"<Vector({self.x}, {self.y}, {self.z})>"

    def cross(self, other):
        return AtomicVector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalized(self):
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize a zero vector")
        return AtomicVector(self.x / mag, self.y / mag, self.z / mag)

    def __mul__(self, scalar):
        return AtomicVector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __add__(self, other):
        return AtomicVector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return AtomicVector(self.x - other.x, self.y - other.y, self.z - other.z)

    def to_vector(self):
        return (self.x, self.y, self.z)

    def serialize(self):
        json = {
            "type": self.subtype,
            "vector": self.to_vector()
        }
        if self.extra_data:
            json.update(self.extra_data)
        return json
    


class AtomicPoint(AtomicVector):
    __slots__ = ("x", "y", "z", "_cq")
    def __init__(self, x, y, z, style: Style=None):
        super().__init__(x, y, z, style)
        self.subtype = "Point"

    def __repr__(self): return f"<Point({self.x}, {self.y}, {self.z})>"


class AtomicNormal(AtomicVector):
    
    __slots__ = ("x", "y", "z", "_cq")
    def __init__(self, x, y, z, style: Style=None):
        super().__init__(x, y, z, style)
        self.subtype = "Normal"

    def __repr__(self): return f"<Normal({self.x}, {self.y}, {self.z})>"


class AtomicPlane(Atomic):
    
    
    __slots__ = ("x", "y", "z", "_cq")
    
    def __init__(self, center: AtomicPoint, normal: AtomicVector):
        self.center = center
        self.normal = normal.normalized()
        self.subtype = "Plane"


    def __repr__(self):
        return f"<Plane(center={self.center}, normal={self.normal})>"


class AtomicUnit(AtomicVector):
    __slots__ = ("x", "y", "z", "_cq", "axis")
    
    def __init__(self, axis: str, style: Style=None):
        """
        Create a unit vector along the specified axis.
        
        Args:
            axis: Must be 'X', 'Y', or 'Z' (case insensitive)
            style: Optional style parameter
        """
        axis = axis.upper()
        if axis not in ['X', 'Y', 'Z']:
            raise ValueError("axis must be 'X', 'Y', or 'Z'")
        
        self.axis = axis
        if axis == 'X':
            x, y, z = 1, 0, 0
        elif axis == 'Y':
            x, y, z = 0, 1, 0
        else:  # axis == 'Z'
            x, y, z = 0, 0, 1
            
        super().__init__(x, y, z)
        self.subtype = "Unit"

    @classmethod
    def X(cls, style: Style=None):
        """Create a unit vector along the X axis"""
        return cls('X', style)
    
    @classmethod
    def Y(cls, style: Style=None):
        """Create a unit vector along the Y axis"""
        return cls('Y', style)
    
    @classmethod
    def Z(cls, style: Style=None):
        """Create a unit vector along the Z axis"""
        return cls('Z', style)

    def __repr__(self): 
        return f"<Unit {self.axis}>"
