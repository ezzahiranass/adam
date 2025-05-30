import ifcopenshell
import ifcopenshell.api.unit
import ifcopenshell.api.context
import ifcopenshell.api.project
import datetime

class IfcFile:
    def __init__(self, headers: dict, *args, **kwargs):
        # Parse header data with fallbacks
        schema = headers.get("schema", "IFC4X3")
        mvd = headers.get("mvd", "UNKNOWN")
        project_name = headers.get("name", "UNKNOWN")
        author = headers.get("author", "UNKNOWN")
        organization = headers.get("organization", "UNKNOWN")
        originating_system = headers.get("originating_system", "UNKNOWN")
        preprocessor_version = headers.get("preprocessor_version", "UNKNOWN")
        authorization = headers.get("authorization", "UNKNOWN")
        description = headers.get("description", "UNKNOWN")
        implementation_level = headers.get("implementation_level", "2;1")

        # Create IFC model with specified schema
        self.model = ifcopenshell.api.project.create_file(schema)

        # Set up IFC HEADER
        self.model.header.file_description.description = [f"{description} ViewDefinition [{mvd}]"]

        self.model.header.file_description.implementation_level = implementation_level
        self.model.header.file_name.name = f"{project_name}.ifc"
        self.model.header.file_name.time_stamp = datetime.datetime.now().isoformat()
        self.model.header.file_name.author = [author]
        self.model.header.file_name.organization = [organization]
        self.model.header.file_name.originating_system = originating_system
        self.model.header.file_name.preprocessor_version = preprocessor_version
        self.model.header.file_name.authorization = authorization
        self.model.header.file_schema.schema_identifiers = [schema]

        
        
        

        # Track spatial hierarchy
        self.structure_stack = []

    def add(self, spatial_obj):
        spatial_obj.register(self.model)
        if self.structure_stack:
            parent = self.structure_stack[-1]
            parent.add_child(spatial_obj)
        self.structure_stack.append(spatial_obj)
    
    def assign_units(self):
        self.unit_assignment = ifcopenshell.api.unit.assign_unit(self.model)

    def export(self, path: str):
        self.model.write(path)

    def get_model(self):
        return self.model

    def get_context(self):
        return self.body_context
