class ImmutableElement:

    def __init__(self, T0):
        self.T = T0
        self.history = {"T": []}

    def calc_next_step(self, _):
        pass

    def go_next_state(self):
        self.history["T"].append(self.T)

    def set_next_exchange(self, _):
        pass

    def set_prev_exchange(self, _):
        pass
