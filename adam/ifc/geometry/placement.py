# Placement module
from ifcopenshell.api import geometry

class LocalPlacementHelper:
    @staticmethod
    def create(model, position):
        return geometry.edit_object_placement(model, location=position)
