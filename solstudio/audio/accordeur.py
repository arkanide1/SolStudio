"""Logique de l'accordeur : fréquence détectée -> statut en solfège (Module 1)."""

from solstudio.theorie.cordes import corde_la_plus_proche, ecart_par_rapport_a_vide
from solstudio.theorie.solfege import freq_vers_note

SEUIL_JUSTE_CENTS = 5.0


def analyser_frequence(freq: float | None) -> dict:
    """Construit le statut complet de l'accordeur pour une fréquence donnée.

    "direction" indique au joueur quoi faire avec le doigt :
    - "juste"     : la note est correctement accordée (± 5 cents)
    - "descendre" : le son est trop haut, reculer le doigt vers le sillet
    - "monter"    : le son est trop bas, avancer le doigt vers le chevalet
    """
    if freq is None:
        return {"detecte": False}

    info_note = freq_vers_note(freq)
    cents = info_note["cents"]
    corde = corde_la_plus_proche(freq)
    ecart_corde = ecart_par_rapport_a_vide(freq, corde)

    if abs(cents) < SEUIL_JUSTE_CENTS:
        direction = "juste"
    elif cents > 0:
        direction = "descendre"
    else:
        direction = "monter"

    return {
        "detecte": True,
        "freq": round(freq, 2),
        "note": info_note["note"],
        "octave": info_note["octave"],
        "cents": cents,
        "corde": corde,
        "ecart_corde_cents": ecart_corde,
        "direction": direction,
    }
