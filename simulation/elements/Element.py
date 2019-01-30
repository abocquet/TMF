from simulation.elements.ElementMixin import ElementMixin


class Element(ElementMixin):
    def __init__(self, T0, density, x, cp, S, thermal_conductivity, energy_production=0):
        self.T = T0  # temperature
        self.S = S
        self.__mass = x * S * density
        self.__x = x  # thickness
        self.__cp = cp  # thermal capacity
        self.__energy_production = energy_production
        self.__thermal_conductivity = thermal_conductivity

        self.absorbed = []
        self.absorbed_by = None

        self.prev_exchange = None
        self.next_exchange = None

        self.dT = 0.0
        self.__history = {
            "T": [], "x": [], "cp": [], "mass": [],
            "thermal_conductivity": [], "energy_production": []
        }

    def go_next_state(self):
        self.__history["T"].append(self.T if self.absorbed_by is None else self.absorbed_by.T)
        self.__history["x"].append(self.x())
        self.__history["cp"].append(self.cp())
        self.__history["mass"].append(self.mass())
        self.__history["thermal_conductivity"].append(self.thermal_conductivity())
        self.T += self.dT

    def set_prev_exchange(self, prev_exchange):
        self.prev_exchange = prev_exchange
        prev_exchange.next_bloc = self

    def set_next_exchange(self, next_exchange):
        self.next_exchange = next_exchange
        next_exchange.prev_bloc = self

    def absorb(self, bloc):
        self.T = (self.T * self.cp() * self.mass() + bloc.T * bloc.cp() * bloc.mass()) / (bloc.cp() * bloc.mass() + self.cp() * self.mass())
        self.absorbed.append(bloc)
        bloc.absorbed_by = self

    @property
    def history(self):
        return self.__history

    def mass(self):
        return self.__mass +  sum([a.__mass for a in self.absorbed])

    def x(self):
        return self.__x + sum([a.x() for a in self.absorbed])


    def energy_production(self, time, T=None):
        if T is None:
            T = self.T

        res = self.__energy_production(time, T) if callable(self.__energy_production) else self.__energy_production
        res += sum([a.energy_production(time, T) for a in self.absorbed])

        return res

    def cp(self, T=None):
        if T is None:
            T = self.T

        res =  self.__mass * (self.__cp(T) if callable(self.__cp) else self.__cp)
        res += sum([a.cp(T) * a.mass() for a in self.absorbed])

        res /= self.__mass + sum([a.mass() for a in self.absorbed])

        return res

    def thermal_conductivity(self, T=None):
        if T is None:
            T = self.T

        res = self.__mass * (self.__thermal_conductivity(T) if callable(self.__thermal_conductivity) else self.__thermal_conductivity)
        res += sum([a.thermal_conductivity(T) * a.mass() for a in self.absorbed])

        res /= self.__mass + sum([a.mass() for a in self.absorbed])

        return res

    def calc_next_step(self, dt, time):
        self.__history["energy_production"].append(self.energy_production(time))

        sigma = 5.70e-8  # sigma de la loi de stephan
        self.dT = 0.0

        self.dT += self.energy_production(time)

        if self.prev_exchange is not None:
            assert self.prev_exchange.next_bloc == self

            self.dT += self.prev_exchange.h * (self.prev_exchange.prev_bloc.T - self.T)  # conductivity

            if self.prev_exchange.radiations:
                self.dT += sigma * (self.prev_exchange.prev_bloc.T ** 4 - self.T ** 4)  # radiations
            elif self.prev_exchange.prev_temp_radiation:
                self.dT += sigma * (self.prev_exchange.prev_temp_radiation ** 4 - self.T ** 4)

        if self.next_exchange is not None:
            assert self.next_exchange.prev_bloc == self

            self.dT += self.next_exchange.h * (self.next_exchange.next_bloc.T - self.T)

            if self.next_exchange.radiations:
                self.dT += sigma * (self.next_exchange.next_bloc.T ** 4 - self.T ** 4)
            elif self.next_exchange.next_temp_radiation:
                self.dT += sigma * (self.next_exchange.next_temp_radiation ** 4 - self.T ** 4)

        self.dT *= dt
        self.dT /= (self.cp() * self.mass())
