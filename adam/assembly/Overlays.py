import trimesh


class Overlays:
    def __init__(self, name):
        self.name = name
        self.overlays= []
        self.trimesh_overlays = []
    
    def add_overlay(self, overlay):
        self.overlays.append(overlay.overlay)
    
    def add_overlays(self, overlays):
        for overlay in overlays:
            self.add_overlay(overlay)
    
    def assemble(self):
        return self.overlays
