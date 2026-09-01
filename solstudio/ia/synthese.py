"""Synthèse audio à partir d'un script (Module 3, étape 3.4).

Utilise de vrais échantillons de violon (voir solstudio/audio/echantillons.py)
transposés par pitch-shifting, plutôt que des sinusoïdes ("son robotique").
"""

import wave
from pathlib import Path

import librosa
import numpy as np

from solstudio.audio.echantillons import obtenir_echantillon
from solstudio.theorie.cordes import midi_de_la_note

TEMPO_BPM_DEFAUT = 80


def synthetiser_script(
    script: dict,
    chemin_sortie,
    samplerate: int = 44100,
    tempo_bpm: float = TEMPO_BPM_DEFAUT,
) -> Path:
    """Génère un fichier WAV d'aperçu à partir d'un script SolStudio."""
    duree_par_temps_s = 60.0 / tempo_bpm

    ondes = []
    for note in script["notes"]:
        midi = midi_de_la_note(note["corde"], note["position"])
        duree = max(0.05, note["duree_temps"] * duree_par_temps_s)
        signal, sr = obtenir_echantillon(midi, duree)
        if sr != samplerate:
            signal = librosa.resample(signal, orig_sr=sr, target_sr=samplerate)
        ondes.append(signal)

    signal_total = np.concatenate(ondes) if ondes else np.zeros(0, dtype=np.float64)
    signal_int16 = np.int16(np.clip(signal_total, -1.0, 1.0) * 32767)

    chemin_sortie = Path(chemin_sortie)
    with wave.open(str(chemin_sortie), "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(samplerate)
        f.writeframes(signal_int16.tobytes())

    return chemin_sortie
