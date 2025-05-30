from adam.components.Core.AtomicTypes.Atomic import Atomic
from adam.components.Core.AtomicTypes.AtomicVector import AtomicPoint, AtomicVector
from adam.components.Core.Style import Style
import math
from shapely.geometry import Point as ShapelyPoint, Polygon as ShapelyPolygon
from collections import defaultdict



class AtomicPolyline(Atomic):
    def __init__(self, points, style: Style=None):
        super().__init__(style)
        self.points = points
        self.subtype = "Polyline"
        self.extra_data = {}

    def get_points(self):
        return self.points
    
    def __repr__(self):
        return f"<Polyline {len(self.points)}>"
    
    def move(self, direction, intensity=1.0):
        points =[]
        for pt in self.points:
            coords = pt.to_vector()
            points.append(AtomicPoint(coords[0] + direction.x * intensity, coords[1] + direction.y * intensity, coords[2] + direction.z * intensity))
        return AtomicPolyline(points)

    def serialize(self):
        json = {
            "type": "Polyline",
            "subtype": self.subtype,
            "points": [point.to_vector() for point in self.points]
        }
        if self.extra_data:
            json.update(self.extra_data)
        return json




class AtomicLine(AtomicPolyline):
    def __init__(self, start, end, style: Style=None):
        self.start = start  # type: AtomicPoint
        self.end = end      # type: AtomicPoint
        super().__init__([start, end], style)
        self.subtype = "Line"

    def __repr__(self):
        return f"<{self.subtype} (start={self.start}, end={self.end})>"







class AtomicCircle(AtomicPolyline):
    def __repr__(self):
        return f"<Circle>"

    def __init__(self, center, normal, radius, segments, style=None):
        
        self.center = center  # Point
        self.normal = normal.normalized()  # Vector
        self.radius = radius  # float
        self.segments = segments  # int

        self.points = self.get_points()

        super().__init__(self.points, style)

        self.subtype = "Circle"
        self.extra_data = {
            "center": self.center.to_vector(),
            "normal": self.normal.to_vector(),
            "radius": self.radius,
            "segments": self.segments,
        }
    
    def __repr__(self):
        return f"<{self.subtype} @ {self.center}, radius={self.radius}>"

    def get_points(self):
        # Compute orthonormal basis from normal
        # Start with any vector not parallel to the normal
        if abs(self.normal.x) < 0.99:
            temp = AtomicVector(1, 0, 0)
        else:
            temp = AtomicVector(0, 1, 0)

        x_axis = self.normal.cross(temp).normalized()
        y_axis = self.normal.cross(x_axis).normalized()

        points = []
        for i in range(self.segments+1):
            angle = 2 * math.pi * i / self.segments
            dir_vector = x_axis * math.cos(angle) + y_axis * math.sin(angle)
            center = AtomicVector(*self.center.to_vector())
            point = center + dir_vector * self.radius
            points.append(point)
        return points





class AtomicArc(AtomicPolyline):

    def __init__(self, center, normal, radius, angle_rad, segments, style=None):
        super().__init__(style)
        self.center = center  # AtomicPoint
        self.normal = normal.normalized()  # AtomicVector
        self.radius = radius
        self.angle = angle_rad
        self.segments = segments
        self.subtype = "Arc"
        self.points = self.get_points()
        self.extra_data = {
            "center": self.center.to_vector(),
            "normal": self.normal.to_vector(),
            "radius": self.radius,
            "angle": self.angle,
            "segments": self.segments,
        }

    def __repr__(self):
        return f"<{self.subtype} @ {self.center}, radius={self.radius}>"
    
    def get_points(self):
        if self.points:
            return self.points
        if abs(self.normal.x) < 0.99:
            temp = AtomicVector(1, 0, 0)
        else:
            temp = AtomicVector(0, 1, 0)

        x_axis = self.normal.cross(temp).normalized()
        y_axis = self.normal.cross(x_axis).normalized()

        points = []
        for i in range(self.segments + 1):
            t = i / self.segments
            angle = self.angle * t
            dir_vector = x_axis * math.cos(angle) + y_axis * math.sin(angle)
            center_vec = AtomicVector(*self.center.to_vector())
            point = center_vec + dir_vector * self.radius
            points.append(point)
        self.points = points
        return points
    
    def set_points(self, points):
        self.points = points










