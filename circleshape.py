import pygame

class CircleShape(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.x = x
        self.y = y
        self.name = name

    def Draw(self, screen):
        pass

    def update(self, dt):
        pass