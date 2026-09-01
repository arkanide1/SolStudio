"""Suivi en direct de la progression dans un morceau (Module 2, étape 2.4).

Compare la note attendue du script à la note réellement détectée par le
Module 1 (accordeur) et avance dans le morceau quand elle est jouée juste.
"""


class SuiveurMorceau:
    def __init__(self, notes: list[dict]):
        self.notes = notes
        self.index = 0

    @property
    def termine(self) -> bool:
        return self.index >= len(self.notes)

    @property
    def note_courante(self) -> dict | None:
        if self.termine:
            return None
        return self.notes[self.index]

    def recevoir_detection(self, resultat_accordeur: dict) -> bool:
        """resultat_accordeur : sortie de accordeur.analyser_frequence().

        Retourne True si la note attendue vient d'être validée (l'index
        avance alors d'une note), False sinon.
        """
        if self.termine or not resultat_accordeur.get("detecte"):
            return False

        attendu = self.note_courante
        if (
            resultat_accordeur["note"] == attendu["note"]
            and resultat_accordeur["corde"] == attendu["corde"]
            and resultat_accordeur["direction"] == "juste"
        ):
            self.index += 1
            return True
        return False

    def reinitialiser(self):
        self.index = 0
