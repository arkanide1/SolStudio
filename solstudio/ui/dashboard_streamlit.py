"""Dashboard graphique SolStudio : accordeur en direct + manche de référence
(M0/M1), et import de script/audio avec partition rendue (M2/M3).

Usage (depuis la racine du projet) :
    venv/Scripts/streamlit run solstudio/ui/dashboard_streamlit.py
"""

import io
import json
import sys
import tempfile
from pathlib import Path

# streamlit exécute ce fichier directement (pas via `python -m`), donc la
# racine du projet n'est pas automatiquement sur sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import soundfile as sf
import streamlit as st
import streamlit.components.v1 as components

from solstudio.audio.accordeur import analyser_frequence
from solstudio.audio.capture import FluxAudio
from solstudio.audio.echantillons import obtenir_echantillon
from solstudio.audio.pitch import detecter_pitch
from solstudio.dashboard.notation import script_vers_abc
from solstudio.dashboard.script import MorceauInvalide, valider_morceau
from solstudio.ia.conversion import segments_vers_script
from solstudio.ia.synthese import synthetiser_script
from solstudio.ia.transcription import transcrire_fichier_audio
from solstudio.theorie.cordes import CORDES, ORDRE_CORDES, midi_de_la_note
from solstudio.ui.manche import grille_manche

st.set_page_config(page_title="SolStudio", page_icon="🎻", layout="centered")
st.title("🎻 SolStudio — Dashboard")


# --------------------------------------------------------------------------
# Onglet Accordeur (M0 : référentiel + M1 : accordeur en direct + manche)
# --------------------------------------------------------------------------

def _bytes_wav(signal, sr) -> bytes:
    tampon = io.BytesIO()
    sf.write(tampon, signal, sr, format="WAV")
    return tampon.getvalue()


def _afficher_manche():
    st.subheader("Manche — 1ère position (solfège)")
    st.caption("Chaque corde couvre une quinte juste en 1ère position. Cliquez sur une note pour l'entendre.")

    grille = grille_manche()
    colonnes = st.columns(len(ORDRE_CORDES))

    for colonne, corde in zip(colonnes, ORDRE_CORDES):
        with colonne:
            st.markdown(f"<div style='text-align:center'><b>{corde}</b></div>", unsafe_allow_html=True)
            for ligne in grille[corde]:
                etiquette = ligne["note"] if ligne["position"] == 0 else f"{ligne['note']} ({ligne['doigt']})"
                if st.button(etiquette, key=f"note_{corde}_{ligne['position']}", use_container_width=True):
                    midi = midi_de_la_note(corde, ligne["position"])
                    signal, sr = obtenir_echantillon(midi, 1.0)
                    st.audio(_bytes_wav(signal, sr), format="audio/wav", autoplay=True)


def _afficher_referentiel():
    with st.expander("📖 Référentiel des cordes (Module 0)"):
        st.table([
            {"Corde": corde, "Fréquence à vide (Hz)": CORDES[corde]["freq"]}
            for corde in ORDRE_CORDES
        ])


@st.fragment(run_every="0.3s")
def _afficher_tuner_en_direct():
    flux = st.session_state.get("flux_audio")
    if flux is None:
        st.info("Cliquez sur « Démarrer le micro » pour lancer l'accordeur.")
        return

    buffer = flux.dernier_buffer()
    freq = detecter_pitch(buffer, flux.samplerate)
    resultat = analyser_frequence(freq)

    if not resultat.get("detecte"):
        st.write("... (silence ou son non reconnu)")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Note", f"{resultat['note']}{resultat['octave']}")
    c2.metric("Corde", resultat["corde"])
    c3.metric("Écart", f"{resultat['cents']:+.1f} cents")

    position_pct = int((max(-50.0, min(50.0, resultat["cents"])) + 50.0) / 100.0 * 100)
    st.progress(position_pct)

    messages = {
        "juste": "✅ Juste",
        "monter": "⬆️ Trop bas — avancer le doigt (vers le chevalet)",
        "descendre": "⬇️ Trop haut — reculer le doigt (vers le sillet)",
    }
    st.write(messages.get(resultat["direction"], ""))


def _afficher_accordeur():
    _afficher_manche()
    _afficher_referentiel()

    st.divider()
    st.subheader("🎯 Accordeur en direct (Module 1)")

    if "flux_audio" not in st.session_state:
        st.session_state["flux_audio"] = None

    col_demarrer, col_arreter = st.columns(2)
    with col_demarrer:
        if st.button("▶ Démarrer le micro", disabled=st.session_state["flux_audio"] is not None):
            flux = FluxAudio()
            flux.demarrer()
            st.session_state["flux_audio"] = flux
            st.rerun()
    with col_arreter:
        if st.button("■ Arrêter le micro", disabled=st.session_state["flux_audio"] is None):
            st.session_state["flux_audio"].arreter()
            st.session_state["flux_audio"] = None
            st.rerun()

    _afficher_tuner_en_direct()


# --------------------------------------------------------------------------
# Onglets Script / Audio (M2 : dashboard partition, M3 : transcription IA)
# --------------------------------------------------------------------------

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


onglet_accordeur, onglet_script, onglet_audio = st.tabs(["🎯 Accordeur", "📄 Importer un script", "🎙️ Importer un audio"])

with onglet_accordeur:
    _afficher_accordeur()

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
