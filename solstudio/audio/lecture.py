"""Lecture d'un fichier WAV via le haut-parleur (utilitaire de test)."""

import wave

import numpy as np
import sounddevice as sd


def jouer_wav(chemin) -> None:
    with wave.open(str(chemin), "rb") as f:
        sr = f.getframerate()
        n = f.getnframes()
        frames = f.readframes(n)

    signal = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    sd.play(signal, sr)
    sd.wait()
