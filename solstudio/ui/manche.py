"""Vue simplifiée du manche du violon pour une note donnée (Module 2, étape 2.3)."""

ORDRE_AFFICHAGE = ["Mi", "La", "Ré", "Sol"]  # aigu en haut -> grave en bas


def vue_manche(note: dict) -> str:
    """Représentation ASCII des 4 cordes avec un repère sur la corde/position
    à jouer pour la note donnée (dict avec 'corde', 'position', 'doigt')."""
    lignes = []
    for corde in ORDRE_AFFICHAGE:
        est_la_corde = corde == note["corde"]
        marqueur = "●" if est_la_corde else "-"
        detail = f"pos {note['position']} doigt {note['doigt']}" if est_la_corde else ""
        lignes.append(f"{corde:<4}|{marqueur:^5}|  {detail}")
    return "\n".join(lignes)
