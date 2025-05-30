from adam.components.Core.AtomicTypes.AtomicVector import AtomicPoint
from adam.components.Core.AtomicTypes.AtomicPolyline import AtomicLine
from adam.components.Core.DataTree import CreateDataTree, Branch

def divide_line(line, count):
    branch = []
    for i in range(count + 1):
        t = i / count
        x = line.start.x + t * (line.end.x - line.start.x)
        y = line.start.y + t * (line.end.y - line.start.y)
        z = line.start.z + t * (line.end.z - line.start.z)
        branch.append(AtomicPoint(x, y, z))
    return branch



class DivideCurve(CreateDataTree):
    path_mode = 'extend'
    structure_input_index = 0  # use only line input to define structure

    def compute(self, *branches: Branch, style=None):
        path = branches[0].path

        curves = branches[0].elements
        divisions = branches[1].elements

        output_branches = []

        for i, (curve, division) in enumerate(zip(curves, divisions)):
            if isinstance(curve, AtomicLine):
                pts = divide_line(curve, division)
                output_branches.append(Branch(None, pts))  # path set later
            else:
                raise TypeError(f"DivideCurve not implemented for {type(curve).__name__}")

        return output_branches  # List[Branch]

