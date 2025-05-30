








class NumberSlider:
    def __init__(self, min, max, step, default_value):
        self.min = min
        self.max = max
        self.step = step
        self.default_value = default_value
        self.value = default_value

    def set_value(self, value):
        self.value = value

