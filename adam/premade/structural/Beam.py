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


class Beam(CreateDataTree):
    path_mode = 'preserve'
    structure_input_index = [0]

    def compute(self, *branches: Branch, style: Style) -> Branch:
        path = branches[0].path
        centers = branches[0].elements
        lengths = branches[1].elements
        widths = branches[2].elements
        heights = branches[3].elements

        boxes = []

        for center, length, width, height in zip(centers, lengths, widths, heights):

            center = list(center.to_vector())
            center[0] -= length/2
            width = 0.2
            height = 0.1
            center = tuple(center)
            
            (L, H, W, t) = (length, height, width, 1.0)

            pts = [
                (0, H / 2.0),
                (W / 2.0, H / 2.0),
                (W / 2.0, (H / 2.0 - t)),
                (t / 2.0, (H / 2.0 - t)),
                (t / 2.0, (t - H / 2.0)),
                (W / 2.0, (t - H / 2.0)),
                (W / 2.0, H / -2.0),
                (0, H / -2.0),
            ]
            result = cq.Workplane("YZ").polyline(pts).mirrorY().extrude(L).translate(center)
            verts, faces = deconstruct_cadquery(result)

            brep = AtomicBrep.from_faces(verts, faces, style)

            boxes.append(brep)

        return Branch(path, boxes)
