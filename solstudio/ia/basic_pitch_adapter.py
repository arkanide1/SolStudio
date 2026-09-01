"""Intégration optionnelle vers Basic Pitch (Spotify, open-source).

Non utilisée par défaut (dépendance lourde : tensorflow/onnxruntime).
Installer avec `pip install basic-pitch` pour l'activer ; sinon le reste
du Module 3 fonctionne avec la transcription "maison" de transcription.py.
"""


def disponible() -> bool:
    try:
        import basic_pitch  # noqa: F401
        return True
    except ImportError:
        return False


def transcrire_avec_basic_pitch(chemin) -> list[dict]:
    """Transcrit un fichier audio via Basic Pitch et retourne des segments
    {"freq", "debut_s", "duree_s"} compatibles avec conversion.py.
    """
    if not disponible():
        raise RuntimeError(
            "basic-pitch n'est pas installé. Lancer `pip install basic-pitch` pour l'activer."
        )

    from basic_pitch import ICASSP_2022_MODEL_PATH
    from basic_pitch.inference import predict

    from solstudio.theorie.solfege import midi_vers_freq

    _, _, note_events = predict(str(chemin), ICASSP_2022_MODEL_PATH)

    segments = []
    for debut, fin, midi, *_ in note_events:
        segments.append({
            "freq": midi_vers_freq(midi),
            "debut_s": round(float(debut), 2),
            "duree_s": round(float(fin - debut), 2),
        })
    return segments
