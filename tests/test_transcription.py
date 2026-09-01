import wave

import numpy as np

from solstudio.ia.transcription import transcrire_fichier_audio

SAMPLERATE = 44100


def _ecrire_wav(chemin, segments_freq_duree, sr=SAMPLERATE):
    morceaux = []
    for freq, duree in segments_freq_duree:
        n = int(sr * duree)
        if freq is None:
            morceaux.append(np.zeros(n, dtype=np.float64))
        else:
            t = np.linspace(0, duree, n, endpoint=False)
            morceaux.append(0.4 * np.sin(2 * np.pi * freq * t))
    signal = np.concatenate(morceaux)
    signal_int16 = np.int16(np.clip(signal, -1.0, 1.0) * 32767)

    with wave.open(str(chemin), "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sr)
        f.writeframes(signal_int16.tobytes())


def test_transcrit_deux_notes_separees_par_un_silence(tmp_path):
    chemin = tmp_path / "test.wav"
    _ecrire_wav(chemin, [(440.0, 0.3), (None, 0.25), (659.25, 0.3)])

    segments = transcrire_fichier_audio(chemin)

    assert len(segments) == 2
    assert abs(segments[0]["freq"] - 440.0) < 3.0
    assert abs(segments[1]["freq"] - 659.25) < 4.0


def test_fichier_silencieux_ne_donne_aucun_segment(tmp_path):
    chemin = tmp_path / "silence.wav"
    _ecrire_wav(chemin, [(None, 0.5)])

    segments = transcrire_fichier_audio(chemin)
    assert segments == []
