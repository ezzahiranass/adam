import math
from adam.components.Core.DataTree import CreateDataTree, Branch
from adam.components.Core.AtomicTypes.AtomicPolyline import AtomicArc



class Arc(CreateDataTree):
    path_mode = 'preserve'

    def compute(self, *branches: Branch, style=None):
        path = branches[0].path

        centers = branches[0].elements
        normals = branches[1].elements
        radii = branches[2].elements
        angles = branches[3].elements
        segments = branches[4].elements

        arcs = []

        for center, normal, radius, angle, seg in zip(centers, normals, radii, angles, segments):
            arc = AtomicArc(center, normal, radius, angle, seg, style)
            arcs.append(arc)

        return Branch(path, arcs)
