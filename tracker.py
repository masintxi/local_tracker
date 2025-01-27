import pygame
from constants import *
from circleshape import CircleShape
from local_tracker import Receiver, Tracker

class Trackedobj(Tracker, CircleShape):
    def __init__(self, name, x, y, color="blue"):
        super().__init__(name, x, y)
        CircleShape.__init__(self, name, x, y)
        self.radius = TRACKER_RADIUS
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.color = color

    @property
    def x(self):
        return self._Tracker__x  # Access the private __x
    
    @x.setter
    def x(self, value):
        self._Tracker__x = value
        return

    @property
    def y(self):
        return self._Tracker__y  # Access the private __y
    
    @y.setter
    def y(self, value):
        self._Tracker__y = value
        return
    
    def Draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        label = self.font.render(self.name, True, self.color)
        textRect = label.get_rect()
        textRect.topleft = (self.x + 10, self.y + 10)
        screen.blit(label, textRect)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= dt * TRACKER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += dt * TRACKER_SPEED
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= dt * TRACKER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += dt * TRACKER_SPEED

        self.x = max(0, min(SCREEN_WIDTH, self.x))
        self.y = max(0, min(SCREEN_HEIGHT, self.y))

