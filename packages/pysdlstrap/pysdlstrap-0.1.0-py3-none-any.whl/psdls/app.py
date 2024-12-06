import sdl2.ext as sdlext
import sdl2
import sdl2.events as sdlevents
import threading
from .window import Window
from .resource import ResourceManager
import os

class App:

    def __init__(self, title: str, width: int, height: int,**kwargs) -> None:
        os.chdir(os.path.dirname(__file__))
        sdlext.init()
        self.title = title
        self.width = width
        self.height = height
        self.kwargs = kwargs
        self.executepath = os.path.dirname(__file__)

        self.running = False
        self.screen = Window(title, width, height, **kwargs)
        self.resource = ResourceManager()
        self.handlers = {}
        self.events = {}
    
    def run(self):
        self._loop()

    def quit(self): 
        self.running = False
        sdlext.quit()
    
    def hide(self): self.screen.hide()

    def minimize(self): self.screen.minimize()

    def addevent(self, event, func, *args, **kwargs): self.events[event] = {"func" : func, "args" : args, "kwargs" : kwargs}

    def addhandler(self, func, args: tuple, kwargs: dict = {}):
        self.handlers[func] = {"args" : args, "kwargs" : kwargs}

    def _loop(self):
        self.running = True
        self.screen.show()
        while self.running:

            self.screen.clock.stamp()

            for event in sdlext.get_events():
                for k, v in self.events.items():
                    if event.type == k:
                        v['func'](*v['args'], **v['kwargs'])

            for k, v in self.handlers.items():
                k(*v["args"], **v["kwargs"])

            self.screen.clock.wait()
            self.screen.screen.refresh()

        self.screen.close()