###

import matplotlib.pyplot as plt

from simulation.Exchange import Exchange
from simulation.elements.ImmutableElement import ImmutableElement
from simulation.elements.MeltSlicedElement import MeltSlicedElement
from simulation.models.Model import Model

###

# ------------- Définition des grandeurs
nombre_couches = 30
pas_de_temps = 0.01  # s
temps_total = 30  # s

hauteur_beton_sacrificiel = 10  # metres

temperature_initiale_air = 70 + 273  # ° kelvins
masse_aire = 1000  # kg

coefficient_echange_air_corium = 5  # W/(m2.K)

temperature_intiale_beton = temperature_initiale_air
conductivite_beton = 1.9082
temperature_fusion_beton = 1_500  # K
chaleur_latente_beton = 640_000  # J/kg
cp_beton = 1430  # J/kg.K
masse_volumique_beton = 2016  # kg/m3
temperature_frontiere_beton = 70 + 273  # K

temperature_initiale_corium = 273 * 2000
production_chaleur_corium = 30e6

masse_volumique_air = 1.2

# -------------  Simulation


model = Model([
    ImmutableElement(temperature_intiale_beton + temperature_fusion_beton),
    Exchange(h=5, radiations=False),
    MeltSlicedElement(temperature_intiale_beton, masse_volumique_air,
                      S=100,  x=10, cp=1.0,
                      melting_temperature=temperature_fusion_beton,
                      latent_melting_heat=chaleur_latente_beton,
                      thermal_conductivity=0.01,
                      number_of_slices=200)
])

model.run(timestep=1e-2, steps=10 ** 1)

####
plt.imshow(model.layers[1].history["temperature"][:, 0::100])
plt.plot(model.layers[1].history)
plt.show()
