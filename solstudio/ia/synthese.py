"""Synthèse audio à partir d'un script (Module 3, étape 3.4).

Génère un aperçu audio (ondes sinusoïdales) pour écouter un morceau avant
de le jouer soi-même. Volontairement simple (pas de dépendance externe type
FluidSynth/SoundFont) : le format de script ne change pas, donc une synthèse
plus réaliste pourra remplacer cette implémentation plus tard sans impact
sur les Modules 0-2.
"""

import wave
from pathlib import Path

import numpy as np

from solstudio.theorie.cordes import CORDES
from solstudio.theorie.solfege import freq_vers_midi, midi_vers_freq

AMPLITUDE = 0.3
TEMPO_BPM_DEFAUT = 80


def _midi_de_la_note(corde: str, position: int) -> float:
    midi_a_vide = round(freq_vers_midi(CORDES[corde]["freq"]))
    return midi_a_vide + position


def _tonaliser(freq: float, duree_s: float, samplerate: int) -> np.ndarray:
    n = max(1, int(samplerate * duree_s))
    t = np.linspace(0, duree_s, n, endpoint=False)
    onde = AMPLITUDE * np.sin(2 * np.pi * freq * t)

    fondu = min(200, n // 4)
    if fondu > 0:
        enveloppe = np.ones(n)
        enveloppe[:fondu] = np.linspace(0.0, 1.0, fondu)
        enveloppe[-fondu:] = np.linspace(1.0, 0.0, fondu)
        onde = onde * enveloppe
    return onde


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
        midi = _midi_de_la_note(note["corde"], note["position"])
        freq = midi_vers_freq(midi)
        duree = max(0.05, note["duree_temps"] * duree_par_temps_s)
        ondes.append(_tonaliser(freq, duree, samplerate))

    signal = np.concatenate(ondes) if ondes else np.zeros(0, dtype=np.float64)
    signal_int16 = np.int16(np.clip(signal, -1.0, 1.0) * 32767)

    chemin_sortie = Path(chemin_sortie)
    with wave.open(str(chemin_sortie), "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(samplerate)
        f.writeframes(signal_int16.tobytes())

    return chemin_sortie
