



import cadquery as cq

class _CQProxy:
    """
    Lazy holder that builds the real CadQuery object on first access, then
    caches it.  Accepts a zero-arg builder function.
    """
    def __init__(self, builder):
        self._builder = builder
        self._obj = None

    @property
    def obj(self):
        if self._obj is None:
            self._obj = self._builder()
        return self._obj

