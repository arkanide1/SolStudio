import wave

from solstudio.ia.synthese import synthetiser_script

SCRIPT = {
    "titre": "Test",
    "notes": [
        {"note": "Sol", "corde": "Sol", "position": 0, "doigt": 0, "duree_temps": 1},
        {"note": "La", "corde": "Sol", "position": 2, "doigt": 2, "duree_temps": 1},
    ],
}


def test_synthetise_un_fichier_wav_de_la_bonne_duree(tmp_path):
    chemin = tmp_path / "apercu.wav"
    resultat = synthetiser_script(SCRIPT, chemin, tempo_bpm=60)

    assert resultat.exists()
    with wave.open(str(resultat), "rb") as f:
        duree = f.getnframes() / f.getframerate()
    # 2 notes d'un temps chacune à 60 bpm = ~2 secondes
    assert 1.8 < duree < 2.2
