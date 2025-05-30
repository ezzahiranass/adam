from adam.components.Core.DataTree import CreateDataTree, Branch


class Merge(CreateDataTree):
    path_mode = 'preserve'

    def compute(self, *branches: Branch, style=None):
        # Assume all branches have the same path
        path = branches[0].path

        merged_elements = []
        for branch in branches:
            merged_elements.extend(branch.elements)

        return Branch(path, merged_elements)
