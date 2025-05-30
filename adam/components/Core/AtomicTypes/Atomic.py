from adam.components.Core.Style import Style
import math
from shapely.geometry import Point as ShapelyPoint, Polygon as ShapelyPolygon
from collections import defaultdict





class Atomic:
    def __init__(self, style: Style=None):
        self.style = style
        self.json = {}
        self.cadquery = None



class AtomicDomain:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def serialize(self):
        return {
            "type": "Domain",
            "start": self.start,
            "end": self.end
        }

