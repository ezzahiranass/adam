import ifcopenshell
import ifcopenshell.api

from .base import IfcSpatialElement

class IfcBuilding(IfcSpatialElement):
    def register(self, model, *args, **kwargs):
        self.entity = ifcopenshell.api.root.create_entity(model, ifc_class="IfcBuilding", name=self.name)
        
        site = kwargs.get("site", None)
        if site:
            site.add_child(self)
        else:
            raise ValueError("Site is required")
