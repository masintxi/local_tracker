import pygame
from constants import *
from tracker import Trackedobj
from receiver import Receiverobj
from rec_update import init_receivers, update_receivers

def main():
    pygame.init()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Trackedobj.containers = (updatable, drawable)
    Receiverobj.containers = (drawable)
 
    screen = pygame.display.set_mode ((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(SCREEN_NAME)
    image = pygame.image.load('images/sample_layout.png')

    clock = pygame.time.Clock()
    dt = 0

    receivers = init_receivers()
    tr = Trackedobj("John", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        screen.fill("lightgrey")
        screen.blit(image, (0, 0))

        update_receivers(screen, receivers, tr)

        for sprite in updatable:
            sprite.update(dt)
        
        for sprite in drawable:
            sprite.Draw(screen)


        pygame.display.flip()

        dt = clock.tick(60) / 1000
    

if __name__ == "__main__":
    main()