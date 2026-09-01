"""Dashboard en console (Module 2) : charge un morceau et suit sa lecture en direct.

Usage:
    python -m solstudio.ui.dashboard_cli [chemin_vers_morceau.json]

Sans argument, charge l'exemple fourni dans solstudio/data/exemple_morceau.json.
"""

import sys
import time
from pathlib import Path

from solstudio.audio.accordeur import analyser_frequence
from solstudio.audio.capture import FluxAudio
from solstudio.audio.pitch import detecter_pitch
from solstudio.dashboard.script import charger_morceau
from solstudio.dashboard.suivi import SuiveurMorceau
from solstudio.ui.manche import vue_manche

CHEMIN_MORCEAU_DEFAUT = Path(__file__).resolve().parents[1] / "data" / "exemple_morceau.json"


def main(chemin_morceau: str | None = None):
    chemin = Path(chemin_morceau) if chemin_morceau else CHEMIN_MORCEAU_DEFAUT
    morceau = charger_morceau(chemin)
    suiveur = SuiveurMorceau(morceau["notes"])

    print(f"SolStudio - Dashboard (Module 2) - {morceau.get('titre', '')}")
    print("Ctrl+C pour quitter\n")

    with FluxAudio() as flux:
        try:
            while not suiveur.termine:
                buffer = flux.dernier_buffer()
                freq = detecter_pitch(buffer, flux.samplerate)
                resultat = analyser_frequence(freq)
                attendu = suiveur.note_courante

                print("\n" * 6, end="")
                print(
                    f"Note {suiveur.index + 1}/{len(suiveur.notes)} attendue : "
                    f"{attendu['note']} (corde {attendu['corde']}, "
                    f"position {attendu['position']}, doigt {attendu['doigt']})"
                )
                print(vue_manche(attendu))

                if suiveur.recevoir_detection(resultat):
                    print(">> validée !")

                time.sleep(0.1)

            print("\nMorceau terminé !")
        except KeyboardInterrupt:
            print("\nArrêt.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
