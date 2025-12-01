import winsound
import threading
import time

class AlarmService:
    def __init__(self):
        self._stop_event = threading.Event()
        self._thread = None

    def play_alarm(self):
        """Plays an alarm sound in a loop until stopped."""
        if self._thread and self._thread.is_alive():
            return  # Already playing

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._loop_sound)
        self._thread.daemon = True
        self._thread.start()

    def stop_alarm(self):
        """Stops the alarm sound."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1.0)
            self._thread = None

    def _loop_sound(self):
        while not self._stop_event.is_set():
            # Play a system sound. SND_ALIAS means it plays a system event sound.
            # SND_ASYNC would play it in background, but we are already in a thread.
            # We use SND_NODEFAULT to avoid silence if sound not found.
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_NODEFAULT)
            
            # Wait a bit before repeating to avoid machine-gun effect
            # winsound.PlaySound is synchronous unless SND_ASYNC is used.
            # SystemHand is usually short.
            time.sleep(1)
