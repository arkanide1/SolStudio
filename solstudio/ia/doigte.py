"""Règles de doigté : choisit une corde et une position pour une note MIDI
donnée (Module 3, étape 3.2).

Aucun modèle d'IA ne fournit la corde/position directement à partir de
l'audio (cf. cahier des charges M3) : c'est une règle codée à la main.

Simplification V1 : position = nombre de demi-tons au-dessus de la corde
à vide, doigt = position plafonnée à 4 (auriculaire). Ce n'est pas toujours
le doigté pédagogiquement idéal, mais donne un point de départ exploitable.
"""

from solstudio.theorie.cordes import ORDRE_CORDES, midi_de_la_note

POSITION_MAX = 12  # limite raisonnable sur le manche pour la V1


def choisir_corde_et_position(midi_note: int):
    """Retourne (corde, position) pour la note MIDI donnée, ou None si la
    note est hors du registre couvert par les 4 cordes en 1ère à ~5e position.

    Parmi les cordes physiquement valides, choisit la position la plus basse
    (la plus proche d'une corde à vide).
    """
    candidats = []
    for corde in ORDRE_CORDES:
        position = midi_note - midi_de_la_note(corde, 0)
        if 0 <= position <= POSITION_MAX:
            candidats.append((corde, position))

    if not candidats:
        return None

    candidats.sort(key=lambda cp: cp[1])
    return candidats[0]


def position_vers_doigt(position: int) -> int:
    return max(0, min(position, 4))
