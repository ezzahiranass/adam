



from adam.components.Core.DataTree import CreateDataTree, Branch



class RepeatData(CreateDataTree):
    """
    Repeats Data

    Inputs:
    - Data: DataTree of float (data to repeat)
    - length: DataTree of int (number of elements in sequence)

    Output:
    - DataTree of float (data tree repeated)
    """
    path_mode = 'preserve'
    structure_input_index = [0, 1]

    def compute(self, *branches: Branch, style=None):
        path = branches[0].path
        data = branches[0].elements
        lengths = branches[1].elements[0]
        # TODO: Make this work for multiple lengths



        branch = []
        for i in range(lengths):
            data_idx = i % len(data)
            branch.append(data[data_idx])

        branch = Branch(path, branch)
        

        return branch
