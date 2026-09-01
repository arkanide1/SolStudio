"""Dashboard graphique (Module 2 + notation) : importer un script ou un
enregistrement audio, voir la partition rendue et écouter un aperçu.

Usage (depuis la racine du projet) :
    venv\\Scripts\\streamlit run solstudio/ui/dashboard_streamlit.py
"""

import json
import sys
import tempfile
from pathlib import Path

# streamlit exécute ce fichier directement (pas via `python -m`), donc la
# racine du projet n'est pas automatiquement sur sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st
import streamlit.components.v1 as components

from solstudio.dashboard.notation import script_vers_abc
from solstudio.dashboard.script import MorceauInvalide, valider_morceau
from solstudio.ia.conversion import segments_vers_script
from solstudio.ia.synthese import synthetiser_script
from solstudio.ia.transcription import transcrire_fichier_audio

st.set_page_config(page_title="SolStudio", page_icon="🎻")
st.title("🎻 SolStudio — Dashboard")


def _rendre_partition(abc_texte: str) -> None:
    html = f"""
    <div id="partition"></div>
    <script src="https://cdn.jsdelivr.net/npm/abcjs@6/dist/abcjs-basic-min.js"></script>
    <script>
      ABCJS.renderAbc("partition", {json.dumps(abc_texte)});
    </script>
    """
    components.html(html, height=260, scrolling=True)


def _afficher_script(script: dict) -> None:
    st.subheader(script.get("titre", "Sans titre"))
    _rendre_partition(script_vers_abc(script))

    st.table([
        {
            "Note": n["note"],
            "Corde": n["corde"],
            "Position": n["position"],
            "Doigt": n["doigt"],
            "Durée (temps)": n["duree_temps"],
        }
        for n in script["notes"]
    ])

    if st.button("Écouter un aperçu"):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            chemin_wav = synthetiser_script(script, f.name)
        st.audio(str(chemin_wav))


onglet_script, onglet_audio = st.tabs(["Importer un script", "Importer un audio"])

with onglet_script:
    fichier = st.file_uploader("Fichier script (.json)", type=["json"])
    if fichier:
        try:
            script = valider_morceau(json.loads(fichier.read().decode("utf-8")))
            _afficher_script(script)
        except (json.JSONDecodeError, MorceauInvalide) as e:
            st.error(f"Fichier invalide : {e}")

with onglet_audio:
    fichier_audio = st.file_uploader("Enregistrement (.wav)", type=["wav"])
    if fichier_audio:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(fichier_audio.read())
            chemin_audio = f.name

        with st.spinner("Transcription en cours..."):
            segments = transcrire_fichier_audio(chemin_audio)
            script = segments_vers_script(segments, titre=Path(fichier_audio.name).stem)

        if not script["notes"]:
            st.warning("Aucune note détectée.")
        else:
            _afficher_script(script)
