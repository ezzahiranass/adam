import math
from adam.components.Core.AtomicTypes.AtomicVector import AtomicPoint, AtomicVector
from adam.components.Core.DataTree import CreateDataTree
from adam.components.Core.AtomicTypes.AtomicSurface import AtomicPolygon



class Polygon(CreateDataTree):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init__(*args, **kwargs)
        return instance.get_output()

    def run(self, center=AtomicPoint(0, 0, 0), normal=AtomicVector(0, 1, 0), radius=5, segments=8, fillet_radius=3):
        return AtomicPolygon(center, normal, radius, segments, fillet_radius)
