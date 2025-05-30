from adam.components.Core.DataTree import CreateDataTree, Branch



class Series(CreateDataTree):
    """
    Creates a sequence of numbers.

    Inputs:
    - Start: DataTree of float (start of sequence)
    - Step: DataTree of float (step size)
    - Count: DataTree of int (number of elements in sequence)

    Output:
    - DataTree of float (sequence of numbers)
    """
    path_mode = 'extend'
    structure_input_index = [0, 1, 2]

    def compute(self, *branches: Branch, style=None):
        path = branches[0].path
        starts = branches[0].elements
        steps = branches[1].elements
        counts = branches[2].elements

        output_branches = []

        for start, step, count in zip(starts, steps, counts):
            branch = []
            for i in range(count):
                branch.append(start + step * i)
            output_branches.append(Branch(path, branch))

        return output_branches
