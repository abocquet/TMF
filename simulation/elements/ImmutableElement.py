class ImmutableElement:

    def __init__(self, T0):
        self.T = T0
        self.history = []

    def calc_next_next(self, dt):
        pass

    def go_next_step(self, dt):
        self.history.append(self.T)
