"""Chargement des scripts/partitions (Module 2).

Format défini au Module 0 : solstudio/data/schema_note.json.
"""

import json
from pathlib import Path

CHAMPS_REQUIS = {"note", "corde", "position", "doigt", "duree_temps"}


class MorceauInvalide(Exception):
    """Levée quand un fichier script ne respecte pas le format attendu."""


def charger_morceau(chemin) -> dict:
    """Charge un morceau depuis un fichier JSON et valide sa structure.

    Retourne le dict complet : {"titre": ..., "notes": [ {...}, ... ]}
    """
    chemin = Path(chemin)
    data = json.loads(chemin.read_text(encoding="utf-8"))

    if "notes" not in data or not isinstance(data["notes"], list):
        raise MorceauInvalide("Le fichier doit contenir une liste 'notes'")

    if len(data["notes"]) == 0:
        raise MorceauInvalide("Le morceau ne contient aucune note")

    for i, note in enumerate(data["notes"]):
        manquants = CHAMPS_REQUIS - note.keys()
        if manquants:
            raise MorceauInvalide(f"Note {i} : champs manquants {sorted(manquants)}")

    return data
