from adam.components.Core.DataTree import CreateDataTree, Branch
from adam.components.Core.AtomicTypes.AtomicVector import AtomicVector



class UnitZ(CreateDataTree):
    path_mode = 'preserve'  # One output per input element

    def compute(self, *branches: Branch, style=None) -> Branch:
        path = branches[0].path
        factors = branches[0].elements

        vectors = [
            AtomicVector(0, 0, factor)
            for factor in factors
        ]

        return Branch(path, vectors)
