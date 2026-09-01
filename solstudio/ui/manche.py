"""Vue simplifiée du manche du violon pour une note donnée (Module 2, étape 2.3),
et grille de référence de la 1ère position (dashboard accordeur)."""

from solstudio.theorie.cordes import ORDRE_CORDES, midi_de_la_note
from solstudio.theorie.solfege import freq_vers_note, midi_vers_freq

ORDRE_AFFICHAGE = ["Mi", "La", "Ré", "Sol"]  # aigu en haut -> grave en bas

LARGEUR_PREMIERE_POSITION = 7  # une quinte juste (7 demi-tons) au-dessus de la corde à vide


def doigt_reference_manche(position: int) -> int:
    """Doigté pédagogique standard de la 1ère position (avec 1er/2e/3e doigt
    "bas" et "haut"), différent de la simplification utilisée par le Module 3
    (ia/doigte.py) qui sert uniquement à la transcription automatique."""
    if position == 0:
        return 0
    return min(4, (position + 1) // 2)


def grille_manche(largeur_demi_tons: int = LARGEUR_PREMIERE_POSITION) -> dict:
    """Retourne, pour chaque corde, la liste des notes en 1ère position :
    la corde à vide puis chaque demi-ton jusqu'à une quinte juste au-dessus.

    {"Sol": [{"position": 0, "doigt": 0, "note": "Sol", "octave": 3}, ...], ...}
    """
    grille = {}
    for corde in ORDRE_CORDES:
        lignes = []
        for position in range(0, largeur_demi_tons + 1):
            midi = midi_de_la_note(corde, position)
            info = freq_vers_note(midi_vers_freq(midi))
            lignes.append({
                "position": position,
                "doigt": doigt_reference_manche(position),
                "note": info["note"],
                "octave": info["octave"],
            })
        grille[corde] = lignes
    return grille


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
