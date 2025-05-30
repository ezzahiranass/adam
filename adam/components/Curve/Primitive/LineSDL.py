
from adam.components.Core.DataTree import CreateDataTree, Branch
from adam.components.Params.Geometry.Point import AtomicPoint
from adam.components.Params.Geometry.Vector import AtomicVector
from adam.components.Curve.Primitive.Line import AtomicLine
from adam.components.Core.Style import Style

class LineSDL(CreateDataTree):
    path_mode = 'preserve'  # because 1 branch in → 1 branch out
    structure_input_index = [0]  # input of index zero will define the length of the branch


    def compute(self, *branches: Branch, style: Style) -> Branch:
        path = branches[0].path

        starts = branches[0].elements
        directions = branches[1].elements
        lengths = branches[2].elements

        lines = []

        for start, direction, length in zip(starts, directions, lengths):
            start_vec = start.to_vector()
            dir_vec = direction.to_vector()
            end_vec = (
                start_vec[0] + dir_vec[0] * length,
                start_vec[1] + dir_vec[1] * length,
                start_vec[2] + dir_vec[2] * length
            )
            end = AtomicPoint(*end_vec)
            lines.append(AtomicLine(start, end, style=style))

        br = Branch(path, lines)
        return br
