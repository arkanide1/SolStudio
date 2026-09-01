"""Script ponctuel : découpe les enregistrements bruts (gammes chromatiques
continues, University of Iowa MIS) en un échantillon WAV par note.

Ce script n'est pas utilisé à l'exécution de l'app ; il sert seulement à
préparer une fois la bibliothèque d'échantillons dans notes/. Sources dans
ce dossier (licence : domaine public, University of Iowa Electronic Music
Studios, https://theremin.music.uiowa.edu/MIS.html).
"""

from pathlib import Path

import numpy as np
import soundfile as sf

DOSSIER = Path(__file__).resolve().parent
DOSSIER_NOTES = DOSSIER / "notes"
DOSSIER_NOTES.mkdir(exist_ok=True)

SAMPLERATE_CIBLE = 44100
SEUIL_RMS = 0.02
DUREE_MIN_S = 0.3
TAILLE_BLOC = 2048
SAUT = 1024
FUSION_ECART_MAX_S = 1.5  # fusionne les segments proches (creux dus au vibrato)

# (fichier, midi_note_de_depart) - la 1ere note detectee = midi_depart,
# chaque note suivante = +1 demi-ton (gamme chromatique montante).
FICHIERS = [
    ("Violin.arco.ff.sulG.G3B3.aiff", 55),  # Sol3
    ("Violin.arco.ff.sulD.D4B4.aiff", 62),  # Ré4
    ("Violin.arco.ff.sulA.A4B4.aiff", 69),  # La4
    ("Violin.arco.ff.sulE.E5B5.aiff", 76),  # Mi5
]


def _rms(bloc: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(bloc))))


def segmenter(signal: np.ndarray, sr: int):
    segments = []
    debut = None
    for i in range(0, len(signal) - TAILLE_BLOC, SAUT):
        bloc = signal[i:i + TAILLE_BLOC]
        t = i / sr
        if _rms(bloc) >= SEUIL_RMS:
            if debut is None:
                debut = t
        else:
            if debut is not None and (t - debut) >= DUREE_MIN_S:
                segments.append((debut, t))
            debut = None
    if debut is not None:
        fin = len(signal) / sr
        if fin - debut >= DUREE_MIN_S:
            segments.append((debut, fin))

    return _fusionner(segments)


def _fusionner(segments):
    """Fusionne les segments séparés par un creux court (vibrato) plutôt
    qu'un vrai silence entre deux notes."""
    if not segments:
        return segments
    fusionnes = [segments[0]]
    for debut, fin in segments[1:]:
        debut_precedent, fin_precedente = fusionnes[-1]
        if debut - fin_precedente <= FUSION_ECART_MAX_S:
            fusionnes[-1] = (debut_precedent, fin)
        else:
            fusionnes.append((debut, fin))
    return fusionnes


def main():
    for nom_fichier, midi_depart in FICHIERS:
        chemin = DOSSIER / nom_fichier
        signal, sr = sf.read(chemin)
        if signal.ndim > 1:
            signal = signal.mean(axis=1)

        segments = segmenter(signal, sr)
        print(f"{nom_fichier}: {len(segments)} segment(s) détecté(s)")

        for i, (debut, fin) in enumerate(segments):
            midi = midi_depart + i
            # on garde le coeur de la note (on saute l'attaque de l'archet
            # et on s'arrête avant la fin/relâchement), max 1.2s
            attaque = 0.15
            marge_fin = 0.15
            duree_utile = min(1.2, (fin - debut) - attaque - marge_fin)
            if duree_utile <= 0:
                continue
            i_debut = int((debut + attaque) * sr)
            i_fin = int((debut + attaque + duree_utile) * sr)
            extrait = signal[i_debut:i_fin].astype(np.float32)

            chemin_sortie = DOSSIER_NOTES / f"{midi}.wav"
            sf.write(chemin_sortie, extrait, sr, subtype="PCM_16")

        print(f"  -> notes MIDI {midi_depart} à {midi_depart + len(segments) - 1}")


if __name__ == "__main__":
    main()
