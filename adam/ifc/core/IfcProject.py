import ifcopenshell
import ifcopenshell.api

class IfcProject:
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init__(*args, **kwargs)
        return instance.project
    
    def __init__(self, model, project_name):
        self.project = ifcopenshell.api.root.create_entity(model, ifc_class="IfcProject", name=project_name)

