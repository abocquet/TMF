# -*- coding: utf-8 -*-
"""# Caractéristiques des matériaux

Caractéristiques du corium et du zircone
"""

# Définition des constantes
corium = {
    "masse_volumique": 4570,  # kg/m3
    "viscosite": 15,  # Pa.s
    "coeff_transfert_thermique": 12,  # W/(m.k)
    "capacite_thermique": 1500  # J/(kg.K)
}

corium["prandtl"] = corium["viscosite"] * corium["capacite_thermique"] / corium["coeff_transfert_thermique"]

air = {
    "masse_volumique": 1.2,  # kg/m3
    "viscosite": 2e-5,  # Pa.s - https://www.google.com/search?q=quelle+est+la+viscosit%C3%A9+de+l%27air
    "coeff_transfert_thermique": 0.040,  # W/(m.k) - hypothèse défavorable
    "capacite_thermique": 1004,  # J/(kg.K)
    "prandtl": 0.7
}

zircone = {
    "conductivite_thermique": 2,
    "epaisseur": 0.23
}

# air["prandtl"] = air["viscosite"] * air["capacite_thermique"] / air["coeff_transfert_thermique"]


def reynolds(v, materiau, longueur):
    """v = vitesse en m/s"""
    return materiau["masse_volumique"] * v * longueur / materiau["viscosite"]

def grely(materiau, longueur, t_fluide, t_surface):
    return 9.81 * abs(t_fluide - t_surface) * (longueur ** 3) * (materiau["masse_volumique"] ** 2) / (
                t_fluide * (materiau["viscosite"] ** 2))


def h(materiau, longueur, geometrie="ouverte", ecoulement="laminaire", convection="naturelle", v=None, t_fluide=None,
      t_surface=None):
    """
      v = vitesse en m/s
      h = le coefficient d'échange thermique
     """

    if [geometrie, ecoulement, convection] == ["ouverte", "laminaire", "forcee"]:
        assert v != None
        assert t_fluide != None
        assert t_surface != None
        return (0.453 * reynolds(v, materiau, longueur) ** 0.5 * materiau["prandtl"] ** 0.33 * materiau[
            "coeff_transfert_thermique"] / longueur) ** 0.5

    if [geometrie, ecoulement, convection] == ["ouverte", "laminaire", "naturelle"]:
        Pr, Gr = materiau["prandtl"], grely(materiau, longueur, t_fluide, t_surface)

        assert t_fluide != None
        assert t_surface != None

        if 1e5 <= Gr * Pr <= 1e7:
            return materiau["coeff_transfert_thermique"] / longueur * 0.54 * (Gr * Pr) ** 0.25
        elif 1e7 <= Gr * Pr <= 3e15:
            return (materiau["coeff_transfert_thermique"] / longueur) * 0.14 * (Gr * Pr) ** 0.33
        else:
            raise Exception("Gr*Pr out of bounds: {}".format(Gr * Pr))

    raise Exception("Case not handled yet")


def biot(h, L, lam):
    """
      h - coefficient global de transfert thermique
      L - longueur caractéristique
      lam - conductivité thermique du corps
    """
    return h * L / lam
