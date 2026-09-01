"""Conversion des segments transcrits vers le format script SolStudio
(Module 3, étape 3.3 -> format défini au Module 0).
"""

import json
from pathlib import Path

from solstudio.ia.doigte import choisir_corde_et_position, position_vers_doigt
from solstudio.theorie.solfege import freq_vers_note


def segments_vers_script(segments: list[dict], titre: str = "Transcription automatique") -> dict:
    """Convertit une liste de segments {"freq", "duree_s", ...} en script
    SolStudio (même format que solstudio/data/schema_note.json).

    Les notes hors du registre couvert par les 4 cordes (1ère à ~5e
    position) sont ignorées pour cette V1.
    """
    notes = []
    for segment in segments:
        info_note = freq_vers_note(segment["freq"])
        choix = choisir_corde_et_position(info_note["midi"])
        if choix is None:
            continue
        corde, position = choix
        notes.append({
            "note": info_note["note"],
            "corde": corde,
            "position": position,
            "doigt": position_vers_doigt(position),
            "duree_temps": round(max(0.25, segment.get("duree_s", 0.5)), 2),
        })

    return {"titre": titre, "notes": notes}


def exporter_script(script: dict, chemin) -> None:
    Path(chemin).write_text(json.dumps(script, ensure_ascii=False, indent=2), encoding="utf-8")
