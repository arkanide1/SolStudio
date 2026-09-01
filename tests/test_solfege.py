from solstudio.theorie.solfege import (
    midi_vers_freq,
    freq_vers_midi,
    note_et_octave_vers_freq,
    freq_vers_note,
)


def test_la4_est_440hz():
    assert midi_vers_freq(69) == 440.0


def test_freq_vers_note_la4_exact():
    resultat = freq_vers_note(440.0)
    assert resultat["note"] == "La"
    assert resultat["octave"] == 4
    assert resultat["cents"] == 0.0
    assert resultat["midi"] == 69


def test_note_et_octave_vers_freq_do4():
    freq = note_et_octave_vers_freq("Do", 4)
    assert round(freq, 2) == 261.63


def test_freq_vers_note_detecte_ecart_en_cents():
    # Un peu au-dessus de La4 (440 Hz) : doit rester "La" avec des cents positifs.
    resultat = freq_vers_note(443.0)
    assert resultat["note"] == "La"
    assert resultat["cents"] > 0


def test_aucune_notation_anglo_saxonne_dans_la_sortie():
    for freq in [196.0, 293.66, 440.0, 659.25]:
        resultat = freq_vers_note(freq)
        assert resultat["note"] in [
            "Do", "Do#", "Ré", "Ré#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"
        ]


def test_aller_retour_freq_midi():
    for midi in [60, 69, 72, 76]:
        freq = midi_vers_freq(midi)
        assert round(freq_vers_midi(freq)) == midi
