"""Capture audio en direct depuis le microphone (Module 1)."""

import threading

import numpy as np
import sounddevice as sd


class FluxAudio:
    """Flux micro continu exposant le dernier bloc audio capté.

    Utilise un callback sounddevice qui tourne dans un thread séparé ;
    `dernier_buffer()` peut être appelé depuis la boucle principale (console
    ou UI) sans bloquer la capture.
    """

    def __init__(self, samplerate: int = 44100, taille_bloc: int = 2048, device=None):
        self.samplerate = samplerate
        self.taille_bloc = taille_bloc
        self._buffer = np.zeros(taille_bloc, dtype=np.float32)
        self._lock = threading.Lock()
        self._stream = sd.InputStream(
            channels=1,
            samplerate=samplerate,
            blocksize=taille_bloc,
            callback=self._callback,
            device=device,
        )

    def _callback(self, indata, frames, time_info, status):
        with self._lock:
            self._buffer = indata[:, 0].copy()

    def dernier_buffer(self) -> np.ndarray:
        with self._lock:
            return self._buffer.copy()

    def demarrer(self):
        self._stream.start()

    def arreter(self):
        self._stream.stop()
        self._stream.close()

    def __enter__(self):
        self.demarrer()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.arreter()
