import math
from adam.components.Core.AtomicTypes.AtomicVector import AtomicPoint
from adam.components.Core.AtomicTypes.AtomicVector import AtomicVector
from adam.components.Core.DataTree import CreateDataTree, Branch
from adam.components.Core.AtomicTypes.AtomicPolyline import AtomicCircle
from adam.utils.cadquery_helpers import cq_to_atomicbrep
from adam.components.Intersect.Shape.SolidDifference import solid_difference
from adam.components.Extras.CadqueryPrimitives.CQCylinder import AtomicCQCylinder
import math
import cadquery as cq
from cadquery import Vector as cq_Vector

class CQHollowCylinder(CreateDataTree):
    """
    Call with CQHollowCylinder(center, normal, outer_radius, inner_radius, segments, height, hollow_percent)
    Builds hollow cylinders whose axes pass through `center` and follow `normal`.
    """
    path_mode = 'preserve'

    def compute(self, *branches: Branch, style=None) -> Branch:
        path     = branches[0].path
        centers  = branches[0].elements      # list[AtomicPoint]
        normals  = branches[1].elements      # list[AtomicVector]
        outer_radii    = branches[2].elements      # list[float]
        inner_radii    = branches[3].elements      # list[float]
        segments = branches[4].elements      # list[int]         (can be None)
        heights  = branches[5].elements      # list[float]
        hollow_percents = branches[6].elements      # list[float]


        cylinders = []


        for center, normal, outer_radius, inner_radius, seg, height, hollow_percent in zip(
                centers, normals, outer_radii, inner_radii, segments, heights, hollow_percents):
            
            inner_height = height * hollow_percent

            # offset needed to keep the inner cylinder centred inside the outer one
            half_gap = (height - inner_height) / 2.0        # scalar distance
            n_dir    = normal.normalized()                  # make sure length == 1

            # move along the normal by `half_gap`
            inner_center = AtomicPoint(
                center.x + n_dir.x * half_gap,
                center.y + n_dir.y * half_gap,
                center.z + n_dir.z * half_gap
            )

            cylinder = AtomicCQCylinder(center, normal, outer_radius, seg, height)
            hollow_cylinder = AtomicCQCylinder(inner_center, normal, inner_radius, seg, inner_height)

            result = solid_difference(cylinder, hollow_cylinder)

            cylinders.append(result)

        return Branch(path, cylinders)
