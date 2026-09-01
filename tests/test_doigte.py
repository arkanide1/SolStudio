from solstudio.ia.doigte import choisir_corde_et_position, position_vers_doigt


def test_corde_a_vide_la():
    assert choisir_corde_et_position(69) == ("La", 0)  # La4


def test_corde_a_vide_re():
    assert choisir_corde_et_position(62) == ("Ré", 0)  # Ré4


def test_choix_position_minimale():
    # Mi4 (midi 64) : valide sur Sol (pos 9) et Ré (pos 2) -> on garde Ré, pos 2.
    assert choisir_corde_et_position(64) == ("Ré", 2)


def test_note_hors_registre_retourne_none():
    assert choisir_corde_et_position(30) is None


def test_position_vers_doigt_plafonne_a_4():
    assert position_vers_doigt(0) == 0
    assert position_vers_doigt(1) == 1
    assert position_vers_doigt(4) == 4
    assert position_vers_doigt(9) == 4
