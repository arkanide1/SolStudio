from solstudio.audio.accordeur import analyser_frequence


def test_note_juste_sur_la_corde_la():
    resultat = analyser_frequence(440.0)
    assert resultat["detecte"] is True
    assert resultat["note"] == "La"
    assert resultat["corde"] == "La"
    assert resultat["direction"] == "juste"


def test_direction_descendre_si_trop_haut():
    resultat = analyser_frequence(445.0)
    assert resultat["cents"] > 0
    assert resultat["direction"] == "descendre"


def test_direction_monter_si_trop_bas():
    resultat = analyser_frequence(435.0)
    assert resultat["cents"] < 0
    assert resultat["direction"] == "monter"


def test_aucune_frequence_retourne_non_detecte():
    resultat = analyser_frequence(None)
    assert resultat == {"detecte": False}


def test_corde_sol_reconnue():
    resultat = analyser_frequence(196.0)
    assert resultat["corde"] == "Sol"
    assert resultat["note"] == "Sol"
