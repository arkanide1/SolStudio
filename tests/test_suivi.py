from solstudio.dashboard.suivi import SuiveurMorceau

NOTES = [
    {"note": "Sol", "corde": "Sol", "position": 0, "doigt": 0, "duree_temps": 1},
    {"note": "La", "corde": "Sol", "position": 1, "doigt": 1, "duree_temps": 1},
]


def test_avance_si_note_juste():
    suiveur = SuiveurMorceau(NOTES)
    resultat = {"detecte": True, "note": "Sol", "corde": "Sol", "direction": "juste"}
    assert suiveur.recevoir_detection(resultat) is True
    assert suiveur.index == 1


def test_n_avance_pas_si_mauvaise_note():
    suiveur = SuiveurMorceau(NOTES)
    resultat = {"detecte": True, "note": "La", "corde": "Sol", "direction": "juste"}
    assert suiveur.recevoir_detection(resultat) is False
    assert suiveur.index == 0


def test_n_avance_pas_si_pas_juste():
    suiveur = SuiveurMorceau(NOTES)
    resultat = {"detecte": True, "note": "Sol", "corde": "Sol", "direction": "monter"}
    assert suiveur.recevoir_detection(resultat) is False
    assert suiveur.index == 0


def test_termine_apres_toutes_les_notes():
    suiveur = SuiveurMorceau(NOTES)
    suiveur.recevoir_detection({"detecte": True, "note": "Sol", "corde": "Sol", "direction": "juste"})
    suiveur.recevoir_detection({"detecte": True, "note": "La", "corde": "Sol", "direction": "juste"})
    assert suiveur.termine is True
    assert suiveur.note_courante is None


def test_non_detecte_ne_change_rien():
    suiveur = SuiveurMorceau(NOTES)
    assert suiveur.recevoir_detection({"detecte": False}) is False
    assert suiveur.index == 0


def test_reinitialiser():
    suiveur = SuiveurMorceau(NOTES)
    suiveur.recevoir_detection({"detecte": True, "note": "Sol", "corde": "Sol", "direction": "juste"})
    suiveur.reinitialiser()
    assert suiveur.index == 0
