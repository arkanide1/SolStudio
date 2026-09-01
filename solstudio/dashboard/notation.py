"""Conversion d'un script SolStudio vers une partition (Module 2, vue notation).

Le script est traduit en notation ABC, un format texte standard pour la
musique. Il n'est jamais affiché tel quel à l'utilisateur : il sert de
donnée d'entrée à la librairie JS abcjs, utilisée par le tableau de bord
Streamlit pour dessiner une vraie portée musicale (noms de notes en
solfège en légende sous les notes, aucune lettre anglo-saxonne visible).
"""

from fractions import Fraction

from solstudio.theorie.cordes import midi_de_la_note

_LETTRES_PAR_DEMI_TON = ["C", "^C", "D", "^D", "E", "F", "^F", "G", "^G", "A", "^A", "B"]
OCTAVE_REFERENCE = 4  # correspond aux lettres majuscules sans marque (Do4-Si4) en ABC


def _midi_vers_pitch_abc(midi: int) -> str:
    lettre = _LETTRES_PAR_DEMI_TON[midi % 12]
    octave = midi // 12 - 1
    decalage = octave - OCTAVE_REFERENCE

    alteration = ""
    base = lettre
    if lettre.startswith("^"):
        alteration = "^"
        base = lettre[1]

    if decalage == 0:
        marque = ""
    elif decalage > 0:
        base = base.lower()
        marque = "'" * (decalage - 1)
    else:
        marque = "," * (-decalage)

    return f"{alteration}{base}{marque}"


def _duree_abc(duree_temps: float) -> str:
    fraction = Fraction(duree_temps).limit_denominator(16)
    if fraction == 1:
        return ""
    if fraction.denominator == 1:
        return str(fraction.numerator)
    if fraction.numerator == 1:
        return f"/{fraction.denominator}"
    return f"{fraction.numerator}/{fraction.denominator}"


def script_vers_abc(script: dict) -> str:
    """Convertit un script SolStudio en notation ABC (texte).

    Attend un script au format défini par solstudio/data/schema_note.json :
    {"titre": ..., "notes": [{"note", "corde", "position", "doigt", "duree_temps"}, ...]}
    """
    entete = [
        "X:1",
        f"T:{script.get('titre', 'Sans titre')}",
        "M:4/4",
        "L:1/4",
        "K:C",
    ]

    tokens_notes = []
    tokens_paroles = []
    for note in script["notes"]:
        midi = midi_de_la_note(note["corde"], note["position"])
        tokens_notes.append(f"{_midi_vers_pitch_abc(midi)}{_duree_abc(note['duree_temps'])}")
        tokens_paroles.append(note["note"])

    ligne_notes = " ".join(tokens_notes) + " |]"
    ligne_paroles = "w: " + " ".join(tokens_paroles)

    return "\n".join(entete + [ligne_notes, ligne_paroles])
