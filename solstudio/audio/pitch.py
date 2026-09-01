"""Détection de la fréquence fondamentale (Module 1).

Implémentation de l'algorithme YIN (De Cheveigné & Kawahara, 2002),
volontairement en numpy pur pour éviter toute dépendance compliquée à
installer (aubio nécessite un compilateur sur Windows).

Le violon utile va environ de Sol3 (196 Hz) à des positions aiguës sur la
corde de Mi (jusqu'à ~1500 Hz pour les premières positions), d'où les bornes
fmin/fmax par défaut.
"""

import numpy as np

FMIN_DEFAUT = 150.0
FMAX_DEFAUT = 1500.0
SEUIL_YIN_DEFAUT = 0.15
SEUIL_SILENCE_RMS = 0.01


def _rms(buffer: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(buffer))))


def _fonction_difference(x: np.ndarray, tau_max: int) -> np.ndarray:
    n = len(x)
    d = np.zeros(tau_max)
    for tau in range(1, tau_max):
        diff = x[: n - tau] - x[tau:n]
        d[tau] = np.dot(diff, diff)
    return d


def _difference_moyenne_cumulative_normalisee(d: np.ndarray) -> np.ndarray:
    cmnd = np.ones_like(d)
    somme_cumulee = 0.0
    for tau in range(1, len(d)):
        somme_cumulee += d[tau]
        cmnd[tau] = d[tau] * tau / somme_cumulee if somme_cumulee > 0 else 1.0
    return cmnd


def detecter_pitch(
    buffer: np.ndarray,
    samplerate: int,
    fmin: float = FMIN_DEFAUT,
    fmax: float = FMAX_DEFAUT,
    seuil: float = SEUIL_YIN_DEFAUT,
) -> float | None:
    """Détecte la fréquence fondamentale d'un buffer audio mono.

    Retourne la fréquence en Hz, ou None si aucun son suffisamment fort
    et périodique n'est détecté (silence, bruit).
    """
    buffer = np.asarray(buffer, dtype=np.float64)

    if _rms(buffer) < SEUIL_SILENCE_RMS:
        return None

    tau_min = max(1, int(samplerate / fmax))
    tau_max = min(int(samplerate / fmin), len(buffer) - 1)
    if tau_max <= tau_min:
        return None

    d = _fonction_difference(buffer, tau_max)
    cmnd = _difference_moyenne_cumulative_normalisee(d)

    tau_estime = None
    for tau in range(tau_min, tau_max):
        if cmnd[tau] < seuil:
            while tau + 1 < tau_max and cmnd[tau + 1] < cmnd[tau]:
                tau += 1
            tau_estime = tau
            break

    if tau_estime is None:
        return None

    if 0 < tau_estime < len(cmnd) - 1:
        x0, x1, x2 = cmnd[tau_estime - 1], cmnd[tau_estime], cmnd[tau_estime + 1]
        denom = x0 - 2 * x1 + x2
        decalage = 0.5 * (x0 - x2) / denom if denom != 0 else 0.0
    else:
        decalage = 0.0

    tau_final = tau_estime + decalage
    if tau_final <= 0:
        return None

    return samplerate / tau_final
