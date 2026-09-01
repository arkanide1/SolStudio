"""Référentiel solfège partagé (Module 0).

Toute conversion fréquence <-> note doit passer par ce module afin que
l'ensemble de l'application (accordeur, dashboard, IA) affiche uniquement
des noms de notes en solfège latin (Do Ré Mi Fa Sol La Si).

La notation anglo-saxonne (A-G) n'existe que comme table de construction
interne, jamais exposée aux autres modules.
"""

import math

A4_FREQ = 440.0
A4_MIDI = 69

# Ordre chromatique interne, jamais exposé en dehors de ce module.
_NOMS_SOLFEGE = ["Do", "Do#", "Ré", "Ré#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"]


def midi_vers_freq(midi: float, a4: float = A4_FREQ) -> float:
    """Convertit un numéro MIDI en fréquence (Hz), tempérament égal."""
    return a4 * (2.0 ** ((midi - A4_MIDI) / 12.0))


def freq_vers_midi(freq: float, a4: float = A4_FREQ) -> float:
    """Convertit une fréquence (Hz) en numéro MIDI fractionnaire."""
    if freq <= 0:
        raise ValueError("La fréquence doit être positive")
    return A4_MIDI + 12.0 * math.log2(freq / a4)


def note_et_octave_vers_freq(nom: str, octave: int, a4: float = A4_FREQ) -> float:
    """Convertit un nom de note en solfège + octave en fréquence (Hz).

    L'octave suit la convention scientifique : Do4 (La4 = 440 Hz est dans
    l'octave 4).
    """
    if nom not in _NOMS_SOLFEGE:
        raise ValueError(f"Note inconnue en solfège : {nom!r}")
    index = _NOMS_SOLFEGE.index(nom)
    midi = (octave + 1) * 12 + index
    return midi_vers_freq(midi, a4)


def freq_vers_note(freq: float, a4: float = A4_FREQ) -> dict:
    """Convertit une fréquence (Hz) en note solfège la plus proche.

    Retourne un dict : {"note": "La", "octave": 4, "cents": 0.0, "midi": 69}
    - "cents" est l'écart entre la fréquence donnée et la note juste la plus
      proche (positif = trop haut, négatif = trop bas).
    """
    midi_frac = freq_vers_midi(freq, a4)
    midi_entier = round(midi_frac)
    cents = (midi_frac - midi_entier) * 100.0

    index = midi_entier % 12
    octave = midi_entier // 12 - 1

    return {
        "note": _NOMS_SOLFEGE[index],
        "octave": octave,
        "cents": round(cents, 1),
        "midi": midi_entier,
    }
