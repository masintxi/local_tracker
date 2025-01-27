import pygame
from constants import *
from circleshape import CircleShape
from local_tracker import Receiver

class Receiverobj(CircleShape, Receiver):
    def __init__(self, name, x, y, color="green"):
        super().__init__(name, x, y)
        self.color = color
        self.radius = RECEIVER_RADIUS
        self.is_alive = True
        self.is_active = False
        self.is_primary = False
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.text = self.name

    def Draw(self, screen):
        if not self.is_alive:
            return
        if self.is_active:
            self.color = "orange"
        else:
            self.color = "green"
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        label = self.font.render(self.text, True, self.color)
        textRect = label.get_rect()
        textRect.topleft = (self.x + 10, self.y - 15)
        screen.blit(label, textRect)

    def update(self, dt):
        pass

    def locate(self, tracked):
        self.text = f"{self.name}: {tracked.report(self):.2f}"
        return
