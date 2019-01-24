import numpy as np

from simulation.elements.SlicedElement import SlicedElement


class MeltSlicedElement(SlicedElement):

    def __init__(self, T0, density, x, S, cp, thermal_conductivity, number_of_slices, melting_temperature,
                 latent_melting_heat, energy_production=0):
        SlicedElement.__init__(self, T0, density, x, S, cp, thermal_conductivity, number_of_slices, energy_production)

        self.melting_temperature = melting_temperature
        self.latent_metling_heat = latent_melting_heat
        self.number_of_molten_slices = 0  # slice 0 is on top, slice n is on bottom

        self.fusion_energy_acc = 0

    def set_prev_exchange(self, prev_exchange):
        self.slices[self.number_of_molten_slices].set_prev_exchange(prev_exchange)

    @property
    def prev_exchange(self):
        return self.slices[self.number_of_molten_slices].prev_exchange

    def calc_next_step(self, dt):
        if self.number_of_molten_slices == len(self.slices):
            return

        latent_fusion_energy = self.latent_metling_heat * self.slices[0].mass()

        if self.slices[self.number_of_molten_slices].T >= self.melting_temperature:

            molting_slice = self.slices[self.number_of_molten_slices]

            self.fusion_energy_acc += (self.slices[self.number_of_molten_slices].T - self.melting_temperature) * self.slices[0].mass * self.slices[0].cp
            molting_slice.T = self.melting_temperature

            if self.fusion_energy_acc >= latent_fusion_energy:

                absorber = molting_slice.prev_exchange.prev_bloc
                absorber.absorb(molting_slice)


                self.number_of_molten_slices += 1

                if self.number_of_molten_slices == len(self.slices):
                    molting_slice.prev_exchange.prev_bloc.set_next_exchange(molting_slice.next_exchange)

                    molting_slice.prev_exchange = None
                    molting_slice.next_exchange = None

                    assert np.all([s.prev_exchange is None and s.next_exchange is None for s in self.slices])
                else:
                    next_non_molten_slice = self.slices[self.number_of_molten_slices]

                    next_non_molten_slice.set_prev_exchange(molting_slice.prev_exchange)

                    molting_slice.prev_exchange = None
                    molting_slice.next_exchange = None

                self.fusion_energy_acc = 0.0

        for slice in self.slices:
            slice.calc_next_step(dt)

    def go_next_state(self):
        i = 0
        for slice in self.slices:
            print("{} {}".format(i, slice.dT))

            slice.go_next_state()

    @property
    def history(self):
        keys = self.slices[0].history.keys()
        res = {k: [] for k in keys}

        for slice in self.slices:
            for k in keys:
                res[k].append(slice.history[k])

        return res
