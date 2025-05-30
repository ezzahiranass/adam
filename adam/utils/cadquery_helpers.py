import tempfile
import os
import trimesh
from cadquery import exporters
from adam.components.Core.AtomicTypes.AtomicVector import AtomicPoint
from adam.components.Core.AtomicTypes.AtomicBrep import AtomicBrep
import cadquery as cq
from cadquery import Vector, Wire, Face, Shell, Solid


# ─────────────────────────────────────────────────────────────
#  CadQuery  ➜  AtomicBrep helper
# ─────────────────────────────────────────────────────────────
def cq_to_atomicbrep(shape) -> "AtomicBrep":
    """
    Accepts either a CadQuery Workplane *or* a Shape/Solid.
    Triangulates it and returns an AtomicBrep.
    """
    if isinstance(shape, cq.Workplane):
        shape = shape.val()          # unwrap to Shape/Solid

    # shape is now an OCC shape, safe to tessellate
    verts, tris = shape.tessellate(1e-3)   # returns (verts, faces)
    vertices = [AtomicPoint(*xyz) for xyz in verts]
    return AtomicBrep(vertices=vertices, faces=tris)


# ─────────────────────────────────────────────────────────────
#  AtomicBrep  ➜  CadQuery helper
# ─────────────────────────────────────────────────────────────
def atomicbrep_to_cq(brep) -> cq.Shape:
    """Turn your AtomicBrep (verts, faces) into a CadQuery Shape."""
    vlist = [Vector(p.x, p.y, p.z) for p in brep.vertices]

    face_objs = []
    for poly in brep.faces:                       # poly is list[int]
        wire = Wire.makePolygon([vlist[i] for i in poly] + [vlist[poly[0]]])
        face_objs.append(Face.makeFromWires(wire))

    if len(face_objs) == 1:
        return face_objs[0]                       # just a single Face
    shell = Shell.makeShell(face_objs)
    # If the shell is closed we can promote to a solid:
    if shell.Closed():
        return Solid.makeSolid(shell)
    return shell










def deconstruct_cadquery(brep):
    vertices = []
    faces = []
    # Use a temporary file to store the STL
    with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as tmp_file:
        tmp_path = tmp_file.name

    try:
        # Export to STL file
        exporters.export(brep, tmp_path, exportType='STL')

        # Load with trimesh
        mesh = trimesh.load(tmp_path, file_type='stl')
        verts = mesh.vertices
        _faces = mesh.faces
        for vert in verts:
            v = AtomicPoint(vert[0], vert[1], vert[2])
            vertices.append(v)
        for face in _faces:
            # convert from trackedarray to list
            face = face.tolist()
            faces.append(face)
    finally:
        # Clean up the temp file
        os.remove(tmp_path)

    return verts, faces