from simulation.elements.ElementMixin import ElementMixin


class Element(ElementMixin):
    def __init__(self, T0, density, x, cp, S, thermal_conductivity, energy_production=0):
        self.T = T0  # temperature
        self.mass = x * S * density
        self.x = x  # thickness
        self.cp = cp  # thermal capacity
        self.energy_production = energy_production
        self.S = S
        self.thermal_conductivity = thermal_conductivity

        self.prev_exchange = None
        self.next_exchange = None

        self.dT = 0.0
        self.__history = {"T": [], "x": [], "cp": [], "mass": []}

    def go_next_state(self):
        self.__history["T"].append(self.T)
        self.__history["x"].append(self.x)
        self.__history["cp"].append(self.cp)
        self.__history["mass"].append(self.mass)
        self.T += self.dT

    def set_prev_exchange(self, prev_exchange):
        self.prev_exchange = prev_exchange
        prev_exchange.next_bloc = self

    def set_next_exchange(self, next_exchange):
        self.next_exchange = next_exchange
        next_exchange.prev_bloc = self

    @property
    def history(self):
        return self.__history

    def calc_next_step(self, dt):
        sigma = 5.70e-8  # sigma de la loi de stephan
        self.dT = 0

        self.dT += self.energy_production * dt

        if self.prev_exchange is not None:
            assert self.prev_exchange.next_bloc == self
            self.dT += self.prev_exchange.h * self.S * (self.prev_exchange.prev_bloc.T - self.T) * dt  # conductivity

            if self.prev_exchange.radiations:
                self.dT += sigma * (self.prev_exchange.prev_bloc.T ** 4 - self.T ** 4) * dt  # radiations

        if self.next_exchange is not None:
            assert self.next_exchange.prev_bloc == self
            self.dT += self.next_exchange.h * self.S * (self.next_exchange.next_bloc.T - self.T) * dt
            if self.next_exchange.radiations:
                self.dT += sigma * (self.next_exchange.next_bloc.T ** 4 - self.T ** 4) * dt

        self.dT /= (self.cp * self.mass)
