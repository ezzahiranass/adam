from adam.components.Core.DataTree import CreateDataTree, Branch
from adam.components.Core.AtomicTypes.AtomicPolyline import AtomicLine



class Line(CreateDataTree):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init__(*args, **kwargs)
        return instance.get_output()

    def run(self, start, end, path=None):
        return Branch(path, [AtomicLine(start, end)])
