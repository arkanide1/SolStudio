import json

import pytest

from solstudio.dashboard.script import MorceauInvalide, charger_morceau


def test_charge_exemple_morceau():
    morceau = charger_morceau("solstudio/data/exemple_morceau.json")
    assert "notes" in morceau
    assert len(morceau["notes"]) == 8
    assert morceau["notes"][0]["note"] == "Sol"


def test_erreur_si_champ_manquant(tmp_path):
    fichier = tmp_path / "invalide.json"
    fichier.write_text(json.dumps({"notes": [{"note": "Do"}]}), encoding="utf-8")
    with pytest.raises(MorceauInvalide):
        charger_morceau(fichier)


def test_erreur_si_pas_de_notes(tmp_path):
    fichier = tmp_path / "vide.json"
    fichier.write_text(json.dumps({"titre": "Vide"}), encoding="utf-8")
    with pytest.raises(MorceauInvalide):
        charger_morceau(fichier)


def test_erreur_si_liste_notes_vide(tmp_path):
    fichier = tmp_path / "sans_notes.json"
    fichier.write_text(json.dumps({"notes": []}), encoding="utf-8")
    with pytest.raises(MorceauInvalide):
        charger_morceau(fichier)
