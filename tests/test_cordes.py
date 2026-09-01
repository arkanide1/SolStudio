from solstudio.theorie.cordes import CORDES, ORDRE_CORDES, corde_la_plus_proche, ecart_par_rapport_a_vide


def test_les_4_cordes_sont_en_solfege():
    assert set(CORDES.keys()) == {"Sol", "Ré", "La", "Mi"}
    assert ORDRE_CORDES == ["Sol", "Ré", "La", "Mi"]


def test_frequences_cordes_a_vide():
    assert CORDES["Sol"]["freq"] == 196.00
    assert CORDES["Ré"]["freq"] == 293.66
    assert CORDES["La"]["freq"] == 440.00
    assert CORDES["Mi"]["freq"] == 659.25


def test_corde_la_plus_proche_sur_freq_a_vide():
    assert corde_la_plus_proche(196.0) == "Sol"
    assert corde_la_plus_proche(293.66) == "Ré"
    assert corde_la_plus_proche(440.0) == "La"
    assert corde_la_plus_proche(659.25) == "Mi"


def test_corde_la_plus_proche_en_position():
    # Une fréquence jouée en 3e position sur la corde de Sol reste sur "Sol"
    # tant qu'elle n'atteint pas la fréquence à vide de la corde de Ré.
    assert corde_la_plus_proche(250.0) == "Sol"


def test_ecart_par_rapport_a_vide_zero_sur_corde_a_vide():
    assert ecart_par_rapport_a_vide(196.0, "Sol") == 0.0
