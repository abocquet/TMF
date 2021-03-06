###

import matplotlib.pyplot as plt

from simulation.elements.Element import Element
from simulation.elements.ImmutableElement import ImmutableElement
from simulation.elements.MeltSlicedElement import MeltSlicedElement
from simulation.elements.SlicedElement import SlicedElement
from simulation.exchanges.Exchange import Exchange
from simulation.exchanges.SolidExchange import SolidExchange
from simulation.models.Model import Model

import numpy as np

###

# ------------- Définition des grandeurs
nombre_couches = 30
pas_de_temps = 0.01  # s
surface = 100 # m carrés

hauteur_beton_sacrificiel = 10  # metres

temperature_initiale_air = 70 + 273  # ° kelvins
masse_aire = 1000  # kg
densite_air = 0.012
cp_air = 1100 # absurde !!!
conductivite_air = 0.08 # absurde !!!

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
densite_corium = 4600  # absurde !!!
x_corium = 2  # absurde !!!
cp_corium = 1700  # absurde !!!
conductivite_corium = 3  # absurde !!!

# -------------  Simulation


model = Model([
    #Element(temperature_initiale_air, densite_air, masse_aire / densite_air / surface, cp_air, surface, conductivite_air),  # air
    #Exchange(h=coefficient_echange_air_corium, radiations=False),
    #Element(temperature_initiale_corium, densite_corium, x_corium, cp_corium, surface, conductivite_corium, production_chaleur_corium),  # corium
    #SolidExchange(radiations=False),
    #MeltSlicedElement(  # béton sacrificiel
    #    temperature_intiale_beton, masse_volumique_beton,
    #    S=100,  x=10, cp=1.0,
    #    melting_temperature=temperature_fusion_beton,
    #    latent_melting_heat=chaleur_latente_beton,
    #    thermal_conductivity=100,
    #    number_of_slices=10
    #),
    Element(temperature_fusion_beton + 100, densite_corium, x=1,
            cp=cp_corium, S=100, thermal_conductivity=conductivite_corium),
    SolidExchange(),
    #Exchange(h=5e0),
    MeltSlicedElement(
        temperature_intiale_beton + 100, masse_volumique_beton,
        S=100,  x=1, cp=1.0,
        melting_temperature=temperature_fusion_beton,
        latent_melting_heat=chaleur_latente_beton,
        thermal_conductivity=100,
        number_of_slices=10
    )  # béton limite
])

time = model.run(timestep=1e0, time=2*24*3600)

####
#plt.imshow(model.layers[1].history["T"][:, 0::1])
#plt.show()
#plt.plot(time, model.layers[0].slices[0].history["T"])
#plt.plot(time, model.layers[0].slices[-1].history["T"])
plt.plot(time, model.layers[1].slices[0].history["T"])
plt.plot(time, model.layers[1].slices[5].history["T"])
plt.plot(time, model.layers[1].slices[-1].history["T"])
plt.show()
