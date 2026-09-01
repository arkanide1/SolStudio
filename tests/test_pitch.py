import numpy as np

from solstudio.audio.pitch import detecter_pitch

SAMPLERATE = 44100


def _sinus(freq: float, sr: int = SAMPLERATE, duree: float = 0.3) -> np.ndarray:
    t = np.linspace(0, duree, int(sr * duree), endpoint=False)
    return (0.5 * np.sin(2 * np.pi * freq * t)).astype(np.float32)


def test_detecte_note_sol_corde_a_vide():
    freq = detecter_pitch(_sinus(196.00), SAMPLERATE)
    assert freq is not None
    assert abs(freq - 196.00) < 2.0


def test_detecte_note_la_corde_a_vide():
    freq = detecter_pitch(_sinus(440.00), SAMPLERATE)
    assert freq is not None
    assert abs(freq - 440.00) < 2.0


def test_detecte_note_mi_corde_a_vide():
    freq = detecter_pitch(_sinus(659.25), SAMPLERATE)
    assert freq is not None
    assert abs(freq - 659.25) < 3.0


def test_silence_retourne_none():
    buffer = np.zeros(4096, dtype=np.float32)
    assert detecter_pitch(buffer, SAMPLERATE) is None


def test_bruit_faible_retourne_none():
    rng = np.random.default_rng(0)
    buffer = (rng.normal(0, 0.0005, 4096)).astype(np.float32)
    assert detecter_pitch(buffer, SAMPLERATE) is None
