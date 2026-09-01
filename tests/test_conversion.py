from solstudio.ia.conversion import segments_vers_script


def test_segment_la_donne_note_juste_corde_la():
    script = segments_vers_script([{"freq": 440.0, "duree_s": 0.5}])
    assert len(script["notes"]) == 1
    note = script["notes"][0]
    assert note["note"] == "La"
    assert note["corde"] == "La"
    assert note["position"] == 0
    assert note["doigt"] == 0


def test_segment_hors_registre_est_ignore():
    script = segments_vers_script([{"freq": 440.0, "duree_s": 0.5}, {"freq": 30.0, "duree_s": 0.3}])
    assert len(script["notes"]) == 1


def test_titre_par_defaut():
    script = segments_vers_script([{"freq": 440.0, "duree_s": 0.5}])
    assert script["titre"] == "Transcription automatique"
