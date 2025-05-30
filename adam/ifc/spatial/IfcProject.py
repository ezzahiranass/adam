from .base import IfcSpatialElement
import ifcopenshell
import ifcopenshell.api.root

class IfcProject(IfcSpatialElement):
    def register(self, model, *args, **kwargs):
        self.entity = ifcopenshell.api.root.create_entity(model, ifc_class="IfcProject", name=self.name)
