from solstudio.audio.echantillons import obtenir_echantillon


def test_note_exacte_a_la_bonne_duree():
    signal, sr = obtenir_echantillon(69, 0.5)  # La4, échantillonné directement
    assert abs(len(signal) / sr - 0.5) < 0.01


def test_note_absente_est_transposee_depuis_la_plus_proche():
    # MIDI 73 n'est pas enregistré (trou entre les cordes La et Mi) :
    # doit quand meme renvoyer un signal audio exploitable.
    signal, sr = obtenir_echantillon(73, 0.3)
    assert len(signal) > 0
    assert abs(len(signal) / sr - 0.3) < 0.01


def test_duree_courte_que_lechantillon_source_est_tronquee():
    signal, sr = obtenir_echantillon(60, 0.2)
    assert abs(len(signal) / sr - 0.2) < 0.01


def test_duree_plus_longue_que_lechantillon_source_est_completee():
    signal, sr = obtenir_echantillon(60, 5.0)
    assert abs(len(signal) / sr - 5.0) < 0.01
