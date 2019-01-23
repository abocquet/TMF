###

import matplotlib.pyplot as plt

from simulation.elements.Element import Element
from simulation.elements.ImmutableElement import ImmutableElement
from simulation.elements.MeltSlicedElement import MeltSlicedElement
from simulation.exchanges.Exchange import Exchange
from simulation.exchanges.SolidExchange import SolidExchange
from simulation.models.Model import Model

###

# ------------- Définition des grandeurs
nombre_couches = 30
pas_de_temps = 0.01  # s
surface = 100 # m carrés

hauteur_beton_sacrificiel = 10  # metres

temperature_initiale_air = 70 + 273  # ° kelvins
masse_aire = 1000  # kg
densite_air = 0.012
cp_air = 1 # absurde !!!
conductivite_air = 1 # absurde !!!

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
densite_corium = 100  # absurde !!!
x_corium = 2  # absurde !!!
cp_corium = 23  # absurde !!!
conductivite_corium = 0.3  # absurde !!!

# -------------  Simulation


model = Model([
    Element(temperature_initiale_air, densite_air, masse_aire / densite_air / surface, cp_air, surface, conductivite_air),  # air
    Exchange(h=coefficient_echange_air_corium, radiations=False),
    Element(temperature_initiale_corium, densite_corium, x_corium, cp_corium, surface, conductivite_corium, production_chaleur_corium),  # corium
    SolidExchange(radiations=True),
    MeltSlicedElement(  # béton sacrificiel
        temperature_intiale_beton, masse_volumique_beton,
        S=100,  x=10, cp=1.0,
        melting_temperature=temperature_fusion_beton,
        latent_melting_heat=chaleur_latente_beton,
        thermal_conductivity=0.01,
        number_of_slices=200,
        radiations_inside=True
    ),
    SolidExchange(radiations=False),
    ImmutableElement(temperature_intiale_beton)  # béton limite
])

model.run(timestep=1e-2, steps=10 ** 3)

####
plt.imshow(model.layers[1].history["T"][:, 0::1])
plt.show()
plt.plot(model.layers[0].history["T"])
plt.show()
