from adam.components.Core.DataTree import CreateDataTree, Branch
from adam.components.Core.Style import Style
from adam.components.Core.AtomicTypes.AtomicPolyline import AtomicPolyline
from adam.components.Core.AtomicTypes.AtomicVector import AtomicPoint
from adam.components.Core.AtomicTypes.AtomicBrep import AtomicBrep
from adam.utils.cadquery_helpers import atomicbrep_to_cq, cq_to_atomicbrep

from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from typing import List

import cadquery as cq
from cadquery import Vector, Wire, Face, Shell, Solid


# ─────────────────────────────────────────────────────────────
#  SolidDifference component (fixed, no STEP round-trip)
# ─────────────────────────────────────────────────────────────


def solid_difference(a_brep, b_brep):
    cq_a = atomicbrep_to_cq(a_brep)
    cq_b = atomicbrep_to_cq(b_brep)
    diff_shape = cq_a.cut(cq_b)           # OCC boolean
    return cq_to_atomicbrep(diff_shape)


class SolidDifference(CreateDataTree):
    """Boolean difference: A minus B."""
    path_mode = 'preserve'
    structure_input_index = [0, 1]

    def compute(self, *branches: Branch, style: Style):
        a_breps = branches[0].elements
        b_breps = branches[1].elements
        path    = branches[0].path

        out_breps = []
        for a_brep, b_brep in zip(a_breps, b_breps):
            diff = solid_difference(a_brep, b_brep)
            out_breps.append(diff)

        return Branch(path, out_breps)
