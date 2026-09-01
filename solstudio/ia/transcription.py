"""Transcription audio -> segments de notes (Module 3, étape 3.1).

Implémentation "maison" sans dépendance lourde : découpe un fichier WAV
mono en segments d'énergie continue (silence = séparateur) et détecte la
fréquence dominante de chaque segment avec l'algorithme YIN déjà utilisé
par l'accordeur (Module 1). Fonctionne pour de l'audio monophonique
(un violon seul), ce qui correspond à l'usage principal du projet.

Une intégration optionnelle vers Basic Pitch (Spotify, plus robuste,
polyphonique) est disponible dans basic_pitch_adapter.py si le paquet
`basic-pitch` est installé.
"""

import wave

import numpy as np

from solstudio.audio.pitch import detecter_pitch

TAILLE_BLOC_DEFAUT = 2048
SAUT_DEFAUT = 1024
SEUIL_RMS_DEFAUT = 0.02
DUREE_MIN_SEGMENT_S = 0.05


def _lire_wav_mono(chemin) -> tuple[np.ndarray, int]:
    with wave.open(str(chemin), "rb") as f:
        sr = f.getframerate()
        n = f.getnframes()
        sampwidth = f.getsampwidth()
        nchannels = f.getnchannels()
        frames = f.readframes(n)

    if sampwidth != 2:
        raise ValueError("Seuls les fichiers WAV 16 bits sont supportés pour l'instant")

    data = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    if nchannels > 1:
        data = data.reshape(-1, nchannels).mean(axis=1)
    return data, sr


def _finaliser_segment(blocs: list[np.ndarray], sr: int, debut: float, fin: float):
    freqs = []
    for bloc in blocs:
        freq = detecter_pitch(bloc, sr)
        if freq is not None:
            freqs.append(freq)
    if not freqs or (fin - debut) < DUREE_MIN_SEGMENT_S:
        return None
    return {
        "freq": float(np.median(freqs)),
        "debut_s": round(debut, 2),
        "duree_s": round(fin - debut, 2),
    }


def transcrire_fichier_audio(
    chemin,
    taille_bloc: int = TAILLE_BLOC_DEFAUT,
    saut: int = SAUT_DEFAUT,
    seuil_rms: float = SEUIL_RMS_DEFAUT,
) -> list[dict]:
    """Découpe un fichier audio WAV mono en segments de notes.

    Retourne une liste de {"freq": Hz, "debut_s": ..., "duree_s": ...}.
    """
    signal, sr = _lire_wav_mono(chemin)

    segments = []
    segment_courant: list[np.ndarray] = []
    debut_segment = None

    for i in range(0, max(0, len(signal) - taille_bloc), saut):
        bloc = signal[i:i + taille_bloc]
        rms = float(np.sqrt(np.mean(np.square(bloc))))
        t = i / sr

        if rms >= seuil_rms:
            if debut_segment is None:
                debut_segment = t
            segment_courant.append(bloc)
        elif segment_courant:
            segment = _finaliser_segment(segment_courant, sr, debut_segment, t)
            if segment:
                segments.append(segment)
            segment_courant = []
            debut_segment = None

    if segment_courant:
        segment = _finaliser_segment(segment_courant, sr, debut_segment, len(signal) / sr)
        if segment:
            segments.append(segment)

    return segments
