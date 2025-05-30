




def stylize(geom, style=None):
    obj = geom.serialize()
    if style:
        obj.update(style.serialize())
    return obj




class Style:
    def __init__(self, strokeColor="black", strokeWidth=1):
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth

    def serialize(self):
        return {
            "stroke": self.strokeColor, 
            "strokeWidth": self.strokeWidth
            }
