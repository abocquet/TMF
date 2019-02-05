###########################
# Imports
###########################
import sys

import matplotlib.pyplot as plt
import numpy as np

from simulation.elements.Element import Element
from simulation.elements.MeltSlicedElement import MeltSlicedElement
from simulation.exchanges.Exchange import Exchange
from simulation.exchanges.SolidExchange import SolidExchange
from simulation.models.Model import Model

###########################
#  Définition des grandeurs
###########################


nombre_couches_beton = 100
timestep = 1e0  # 1/s
simulation_time = 3600 * 20  # s

# Béton
hauteur_beton_sacrificiel = 0.5  # metres
surface_beton = 99
temperature_intiale_beton = 70 + 273  # K
conductivite_beton = 1.9082
temperature_fusion_beton = 1500  # K
chaleur_latente_beton = 640000  # J/kg
masse_beton = 100000
capacite_thermique_beton = 1430
volume_beton = hauteur_beton_sacrificiel * surface_beton
masse_volumique_beton = masse_beton / volume_beton

# Air
temperature_initiale_air = 1450 + 273  # ° kelvins
masse_air = 1000  # kg
capacite_thermique_air = 1100
conductivite_air = 0.08
masse_volumique_air = 1.2  # kg/m^3
hauteur_air = masse_air / masse_volumique_air / surface_beton

# Corium
coefficient_echange_air_corium = 5  # W/(m2.K)
masse_volumique_corium = 4600  # kg/m^3
volume_corium = 59  # m^3
masse_corium = 271e3
capacite_thermique_corium = lambda t: 1000 if t <= 1700 else (1700 if t <= 2200 else 800)
#conductivite_corium = lambda t: 0.001 * t + 1 if t <= 1600 else (0.001 * t + 1 if t <= 2000 else 0.0067 * t - 10.333)
conductivite_corium = lambda t: 0.000875 * (t - 1200) + 2.3 if t <= 2000 else 0.0066666667 * (t - 2000) + 3
hauteur_corium = masse_corium / masse_volumique_corium / surface_beton

temperature_initiale_corium = 2273
# production_chaleur_corium = 35e6

T0 = 365  # jours de fonctionnement du réacteur avant incident
production_chaleur_corium = lambda time, T=None: 6.48e-3 * 4500e6 * (
            (time / (3600 * 24)) ** -0.2 - ((time / (3600 * 24)) + T0) ** -0.2)

# Acier
temperature_initiale_acier = 343
temperature_fusion_acier = 1500
masse_volumique_acier = 8000
conductivite_thermique_acier = 50
capacite_thermique_acier = 470
surface_acier = 2.4
epaisseur_acier = 0.04
volume_acier = surface_acier * epaisseur_acier
masse_acier = masse_volumique_acier * volume_acier

######################################################
# Simulation fonte dans la cuve de rétention
######################################################

model = Model([
    Element(temperature_initiale_air, masse_volumique_air, 3, capacite_thermique_air, surface_beton, conductivite_air),
    Exchange(h=5 * 99, radiations=False, prev_temp_radiation=1500),
    Element(temperature_initiale_corium, masse_volumique_corium, volume_corium / surface_beton,
            capacite_thermique_corium, surface_beton, conductivite_corium, production_chaleur_corium),
    SolidExchange(radiations=False),
    MeltSlicedElement(
        temperature_intiale_beton, masse_volumique_beton,
        hauteur_beton_sacrificiel, surface_beton,
        capacite_thermique_beton, conductivite_beton, nombre_couches_beton,
        temperature_fusion_beton, chaleur_latente_beton, 0),
    SolidExchange(radiations=False),
    Element(temperature_initiale_acier, masse_volumique_acier, epaisseur_acier, capacite_thermique_acier,
            surface_acier, conductivite_thermique_acier, 0)
])

time = model.run(
    timestep=timestep, time=simulation_time,
    time_offset=0.0,
    early_interrupt=lambda s: s.layers[-1].history["T"][-1] > temperature_fusion_acier + 150
)

# Résultats

T1 = np.argmax(np.array(model.layers[-1].history["T"]) > temperature_fusion_acier) * timestep
T1 = len(model.layers[-1].history["T"]) * timestep
T1_h, T1_m, T1_s = int(T1 / 3600), int((T1 % 3600) / 60), int(T1 % 60)
print("\nTemps final avant fonte {}h {}m {}s (={}s)".format(T1_h, T1_m, T1_s, T1))
print(T1)

#plt.plot(time, model.layers[1].history["thermal_conductivity"], label="Lambda mélange corium béton")
#plt.plot(time, np.vectorize(conductivite_corium)(model.layers[1].history["T"]), label="Lambda corium seul")
#plt.title("Conductivité thermique du corium en fonction du temps")
#plt.legend()
#plt.show()
#sys.exit()

plt.plot(time, model.layers[0].history["T"], label="Air")
plt.plot(time, model.layers[1].history["T"], label="Corium")

i0 = 3
for i in range(i0):
    h = model.layers[2].history["T"][int(i / i0 * nombre_couches_beton)]
    t, h = zip(*[(ti, hi) for ti, hi in zip(time, h) if hi <= temperature_fusion_beton + 10])

    plt.plot(t, h, "g")

plt.plot(time, model.layers[2].slices[-1].history["T"])

plt.plot(time, model.layers[3].history["T"], "r", label="Plaque de métal")
plt.legend()
plt.title("Evolution des grandeurs dans la cuve de rétention")
plt.xlabel("Temps écoulé (s)")
plt.ylabel("Température (K)")
plt.show()

pix_beton = len(model.layers[2].slices) * 100
pix_air, pix_corium, pix_acier = int(0.1 * pix_beton), int(0.3 * pix_beton), int(0.1 * pix_beton)
ticks = [0]
ticks += [ticks[-1] + pix_acier]
ticks += [ticks[-1] + pix_beton]
ticks += [ticks[-1] + pix_corium]
ticks += [ticks[-1] + pix_air]

plt.imshow(
    np.vstack((
        np.tile(model.layers[0].history["T"], (pix_air, 1)),
        np.tile(model.layers[1].history["T"], (pix_corium, 1)),
        np.repeat(model.layers[2].history["T"], 100, axis=0),
        np.tile(model.layers[3].history["T"], (pix_acier, 1)),
    )),
    extent=[0, T1 / 3600, 0, ticks[-1]], aspect='auto'
)
plt.colorbar()
plt.title("Profil de température verticale dans la cuve de rétention")
plt.xlabel("Temps écoulé (h)")
plt.yticks(ticks, labels=reversed(["Air", "Corium", "Béton sacrificiel", "Plaque acier", "Fin"]))
plt.show()

sys.exit()

######################################################
# Mise à jour des grandeurs pour la seconde simulation
######################################################

surface_zone_etalement = 170
profondeur_cables = 0.1  # m
hauteur_beton_sacrificiel_zone_etalement = profondeur_cables * 2
nombre_couches_beton_zone_etalement = 100
hauteur_air_zone_etalement = 10

corium_element = model.layers[1]
temperature_initiale_corium_zone_etalement = corium_element.T
masse_corium_zone_etalement = masse_corium + masse_beton + masse_acier
volume_corium_zone_etalement = volume_corium + volume_beton + volume_acier
masse_volumique_corium_zone_etalement = masse_corium_zone_etalement / volume_corium_zone_etalement
hauteur_corium_zone_etalement = volume_corium_zone_etalement / surface_zone_etalement

######################################################
# Simulation fonte dans la zone d'étalement
######################################################

model = Model([
    Element(temperature_initiale_air, masse_volumique_air, hauteur_air_zone_etalement, capacite_thermique_air,
            surface_beton, conductivite_air),
    Exchange(h=5 * 99),
    Element(temperature_initiale_corium_zone_etalement, masse_volumique_corium_zone_etalement,
            hauteur_corium_zone_etalement,
            capacite_thermique_corium, surface_zone_etalement, conductivite_corium, production_chaleur_corium),
    SolidExchange(radiations=False),
    MeltSlicedElement(
        temperature_intiale_beton, masse_volumique_beton,
        hauteur_beton_sacrificiel_zone_etalement, surface_zone_etalement,
        capacite_thermique_beton, conductivite_beton, nombre_couches_beton_zone_etalement,
        temperature_fusion_beton, chaleur_latente_beton,
        0
    ),
])

time = model.run(
    timestep=timestep, time=simulation_time,
    time_offset=T1,
    early_interrupt=lambda s: s.layers[2].slices[int(
        nombre_couches_beton_zone_etalement * (0.5 + 1 / 3))].T >= temperature_fusion_beton - 1
)

# Résultats

T2 = np.argmax(np.array(model.layers[2].slices[nombre_couches_beton_zone_etalement // 2 + 1].history[
                            "T"]) >= temperature_fusion_beton - 1) * timestep
T2_h, T2_m, T2_s = int(T2 / 3600), int((T2 % 3600) / 60), int(T2 % 60)
print("\nTemps final avant fonte {}h {}m {}s (={}s)".format(T2_h, T2_m, T2_s, T2))

plt.plot(time, model.layers[0].history["T"], label="Air")
plt.plot(time, model.layers[1].history["T"], label="Corium")

i0 = 3
for i in range(i0):
    h = model.layers[2].history["T"][int(i / i0 * nombre_couches_beton_zone_etalement)]
    t, h = zip(*[(ti, hi) for ti, hi in zip(time, h) if hi <= temperature_fusion_beton + 10])

    plt.plot(t, h, "g")

plt.legend()
plt.title("Evolution des grandeurs dans la zone d'étalement")
plt.xlabel("Temps écoulé (s)")
plt.ylabel("Température (K)")
plt.show()

pix_beton = len(model.layers[2].slices) * 100
pix_air, pix_corium = int(0.1 * pix_beton), int(0.3 * pix_beton)
ticks = [0]
ticks += [ticks[-1] + pix_beton]
ticks += [ticks[-1] + pix_corium]
ticks += [ticks[-1] + pix_air]

plt.imshow(
    np.vstack((
        np.tile(model.layers[0].history["T"], (pix_air, 1)),
        np.tile(model.layers[1].history["T"], (pix_corium, 1)),
        np.repeat(model.layers[2].history["T"], 100, axis=0),
    )),
    extent=[0, T2 / 3600, 0, ticks[-1]], aspect='auto'
)

plt.colorbar()
plt.title("Profil de température verticale dans la zone d'étalement")
plt.xlabel("Temps écoulé (h)")
plt.yticks(ticks, labels=reversed(["Air", "Corium", "Béton sacrificiel", "Fin"]))
plt.show()
