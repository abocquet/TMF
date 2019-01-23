import numpy as np

from simulation.elements.SlicedElement import SlicedElement


class MeltElement(SlicedElement):

    def __init__(self, T0, density, x, cp, thermal_conductivity, number_of_slices, melting_temperature, energy_production=0, radiations_inside=False):
        SlicedElement.__init__(self, T0, density, x, cp, thermal_conductivity, number_of_slices, energy_production, radiations_inside)

        self.melting_temperature = melting_temperature
        self.number_of_molten_slices = 0  # slice 0 is on top, slice n is on bottom

    def set_prev_exchange(self, prev_exchange):
        self.slices[self.number_of_molten_slices].set_prev_exchange(prev_exchange)

    @property
    def prev_exchange(self):
        return self.slices[self.number_of_molten_slices].prev_exchange

    def calc_next_step(self, dt):
        for slice in self.slices:
            slice.calc_next_step(dt)

    def go_next_state(self):
        for slice in self.slices:
            slice.go_next_state()

    @property
    def history(self):
        return np.array([s.history for s in self.slices])
