from adam.components.Core.DataTree import CreateDataTree
from adam.components.Core.AtomicTypes.AtomicDomain import AtomicDomain


class ConstructDomain(CreateDataTree):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init__(*args, **kwargs)
        return instance.get_output()

    def run(self, start, end, path=None):
        return AtomicDomain(start, end)
