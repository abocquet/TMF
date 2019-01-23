from simulation.elements.ElementMixin import ElementMixin


class Element(ElementMixin):
    def __init__(self, T0, density, x, cp, energy_production=0):
        self.T = T0  # temperature
        self.density = density  # density
        self.x = x  # thickness
        self.cp = cp  # thermal capacity
        self.energy_production = energy_production

        self.prev_exchange = None
        self.next_exchange = None

        self.dT = 0.0
        self.__history = []


    def go_next_state(self):
        self.__history.append(self.T)
        self.T += self.dT

    def set_prev_exchange(self, prev_exchange):
        self.prev_exchange = prev_exchange
        prev_exchange.next_bloc = self

    def set_next_exchange(self, next_exchange):
        self.next_exchange = next_exchange
        next_exchange.prev_bloc = self

    @property
    def history(self):
        return list(map(float, self.__history))

    def calc_next_step(self, dt):
        sigma = 5.70e-8  # sigma de la loi de stephan
        self.dT = 0

        self.dT += self.energy_production * dt

        if self.prev_exchange is not None:
            assert self.prev_exchange.next_bloc == self
            self.dT += self.prev_exchange.h * (self.prev_exchange.prev_bloc.T - self.T) * dt  # conductivity

            if self.prev_exchange.radiations:
                self.dT += sigma * (self.prev_exchange.prev_bloc.T ** 4 - self.T ** 4) * dt  # radiations

        if self.next_exchange is not None:
            assert self.next_exchange.prev_bloc == self
            self.dT += self.next_exchange.h * (self.next_exchange.next_bloc.T - self.T) * dt
            if self.next_exchange.radiations:
                self.dT += sigma * (self.next_exchange.next_bloc.T ** 4 - self.T ** 4) * dt

        mass = self.density * self.x
        self.dT /= (self.cp * mass)
