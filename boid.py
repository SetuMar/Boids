import math
import pygame
import random
from settings import *

class Boid:
    # radius of each boid
    BOID_RADIUS = 3
    
    # sight of each boid
    SIGHT_RADIUS = 40
    
    # speed of each boid
    speed = 10
    
    # force values
    alignment_force = 0.5
    cohesion_force = 0.5
    separation_force = 1
    
    def __init__(self, position:pygame.Vector2) -> None:
        # boid position
        self.position = position
        
        # random color
        self.color = tuple(random.randint(50, 255) for i in range(3))
        
        # random speed of movement
        speed = random.uniform(2, 5)
        # direction of movement
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
        
        # rate of change in velocity
        self.acceleration = pygame.Vector2(0, 0)
        
    def apply_rules(self, boids):
        # force for alignment
        alignment_force = pygame.Vector2(0, 0)
        # force for cohesion
        cohesion_force = pygame.Vector2(0, 0)
        # force for separation
        separation_force = pygame.Vector2(0, 0)
        
        # number of boids
        num_boids = 0
        
        for b in boids:
            # get distance to other boid
            current_boid_distance = pygame.Vector2.distance_to(b.position, self.position)
            
            # check if boid in radius and looping boid is not current
            if current_boid_distance <= Boid.SIGHT_RADIUS and b != self:
                # add velocity to steering force
                alignment_force += b.velocity
                cohesion_force += b.position
                
                # inversely use distance to nearest boid to determine separation force
                diff = (self.position - b.position)
                
                # cannot use overlapping distance (pray this doesn't happen too often 🙏)
                if diff != pygame.Vector2(0, 0):
                    separation_force += (self.position - b.position).normalize() * Boid.separation_force / current_boid_distance
                else:
                    separation_force = pygame.Vector2(0, 0)
                
                # add to num boids
                num_boids += 1
        
        # if there are nearby boids, do the calculation
        if num_boids > 0:
            
            # determine steering velocity (force needed)
            alignment_force /= num_boids
            cohesion_force /= num_boids
            separation_force /= num_boids

            # vector in direction of movement (from boid to cohesion point)
            cohesion_force -= self.position
            
            # ensure consistent steering force for all boids (all steering is of the same force)
            alignment_force = Boid.set_magnitude(alignment_force, Boid.speed)
            cohesion_force = Boid.set_magnitude(cohesion_force, Boid.speed)
            separation_force = Boid.set_magnitude(separation_force, Boid.speed)
            
            # determine direction of steering and cohesion velocity
            alignment_force -= self.velocity
            cohesion_force -= self.velocity
            separation_force -= self.velocity
            
            # limit the speed of each boid (each boid cannot travel faster than a max speed)
            alignment_force = Boid.limit_magnitude(alignment_force, Boid.alignment_force)
            cohesion_force = Boid.limit_magnitude(cohesion_force, Boid.cohesion_force)
            separation_force = Boid.limit_magnitude(separation_force, Boid.separation_force)

            # add to acceleration
            self.acceleration = alignment_force + cohesion_force + separation_force

    def update(self):
        # update position by velocity (accleration is rate of change in position (distance) over time)
        self.position += self.velocity
        # update velocity by acceleration (accleration is rate of change in velocity over time)
        self.velocity += self.acceleration
        
        # screen wrapping
        if self.position.x < 0: self.position.x = WIDTH
        if self.position.x > WIDTH: self.position.x = 0
        if self.position.y > HEIGHT: self.position.y = 0
        if self.position.y < 0: self.position.y = HEIGHT
        
    def draw(self, display):
        # draw to display
        pygame.draw.circle(display, self.color, self.position, Boid.BOID_RADIUS)
    
    # return list of x number of boids
    @staticmethod
    def generate_boids(num_boids:int) -> list:
        return [Boid(pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))) for x in range(num_boids)]
    
    # set magnitude of a vector
    @staticmethod
    def set_magnitude(v:pygame.Vector2, desired_mag:int):
        # get magnitude of vector
        mag = v.magnitude()
        
        # if not zero vector
        if mag > 0:
            # determine scale amount
            mag_scale_amt = desired_mag / mag
            
            # scale the vector accordingly
            return v * mag_scale_amt
        
        # return zero vector
        return v
    
    # limit magnitude of a vector
    @staticmethod
    def limit_magnitude(v:pygame.Vector2, max_desired:int):
        # get magnitude of vector
        mag = v.magnitude()
        
        # if not zero vector
        if mag > 0:
            # determine scale amount (how much to change scale of the vector by)
            mag_scale = max_desired / mag
            
            # rescale vector accordingly
            if mag_scale < 1: return v * mag_scale
        
        # return vector if mag_scale is needed or if 0 vector
        return v