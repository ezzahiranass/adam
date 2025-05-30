from adam.components.Core.DataTree import CreateDataTree, Branch, Style
from adam.components.Core.AtomicTypes.AtomicVector import AtomicPoint
from adam.components.Core.AtomicTypes.AtomicBrep import AtomicBrep


class CenterBox(CreateDataTree):
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
            hx = dx / 2
            hy = dy / 2
            hz = dz / 2

            cx, cy, cz = center.x, center.y, center.z

            # 8 corner points of the box
            p000 = AtomicPoint(cx - hx, cy - hy, cz - hz) # bottom left back
            p001 = AtomicPoint(cx - hx, cy - hy, cz + hz) # top right back
            p010 = AtomicPoint(cx - hx, cy + hy, cz - hz) # bottom right front
            p011 = AtomicPoint(cx - hx, cy + hy, cz + hz) # top right front
            p100 = AtomicPoint(cx + hx, cy - hy, cz - hz) # bottom right back
            p101 = AtomicPoint(cx + hx, cy - hy, cz + hz) # top right back
            p110 = AtomicPoint(cx + hx, cy + hy, cz - hz) # bottom left front
            p111 = AtomicPoint(cx + hx, cy + hy, cz + hz) # top left front
            points = [p000, p001, p010, p011, p100, p101, p110, p111]

            # 6 face profiles (each as list of 4 points, CCW winding)
            # Triangle faces (12 triangles for 6 sides)
            faces = [
                [0, 1, 3], [0, 3, 2],  # -X
                [4, 6, 7], [4, 7, 5],  # +X
                [0, 4, 5], [0, 5, 1],  # -Y
                [2, 3, 7], [2, 7, 6],  # +Y
                [0, 2, 6], [0, 6, 4],  # -Z
                [1, 5, 7], [1, 7, 3],  # +Z
            ]
            brep = AtomicBrep.from_faces(points, faces, style)

            boxes.append(brep)

        return Branch(path, boxes)
