import matplotlib.pyplot as plt

from simulation.elements.Element import Element
from simulation.elements.MeltSlicedElement import MeltSlicedElement
from simulation.exchanges.Exchange import Exchange
from simulation.exchanges.SolidExchange import SolidExchange
from simulation.models.Model import Model

# ------------- Définition des grandeurs
nombre_couches = 10
pas_de_temps = 30  # s
temps_total = 3600  # s

# Béton
hauteur_beton_sacrificiel = 0.5  # metres
surface_beton = 99
temperature_intiale_beton = 70 + 273  # K
conductivite_beton = 1.9082
temperature_fusion_beton = 1_500  # K
chaleur_latente_beton = 640_000  # J/kg
cp_beton = 1430  # J/kg.K
masse_volumique_beton = 2016  # kg/m3

# Air
temperature_initiale_air = 1450 + 273  # ° kelvins
masse_aire = 1000  # kg
capacite_thermique_air = 1100
conductivite_air = 0.08

# Corium
coefficient_echange_air_corium = 5  # W/(m2.K)
masse_volumique_corium = 4600  # kg/m^3
volume_corium = 59  # m^3
masse_corium = masse_volumique_corium * volume_corium
capacite_thermique_corium = 1500
conductivite_corium = 3

# Acier
temperature_initiale_acier = 343
masse_volumique_acier = 8000
conductivite_thermique_acier = 50
capacite_thermique_acier = 470
surface_acier = 2.4
epaisseur_acier = 0.04

temperature_initiale_corium = 2273
production_chaleur_corium = 35e6

masse_volumique_air = 1.2  # kg/m^3

# -------------  Simulation


model = Model([
    Element(temperature_initiale_air, masse_volumique_air, 6, capacite_thermique_air, surface_beton, conductivite_air,
            0),
    Exchange(h=5, radiations=False),
    Element(temperature_initiale_corium, masse_volumique_corium, volume_corium / surface_beton,
            capacite_thermique_corium, surface_beton, conductivite_corium, production_chaleur_corium),
    SolidExchange(radiations=False),
    MeltSlicedElement(temperature_intiale_beton, masse_volumique_beton, hauteur_beton_sacrificiel, surface_beton,
                      cp_beton, conductivite_beton, 2, temperature_fusion_beton, chaleur_latente_beton, 0, False),
    SolidExchange(radiations=False),
    Element(temperature_initiale_acier, masse_volumique_acier, epaisseur_acier, capacite_thermique_corium,
            surface_acier, conductivite_thermique_acier, 0)

])

time = model.run(timestep=1e0, time=3600 * 10)
plt.plot(time, model.layers[2].history["T"][0])
plt.show()
