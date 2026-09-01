from solstudio.dashboard.notation import script_vers_abc


def _script(note, corde, position, doigt=0, duree_temps=1, titre="Test"):
    return {
        "titre": titre,
        "notes": [{"note": note, "corde": corde, "position": position, "doigt": doigt, "duree_temps": duree_temps}],
    }


def test_entete_contient_titre_et_metadonnees_abc():
    abc = script_vers_abc(_script("La", "La", 0, titre="Ma Gamme"))
    assert "X:1" in abc
    assert "T:Ma Gamme" in abc
    assert "M:4/4" in abc
    assert "K:C" in abc


def test_la_corde_a_vide_est_A_sans_marque():
    abc = script_vers_abc(_script("La", "La", 0))
    ligne_notes = abc.splitlines()[-2]
    assert ligne_notes.startswith("A ") or ligne_notes.startswith("A|")


def test_sol_corde_a_vide_a_une_virgule():
    abc = script_vers_abc(_script("Sol", "Sol", 0))
    ligne_notes = abc.splitlines()[-2]
    assert "G," in ligne_notes


def test_mi_corde_a_vide_est_en_minuscule():
    abc = script_vers_abc(_script("Mi", "Mi", 0))
    ligne_notes = abc.splitlines()[-2]
    assert ligne_notes.startswith("e")


def test_paroles_contiennent_le_nom_solfege():
    abc = script_vers_abc(_script("Fa", "Ré", 2, doigt=2))
    ligne_paroles = abc.splitlines()[-1]
    assert ligne_paroles == "w: Fa"


def test_duree_deux_temps_donne_suffixe_2():
    abc = script_vers_abc(_script("La", "La", 0, duree_temps=2))
    ligne_notes = abc.splitlines()[-2]
    assert "A2" in ligne_notes


def test_duree_demi_temps_donne_fraction():
    abc = script_vers_abc(_script("La", "La", 0, duree_temps=0.5))
    ligne_notes = abc.splitlines()[-2]
    assert "A/2" in ligne_notes
