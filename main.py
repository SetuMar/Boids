import pygame
pygame.font.init()
import sys

from boid import Boid
from settings import *

from slider import Slider

screen_size = (WIDTH, HEIGHT)
pygame.init()

display = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# list of all boids
boids = Boid.generate_boids(300)

alignment_slider = Slider(0.5, 0, 5, 0.5, pygame.Vector2(12, 25), 165, 10, (255, 0, 0), 8, (255, 255, 255), "Alignment:", 15, (255, 255, 255))
cohesion_slider = Slider(0.5, 0, 5, 0.5, pygame.Vector2(12, 75), 165, 10, (0, 255, 0), 8, (255, 255, 255), "Cohesion:", 15, (255, 255, 255))
separation_slider = Slider(1, 0, 10, 0.5, pygame.Vector2(12, 125), 165, 10, (0, 0, 255), 8, (255, 255, 255), "Separation:", 15, (255, 255, 255))

boid_speed_slider = Slider(7.5, 5, 15, 0.25, pygame.Vector2(12, 175), 165, 10, (0, 255, 255), 8, (255, 255, 255), "Boid Speed:", 15, (255, 255, 255))

setting_shown = False

while True:
    display.fill('black')
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if setting_shown: setting_shown = False
                else: setting_shown = True
            
            
    if setting_shown:
        # set forces to slider values
        Boid.alignment_force = alignment_slider.slide()
        Boid.cohesion_force = cohesion_slider.slide()
        Boid.separation_force = separation_slider.slide()
        Boid.speed = boid_speed_slider.slide()
    
    for b in boids:
        # apply rules to all boids
        b.apply_rules(boids)
        
        # update all boids
        b.update()
        
        # draw all boids
        b.draw(display)
    
    # draw sliders
    if setting_shown:
        alignment_slider.draw(display)
        cohesion_slider.draw(display)
        separation_slider.draw(display)
        boid_speed_slider.draw(display)

    pygame.display.update()
    clock.tick(60)