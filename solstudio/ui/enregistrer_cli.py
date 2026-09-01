"""Enregistre un extrait audio depuis le micro vers un fichier WAV.

Utile pour tester le Module 3 (transcription) sans dépendre d'un fichier
audio externe.

Usage:
    python -m solstudio.ui.enregistrer_cli sortie.wav [duree_secondes]
"""

import sys
import wave

import numpy as np
import sounddevice as sd

SAMPLERATE = 44100
DUREE_DEFAUT_S = 5.0


def enregistrer(chemin_sortie: str, duree_s: float = DUREE_DEFAUT_S, samplerate: int = SAMPLERATE):
    print(f"Enregistrement de {duree_s}s... jouez maintenant !")
    audio = sd.rec(int(duree_s * samplerate), samplerate=samplerate, channels=1, dtype="float32")
    sd.wait()
    print("Terminé.")

    signal_int16 = np.int16(np.clip(audio[:, 0], -1.0, 1.0) * 32767)
    with wave.open(chemin_sortie, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(samplerate)
        f.writeframes(signal_int16.tobytes())
    print(f"Fichier écrit -> {chemin_sortie}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    chemin_sortie = sys.argv[1]
    duree_s = float(sys.argv[2]) if len(sys.argv) > 2 else DUREE_DEFAUT_S
    enregistrer(chemin_sortie, duree_s)


if __name__ == "__main__":
    main()
