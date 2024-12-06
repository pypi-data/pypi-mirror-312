import sdl2
import sdl2.ext as sdlext
from .clock import Clock

class Window:

    def __init__(self, title: str, width: int, height: int, **kwargs):
        self.title = title
        self.width = width
        self.height = height
        self.kwargs = kwargs
        self.fullscreen = sdl2.SDL_WINDOW_FULLSCREEN
        self.fullscreen_desktop = sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP
        self.bordeless = sdl2.SDL_WINDOW_BORDERLESS
        self.resizable = sdl2.SDL_WINDOW_RESIZABLE

        self.fps = self._getKwarg('fps', 60, int)
        self.display = self._getKwarg('display', 0, int)
        self.screensize = (sdlext.DisplayInfo(self.display).current_mode.w, sdlext.DisplayInfo(self.display).current_mode.h)
        self.showpos = self._getKwarg('pos', ((self.screensize[0] // 2)-self.width//2, (self.screensize[1] // 2)-self.height//2), tuple)
        self.flags = (self._getKwarg('flags', 0) | self.fullscreen_desktop if self._getKwarg('fullscreen', False) else 0 | self.bordeless if self._getKwarg('borderless', False) else 0 | self.resizable if self._getKwarg('resizable', False) else 0)
        self.screen = sdlext.Window(title, (width, height), self.showpos, self.flags)
        self.clock = Clock(60)

    def _getKwarg(self, key, default, type: None = None):
        q = self.kwargs.get(key, default)
        if type is not None and q != default: q = type(q)
        return q
    
    def show(self): self.screen.show()
    def minimize(self): self.screen.minimize()
    def hide(self): self.screen.hide()
    def maximize(self): self.screen.maximize()
    def restore(self): self.screen.restore()
    def close(self): self.screen.close()
    def create(self): self.screen.create()