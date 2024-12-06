import sdl2.sdlimage as sdlimage
import gc

class ResourceCollector:
    
    def __init__(self) -> None:
        pass

    def clear(self):
        gc.collect()

class ResourceManager:

    def __init__(self) -> None:
        self.collector = ResourceCollector()

    def load_image(self, path: str):
        image = sdlimage.IMG_Load(path.encode())
        if image is None:
            return None
        return image
    
    def free_image(self, image):
        sdlimage.IMG_Quit()
        self.collector.clear()