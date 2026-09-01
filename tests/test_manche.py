from solstudio.ui.manche import vue_manche

NOTE = {"note": "Fa", "corde": "Ré", "position": 2, "doigt": 2, "duree_temps": 1}


def test_vue_manche_contient_les_4_cordes():
    vue = vue_manche(NOTE)
    for corde in ["Sol", "Ré", "La", "Mi"]:
        assert corde in vue


def test_vue_manche_indique_la_bonne_position():
    vue = vue_manche(NOTE)
    assert "pos 2 doigt 2" in vue
