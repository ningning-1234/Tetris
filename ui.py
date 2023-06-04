import pygame

class UIManager:
    def __init__(self, pos=(0,0)):
        self.elements = []
        self.uiID = 0

    def add_elem(self,elem):
        self.elements.append(elem)
        elem.uiID = self.uiID
        self.uiID = self.uiID +1

    def remove_elem(self,elem):
        self.elements.remove(elem)

    def remove_elem_id(self, elem_id):
        pass

    def update(self, *args, **kwargs):
        for elem in self.elements:
            elem.update(args, kwargs)

    def draw(self, surface, *args, **kwargs):
        for elem in self.elements:
            elem.draw(surface, args, kwargs)

UI_MANAGER = UIManager()

class UIContainer:
    def __init__(self, pos, size):
        self.uiID = -1
        self.pos = pos
        self.size = size
        self.surface = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA,32)
        UI_MANAGER.add_elem(self)


    def update(self, *args, **kwargs):
        pass

    def draw(self, surface, *args, **kwargs):
        surface.blit(self.surface,self.pos)