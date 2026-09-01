"""Référentiel des cordes du violon, en solfège uniquement (Module 0).

Jamais G/D/A/E dans le reste de l'application : uniquement Sol, Ré, La, Mi.
"""

from .solfege import freq_vers_midi

# Fréquences à vide standard (tempérament égal, La4 = 440 Hz).
CORDES = {
    "Sol": {"freq": 196.00, "octave": 3},
    "Ré": {"freq": 293.66, "octave": 4},
    "La": {"freq": 440.00, "octave": 4},
    "Mi": {"freq": 659.25, "octave": 5},
}

# Ordre du grave à l'aigu, utilisé pour la reconnaissance de corde.
ORDRE_CORDES = ["Sol", "Ré", "La", "Mi"]


def corde_la_plus_proche(freq: float) -> str:
    """Détermine la corde la plus probable pour une fréquence jouée.

    Heuristique simple pour la V1 (Module 0) : chaque corde couvre les
    fréquences depuis sa corde à vide jusqu'à un peu avant la corde à vide
    suivante. Le Module 1 pourra affiner cette logique (position réelle du
    doigt, timbre, etc.).
    """
    if freq <= 0:
        raise ValueError("La fréquence doit être positive")

    cordes_triees = sorted(ORDRE_CORDES, key=lambda c: CORDES[c]["freq"])

    corde_choisie = cordes_triees[0]
    for corde in cordes_triees:
        seuil_bas = CORDES[corde]["freq"] * 0.97  # tolérance légère vers le grave
        if freq >= seuil_bas:
            corde_choisie = corde
    return corde_choisie


def ecart_par_rapport_a_vide(freq: float, corde: str) -> float:
    """Écart en cents entre la fréquence jouée et la corde à vide donnée."""
    if corde not in CORDES:
        raise ValueError(f"Corde inconnue : {corde!r}")
    midi_joue = freq_vers_midi(freq)
    midi_vide = freq_vers_midi(CORDES[corde]["freq"])
    return round((midi_joue - midi_vide) * 100.0, 1)


def midi_de_la_note(corde: str, position: int) -> int:
    """MIDI de la note jouée sur une corde à une position donnée (nombre de
    demi-tons au-dessus de la corde à vide)."""
    if corde not in CORDES:
        raise ValueError(f"Corde inconnue : {corde!r}")
    return round(freq_vers_midi(CORDES[corde]["freq"])) + position
