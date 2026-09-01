"""Détection de la fréquence fondamentale (Module 1).

Utilise librosa.pyin (variante probabiliste de YIN, avec correction des
erreurs d'octave via un modèle de Markov caché). Remplace une première
implémentation YIN "maison" qui se trompait souvent d'octave sur de
l'audio réel de violon (riche en harmoniques), alors qu'elle fonctionnait
bien sur des sinusoïdes pures de test.

Le violon utile va environ de Sol3 (196 Hz) à des positions aiguës sur la
corde de Mi (jusqu'à ~1500 Hz pour les premières positions), d'où les bornes
fmin/fmax par défaut.
"""

import librosa
import numpy as np

FMIN_DEFAUT = 150.0
FMAX_DEFAUT = 1500.0
SEUIL_SILENCE_RMS = 0.01
TAILLE_TRAME_MAX = 2048


def _rms(buffer: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(buffer))))


def detecter_pitch(
    buffer: np.ndarray,
    samplerate: int,
    fmin: float = FMIN_DEFAUT,
    fmax: float = FMAX_DEFAUT,
) -> float | None:
    """Détecte la fréquence fondamentale d'un buffer audio mono.

    Retourne la fréquence en Hz, ou None si aucun son suffisamment fort
    et voisé n'est détecté (silence, bruit).
    """
    buffer = np.asarray(buffer, dtype=np.float64)

    if _rms(buffer) < SEUIL_SILENCE_RMS:
        return None

    taille_trame = min(len(buffer), TAILLE_TRAME_MAX)
    if taille_trame < 64:
        return None
    saut = max(1, taille_trame // 4)

    f0, voise, _probabilite = librosa.pyin(
        buffer,
        fmin=fmin,
        fmax=fmax,
        sr=samplerate,
        frame_length=taille_trame,
        hop_length=saut,
        center=True,
    )

    f0_voise = f0[voise]
    f0_voise = f0_voise[np.isfinite(f0_voise)]
    if f0_voise.size == 0:
        return None

    return float(np.median(f0_voise))
