from solstudio.ui.manche import doigt_reference_manche, grille_manche, vue_manche

NOTE = {"note": "Fa", "corde": "Ré", "position": 2, "doigt": 2, "duree_temps": 1}


def test_vue_manche_contient_les_4_cordes():
    vue = vue_manche(NOTE)
    for corde in ["Sol", "Ré", "La", "Mi"]:
        assert corde in vue


def test_vue_manche_indique_la_bonne_position():
    vue = vue_manche(NOTE)
    assert "pos 2 doigt 2" in vue


def test_doigt_reference_manche_bas_et_haut():
    assert doigt_reference_manche(0) == 0
    assert doigt_reference_manche(1) == 1
    assert doigt_reference_manche(2) == 1
    assert doigt_reference_manche(3) == 2
    assert doigt_reference_manche(4) == 2
    assert doigt_reference_manche(5) == 3
    assert doigt_reference_manche(6) == 3
    assert doigt_reference_manche(7) == 4


def test_grille_manche_a_les_4_cordes():
    grille = grille_manche()
    assert set(grille.keys()) == {"Sol", "Ré", "La", "Mi"}
    for corde, lignes in grille.items():
        assert len(lignes) == 8  # corde à vide + 7 demi-tons


def test_grille_manche_corde_a_vide_est_correcte():
    grille = grille_manche()
    assert grille["Sol"][0]["note"] == "Sol"
    assert grille["Sol"][0]["octave"] == 3
    assert grille["La"][0]["note"] == "La"
    assert grille["La"][0]["octave"] == 4


def test_grille_manche_quinte_juste_au_dessus():
    # 7 demi-tons au-dessus de Sol (corde) = Ré (quinte juste), soit la
    # meme note que la corde Ré à vide.
    grille = grille_manche()
    assert grille["Sol"][7]["note"] == "Ré"
    assert grille["Sol"][7]["octave"] == grille["Ré"][0]["octave"]
