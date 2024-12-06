import time
import threading

class Clock:

    def __init__(self, fps: int) -> None:
        self.fps = fps
        self.frametime = 1 / self.fps
        self.frames = 0
        self.t2 = time.perf_counter()
        self.ft = time.perf_counter()
        self._thread = threading.Thread(target=self._reset_fpsstat)
        self._thread.start()

    def stamp(self):
        self.t2 = time.perf_counter()

    def wait(self):
        self.frames += 1
        while time.perf_counter() - self.t2 < self.frametime:
            pass

    def get_fps(self): return (self.frames / (time.perf_counter() - self.ft))

    def _reset_fpsstat(self):
        while True:
            self.frames = 0
            self.ft = time.perf_counter()
            time.sleep(5)