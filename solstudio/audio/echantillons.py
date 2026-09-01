"""Échantillons réels de violon pour la synthèse (Module 3, étape 3.4).

Remplace la synthèse par sinusoïdes ("son robotique") par de vrais
enregistrements de violon (domaine public, University of Iowa Electronic
Music Studios, https://theremin.music.uiowa.edu/MIS.html), transposés par
pitch-shifting vers la note MIDI exacte demandée.

Voir solstudio/data/echantillons_violon/_preparer.py pour la façon dont les
fichiers notes/*.wav ont été découpés à partir des enregistrements bruts.
"""

import functools
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf

DOSSIER_NOTES = Path(__file__).resolve().parents[1] / "data" / "echantillons_violon" / "notes"


@functools.lru_cache(maxsize=1)
def _midis_disponibles() -> list[int]:
    midis = sorted(int(p.stem) for p in DOSSIER_NOTES.glob("*.wav"))
    if not midis:
        raise RuntimeError(f"Aucun échantillon trouvé dans {DOSSIER_NOTES}")
    return midis


@functools.lru_cache(maxsize=None)
def _charger(midi: int) -> tuple[np.ndarray, int]:
    signal, sr = sf.read(DOSSIER_NOTES / f"{midi}.wav")
    if signal.ndim > 1:
        signal = signal.mean(axis=1)
    return signal.astype(np.float32), sr


def _ajuster_duree(signal: np.ndarray, sr: int, duree_s: float) -> np.ndarray:
    n_cible = max(1, int(duree_s * sr))

    if len(signal) >= n_cible:
        extrait = signal[:n_cible].copy()
    else:
        repetitions = int(np.ceil(n_cible / len(signal)))
        extrait = np.tile(signal, repetitions)[:n_cible]

    fondu = min(300, n_cible // 6)
    if fondu > 0:
        enveloppe = np.ones(n_cible)
        enveloppe[:fondu] = np.linspace(0.0, 1.0, fondu)
        enveloppe[-fondu:] = np.linspace(1.0, 0.0, fondu)
        extrait = extrait * enveloppe

    return extrait


def obtenir_echantillon(midi_cible: int, duree_s: float) -> tuple[np.ndarray, int]:
    """Retourne (signal, samplerate) pour la note MIDI demandée.

    Si la note exacte n'a pas été enregistrée, transpose par pitch-shifting
    l'échantillon disponible le plus proche. La durée est ensuite ajustée
    (tronquée ou répétée) pour correspondre à duree_s.
    """
    disponibles = _midis_disponibles()
    plus_proche = min(disponibles, key=lambda m: abs(m - midi_cible))
    signal, sr = _charger(plus_proche)

    decalage = midi_cible - plus_proche
    if decalage != 0:
        signal = librosa.effects.pitch_shift(signal, sr=sr, n_steps=decalage)

    return _ajuster_duree(signal, sr, duree_s), sr
