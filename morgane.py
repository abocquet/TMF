import matplotlib.pyplot as plt

from simulation.Exchange import Exchange
from simulation.elements.Element import Element
from simulation.elements.MeltSlicedElement import MeltSlicedElement
from simulation.elements.SlicedElement import SlicedElement
from simulation.models.Model import Model

# ------------- Définition des grandeurs
nombre_couches = 10
pas_de_temps = 30  # s
temps_total = 3600  # s

# Béton
hauteur_beton_sacrificiel = 0.5  # metres


# Air
temperature_initiale_air = 1450 + 273  # ° kelvins
masse_aire = 1000  # kg
capacite_thermique_air = 1100
conductivite_air = 0,08

# Corium
coefficient_echange_air_corium = 5  # W/(m2.K)
masse_volumique_corium = 4600 # kg/m^3
volume_corium = 59 # m^3
masse_corium = masse_volumique_corium * volume_corium
capacite_thermique_corium = 1500
conductivite_corium = 3


surface_beton = 99
temperature_intiale_beton = temperature_initiale_air
conductivite_beton = 1.9082
temperature_fusion_beton = 1_500  # K
chaleur_latente_beton = 640_000  # J/kg
cp_beton = 1430  # J/kg.K
masse_volumique_beton = 2016  # kg/m3
temperature_frontiere_beton = 70 + 273  # K

temperature_initiale_corium = 2273
production_chaleur_corium = 30e6

masse_volumique_air = 1.2 # kg/m^3

#-------------  Simulation


model = Model([
    MeltSlicedElement(conductivite_corium
                      )
    Element(temperature_initiale_air, masse_volumique_air, 6, capacite_thermique_air , surface_beton, conductivite_air,0),
    Exchange()
    Element(temperature_initiale_corium, masse_volumique_corium, volume_corium/ surface_beton,capacite_thermique_corium, surface_beton, conductivite_corium, 35),
    Exchange(h=5, radiations=False),

])

model.run(timestep=1e-2, steps=10**4)

#plt.imshow(model.layers[0].history["T"][:, 0::100])
#plt.plot(model.layers[1].history)
#plt.show()

print(model.layers[0].history["T"])