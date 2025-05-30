import math
from adam.components.Core.DataTree import CreateDataTree, Atomic, Branch



class Radians(CreateDataTree):
    path_mode = 'preserve'

    def compute(self, *branches: Branch, style=None):
        path = branches[0].path
        angle = branches[0].elements[0]
        return Branch(path, [math.radians(angle)])


