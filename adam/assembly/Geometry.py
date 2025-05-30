import trimesh


class Geometry:
    def __init__(self, name):
        self.name = name
        self.meshes= []
        self.trimesh_meshes = []
    
    def add_mesh(self, mesh):
        self.meshes.append(mesh)
    
    def add_meshes(self, meshes):
        self.meshes.extend(meshes)
    
    def assemble(self):
        # Collect all trimesh meshes
        for mesh in self.meshes:
            self.trimesh_meshes.append(mesh)
        
        # Combine into a single trimesh.Scene for export
        scene = trimesh.Scene(self.trimesh_meshes)
        return scene
