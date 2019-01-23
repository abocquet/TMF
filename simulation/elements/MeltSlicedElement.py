import numpy as np

from simulation.elements.SlicedElement import SlicedElement


class MeltSlicedElement(SlicedElement):

    def __init__(self, T0, density, x, S, cp, thermal_conductivity, number_of_slices, melting_temperature,
                 latent_melting_heat, energy_production=0, radiations_inside=False):
        SlicedElement.__init__(self, T0, density, x, S, cp, thermal_conductivity, number_of_slices, energy_production,
                               radiations_inside)

        self.melting_temperature = melting_temperature
        self.latent_metling_heat = latent_melting_heat
        self.number_of_molten_slices = 0  # slice 0 is on top, slice n is on bottom

    def set_prev_exchange(self, prev_exchange):
        self.slices[self.number_of_molten_slices].set_prev_exchange(prev_exchange)

    @property
    def prev_exchange(self):
        return self.slices[self.number_of_molten_slices].prev_exchange

    def calc_next_step(self, dt):
        latent_fusion_energy = self.latent_metling_heat * self.slices[0].mass

        if self.slices[self.number_of_molten_slices].T >= self.melting_temperature + latent_fusion_energy:
            molten_slice = self.slices[self.number_of_molten_slices]
            absorber = molten_slice.prev_exchange.prev_bloc

            absorber.mass += molten_slice.mass
            absorber.cp = (absorber.cp * absorber.mass + molten_slice.cp * molten_slice.mass) / (
                        absorber.mass + molten_slice.mass)

            self.number_of_molten_slices += 1
            next_non_molten_slice = self.slices[self.number_of_molten_slices]

            next_non_molten_slice.set_prev_exchange(molten_slice.prev_exchange)

            molten_slice.prev_exchange = None
            molten_slice.next_exchange = None

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

        return res
