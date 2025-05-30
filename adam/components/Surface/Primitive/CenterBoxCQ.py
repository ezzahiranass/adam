from adam.components.Core.DataTree import CreateDataTree, Branch, Style
from adam.components.Core.AtomicTypes.AtomicVector import AtomicPoint
from adam.components.Core.AtomicTypes.AtomicBrep import AtomicBrep
import cadquery as cq
import io
from cadquery import exporters
import trimesh
import tempfile
import os
from adam.utils.cadquery_helpers import deconstruct_cadquery

class CenterBoxCQ(CreateDataTree):
    path_mode = 'preserve'
    structure_input_index = [0]

    def compute(self, *branches: Branch, style: Style) -> Branch:
        path = branches[0].path
        centers = branches[0].elements
        dims_x = branches[1].elements
        dims_y = branches[2].elements
        dims_z = branches[3].elements

        boxes = []

        for center, dx, dy, dz in zip(centers, dims_x, dims_y, dims_z):
            diameter = 0.5
            result = cq.Workplane("XY").box(dx, dy, dz)
            verts, faces = deconstruct_cadquery(result)
            

            brep = AtomicBrep.from_faces(verts, faces, style)

            boxes.append(brep)

        return Branch(path, boxes)
