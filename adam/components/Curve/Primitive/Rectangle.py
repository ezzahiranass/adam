import math
from adam.components.Core.AtomicTypes.AtomicVector import AtomicPoint
from adam.components.Core.DataTree import CreateDataTree, Branch
from adam.components.Core.AtomicTypes.AtomicPolyline import AtomicPolyline
from adam.components.Core.Style import Style



def create_rectangle(center, x_size, y_size, radius):
    points = []
    points.append(AtomicPoint(center.x - x_size/2, center.y - y_size/2, center.z))
    points.append(AtomicPoint(center.x + x_size/2, center.y - y_size/2, center.z))
    points.append(AtomicPoint(center.x + x_size/2, center.y + y_size/2, center.z))
    points.append(AtomicPoint(center.x - x_size/2, center.y + y_size/2, center.z))
    points.append(points[0])
    return points


class Rectangle(CreateDataTree):
    path_mode = 'preserve'  # because 1 branch in → 1 branch out
    structure_input_index = [0]  # input of index zero will define the length of the branch


    def compute(self, *branches: Branch, style: Style):
        path = branches[0].path
        centers = branches[0].elements
        x_sizes = branches[1].elements
        y_sizes = branches[2].elements
        radii = branches[3].elements

        branch = []
        for center, x_size, y_size, radius in zip(centers, x_sizes, y_sizes, radii):
            points = create_rectangle(center, x_size, y_size, radius)
            polyline = AtomicPolyline(points, style)
            branch.append(polyline)

        return Branch(path, branch)
