from adam.components.Core.DataTree import CreateDataTree, Branch, Atomic
from adam.components.Core.AtomicTypes.AtomicBrep import AtomicBrep



class Loft(CreateDataTree):
    path_mode = 'preserve'

    def compute(self, *branches: Branch, style=None):
        path = branches[0].path

        curves = branches[0].elements

        grid = []
        for curve in curves:
            points = curve.get_points()
            grid.append(points)  # Each curve gives one row in the grid

        brep = AtomicBrep(vertices=[], faces=[], style=style)
        brep = brep.from_profiles(grid, style)
        return Branch(path, [brep])
