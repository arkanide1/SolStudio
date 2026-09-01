"""CLI du Module 3 : transcrire de l'audio en script, ou écouter un script.

Usage:
    python -m solstudio.ui.ia_cli transcrire chemin_audio.wav sortie_script.json
    python -m solstudio.ui.ia_cli ecouter chemin_script.json sortie_audio.wav
"""

import sys
from pathlib import Path

from solstudio.audio.lecture import jouer_wav
from solstudio.dashboard.script import charger_morceau
from solstudio.ia.conversion import exporter_script, segments_vers_script
from solstudio.ia.synthese import synthetiser_script
from solstudio.ia.transcription import transcrire_fichier_audio


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return

    commande = sys.argv[1]

    if commande == "transcrire":
        chemin_audio, chemin_sortie = sys.argv[2], sys.argv[3]
        segments = transcrire_fichier_audio(chemin_audio)
        script = segments_vers_script(segments, titre=Path(chemin_audio).stem)
        exporter_script(script, chemin_sortie)
        print(f"{len(script['notes'])} note(s) détectée(s) -> {chemin_sortie}")

    elif commande == "ecouter":
        chemin_script, chemin_sortie = sys.argv[2], sys.argv[3]
        morceau = charger_morceau(chemin_script)
        synthetiser_script(morceau, chemin_sortie)
        print(f"Aperçu audio généré -> {chemin_sortie}")
        print("Lecture...")
        jouer_wav(chemin_sortie)

    else:
        print(__doc__)


if __name__ == "__main__":
    main()
