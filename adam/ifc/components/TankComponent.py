import ifcopenshell.api.geometry


class TankComponent:
    def __init__(self, model, *args, **kwargs):
        self.model = model
        self.context = kwargs.get("context", None)
        self.body = self.context.body_context
        self.proxy_data = kwargs.get("proxy_data", None)
        self.name = self.proxy_data.get("name", "Unnamed Proxy")
        self.vertices = kwargs.get("vertices", None)
        self.faces = kwargs.get("faces", None)
        

        if not self.context:
            raise ValueError("Context is required")
        self.entity = ifcopenshell.api.root.create_entity(self.model, ifc_class="IfcBuildingElementProxy", name=self.name)

        
        representation = ifcopenshell.api.geometry.add_mesh_representation(self.model, context=self.body, vertices=self.vertices, faces=self.faces)


        # Assign our new body geometry back to our wall
        ifcopenshell.api.geometry.assign_representation(self.model, product=self.entity, representation=representation)




