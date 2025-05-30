import ifcopenshell
import ifcopenshell.api

from .base import IfcSpatialElement

class IfcStorey(IfcSpatialElement):
    def __init__(self, model, *args, **kwargs):
        self.elevation = kwargs.get("elevation", 0.0)
        super().__init__(model, *args, **kwargs)

    def register(self, model, *args, **kwargs):
        self.entity = ifcopenshell.api.root.create_entity(
            model, ifc_class="IfcBuildingStorey", name=self.name
        )
        self.entity.Elevation = self.elevation
        
        building = kwargs.get("building", None)
        if building:
            building.add_child(self)
        else:
            raise ValueError("Building is required")
