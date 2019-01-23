import numpy as np

from simulation.Exchange import Exchange
from simulation.elements.Element import Element
from simulation.elements.ElementMixin import ElementMixin


class SlicedElement(ElementMixin):

    def __init__(self, T0, density, x, S, cp, thermal_conductivity, number_of_slices, energy_production=0, radiations_inside=False):
        self.slices = []

        for i in range(number_of_slices):
            self.slices.append(Element(T0, density, x / number_of_slices, cp, S, thermal_conductivity, energy_production))

        for i in range(0, number_of_slices - 1):
            e = Exchange(h=thermal_conductivity, radiations=radiations_inside)
            self.slices[i].set_next_exchange(e)
            self.slices[i+1].set_prev_exchange(e)

    def set_prev_exchange(self, prev_exchange):
        self.slices[0].set_prev_exchange(prev_exchange)

    def set_next_exchange(self, next_exchange):
        self.slices[-1].set_next_exchange(next_exchange)

    @property
    def next_exchange(self):
        return self.slices[-1].next_exchange

    @property
    def prev_exchange(self):
        return self.slices[0].prev_exchange

    def calc_next_step(self, dt):
        for slice in self.slices:
            slice.calc_next_step(dt)

    def go_next_state(self):
        for slice in self.slices:
            slice.go_next_state()

    @property
    def history(self):
        keys = self.slices[0].history.keys()
        res = {k: [] for k in keys}

        for slice in self.slices:
            for k in keys:
                res[k].append(slice.history[k])

        for k in keys:
            res[k] = np.array(res[k])

        return res
