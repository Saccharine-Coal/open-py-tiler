import imp
import pygame

import animation

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
FPS = 60  # Frames per second.

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# RED = (255, 0, 0), GREEN = (0, 255, 0), BLUE = (0, 0, 255).

rect = pygame.Rect((0, 0), (32, 32))
image = pygame.Surface((32, 32))
image .fill(WHITE)

running = True

import os
path_to_animation = os.path.join("assets", "animations", "player_rotation")
anim = animation.Animation(path_to_animation)

while running:
    getTicksLastFrame = 0
    tick = clock.tick(FPS) 
    dt = tick / 1000.0
    anim.update(dt*10)
    print(tick)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("quit event")
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                rect.move_ip(0, -2)
            elif event.key == pygame.K_s:
                rect.move_ip(0, 2)
            elif event.key == pygame.K_a:
                rect.move_ip(-2, 0)
            elif event.key == pygame.K_d:
                rect.move_ip(2, 0)
    screen.fill((255, 100, 100))
    anim.draw(screen)
    pygame.display.flip()  # Or pygame.display.flip()
pygame.display.quit()
