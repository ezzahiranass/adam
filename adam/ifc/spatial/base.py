import ifcopenshell
import ifcopenshell.api.aggregate

# Base module
class IfcSpatialElement:
    def __init__(self, model, *args, **kwargs):
        self.name = kwargs.get("name", "Unnamed Spatial Element")
        self.entity = None
        self.children = []
        self.model = model
        self.register(model, *args, **kwargs)

    def register(self, model, *args, **kwargs):
        raise NotImplementedError("Subclass must implement register()")

    def add_child(self, child, mode="AGGREGATE"):
        self.children.append(child)

        if mode == "AGGREGATE":
            ifcopenshell.api.aggregate.assign_object(
                self.model,
                relating_object=self.entity,
                products=[child.entity]
            )
        elif mode == "CONTAINER":
            ifcopenshell.api.spatial.assign_container(
                self.model, 
                relating_structure=self.entity, 
                products=[child.entity]
            )
        
