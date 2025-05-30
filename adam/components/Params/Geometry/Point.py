from adam.components.Core.DataTree import CreateDataTree, Branch
from adam.components.Core.Style import Style
from adam.components.Core.AtomicTypes.AtomicVector import AtomicPoint



class Point(CreateDataTree):
    path_mode = 'preserve' #Will return one branch per given branch
    def compute(self, *branches: Branch, style: Style):
        path = branches[0].path
        # compute receives only one branch per input, to get path, you can take it from any element, in this case, we receive x y and z as data trees, processing one branch at a time, path variable is available in either branches[0] or branches[1] or branches[2] (we take 0 to be safe)
        points = []
        for x, y, z in zip(*[b.elements for b in branches]):
            points.append(AtomicPoint(x, y, z))
        return Branch(path, points)

