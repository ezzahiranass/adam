import ifcopenshell
import ifcopenshell.api.context


class IfcContext:
    def __init__(self, model, name):
        self.model = model
        self.context = ifcopenshell.api.context.add_context(self.model, context_type="Model")
        self.body_context = ifcopenshell.api.context.add_context(
            self.model,
            context_type="Model",
            context_identifier="Body",
            target_view="MODEL_VIEW",
            parent=self.context
        )
