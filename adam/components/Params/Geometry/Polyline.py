from adam.components.params.Curve.Curve import Curve
from adam.components.Core.DataTree import CreateDataTree, DataTree
class Polyline(Curve):
    def __init__(self, points):
        # If a PointGroup is passed, extract the points
        self.points = points

    def get_points(self):
        return self.points

    def serialize(self):
        return {
            "type": "Polyline",
            "points": [p.to_vector() for p in self.points],
        }

    
    def length(self):
        total = 0
        for i in range(1, len(self.points)):
            p1 = self.points[i - 1]
            p2 = self.points[i]
            total += ((p2.x - p1.x)**2 + (p2.y - p1.y)**2 + (p2.z - p1.z)**2) ** 0.5
        if self.closed and len(self.points) > 1:
            p1 = self.points[-1]
            p2 = self.points[0]
            total += ((p2.x - p1.x)**2 + (p2.y - p1.y)**2 + (p2.z - p1.z)**2) ** 0.5
        return total



class CreatePolyline(CreateDataTree):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init__(*args, **kwargs)
        return instance.get_output()

    def run(self, *args):
        # args is a list of points
        return Polyline(args)
