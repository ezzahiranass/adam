import ifcopenshell
import ifcopenshell.api

from .base import IfcSpatialElement

class IfcSite(IfcSpatialElement):
    def register(self, model, *args, **kwargs):
        self.entity = ifcopenshell.api.root.create_entity(model, ifc_class="IfcSite", name=self.name)

        
        project = kwargs.get("project", None)
        if project:
            project.add_child(self)
        else:
            raise ValueError("Project is required")

