import math
from adam.components.Core.AtomicTypes.AtomicVector import AtomicPoint
from adam.components.Core.DataTree import CreateDataTree, Branch
from adam.components.Core.AtomicTypes.AtomicPolyline import AtomicCircle



class Circle(CreateDataTree):
    path_mode = 'preserve'

    def compute(self, *branches: Branch, style=None):
        path = branches[0].path

        centers = branches[0].elements
        normals = branches[1].elements
        radii = branches[2].elements
        segments = branches[3].elements

        circles = []

        for center, normal, radius, segments in zip(centers, normals, radii, segments):
            circles.append(AtomicCircle(center, normal, radius, segments, style))

        return Branch(path, circles)
