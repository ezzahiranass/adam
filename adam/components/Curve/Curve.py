


class Curve:
    def get_points(self):
        """Return the points that define or approximate the curve."""
        raise NotImplementedError("Subclasses must implement get_points")

    def serialize(self):
        """Return a JSON-serializable dictionary."""
        raise NotImplementedError("Subclasses must implement serialize")

    def is_closed(self):
        """Return whether the curve is closed."""
        return False
