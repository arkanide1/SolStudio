"""Accordeur en console (première version du Module 1, étapes 1.1-1.4).

Lance la capture micro et affiche en direct : note en solfège, écart en
cents, corde détectée et direction à suivre (monter / descendre / juste).

Usage:
    python -m solstudio.ui.accordeur_cli
"""

import sys
import time

from solstudio.audio.accordeur import analyser_frequence
from solstudio.audio.capture import FluxAudio
from solstudio.audio.pitch import detecter_pitch

SAMPLERATE = 44100
TAILLE_BLOC = 2048
LARGEUR_BARRE = 20


def barre_cents(cents: float, largeur: int = LARGEUR_BARRE) -> str:
    cents_clip = max(-50.0, min(50.0, cents))
    position = int((cents_clip + 50.0) / 100.0 * largeur)
    position = max(0, min(largeur, position))
    barre = ["-"] * (largeur + 1)
    barre[largeur // 2] = "|"
    barre[position] = "●"  # ●
    return "".join(barre)


def formater_ligne(resultat: dict) -> str:
    if not resultat.get("detecte"):
        return "... (silence ou son non reconnu)"
    return (
        f"{resultat['note']}{resultat['octave']:<3} "
        f"corde:{resultat['corde']:<4} "
        f"{resultat['cents']:+6.1f} cents  "
        f"[{barre_cents(resultat['cents'])}]  -> {resultat['direction']}"
    )


def main():
    print("SolStudio - Accordeur (Module 1) - Ctrl+C pour quitter")
    with FluxAudio(samplerate=SAMPLERATE, taille_bloc=TAILLE_BLOC) as flux:
        try:
            while True:
                buffer = flux.dernier_buffer()
                freq = detecter_pitch(buffer, SAMPLERATE)
                resultat = analyser_frequence(freq)
                ligne = formater_ligne(resultat)
                print("\r" + ligne.ljust(70), end="")
                sys.stdout.flush()
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nArrêt.")


if __name__ == "__main__":
    main()
