import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        # Call the parent class constructor
        super().__init__(x, y, radius)

    def update(self, dt):
        # Move the asteroid in a straight line at constant speed
        self.position += self.velocity * dt

    def split(self):
        # Always destroy this asteroid
        self.kill()

        # If this is a small asteroid, we're done
        if self.radius <= ASTEROID_MIN_RADIUS:
            return []

        # Calculate the new radius for the smaller asteroids
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Generate a random angle between 20 and 50 degrees for splitting
        random_angle = random.uniform(20, 50)

        # Create two new velocity vectors by rotating the current velocity
        velocity1 = self.velocity.rotate(random_angle)
        velocity2 = self.velocity.rotate(-random_angle)

        # Make the new asteroids move faster
        velocity1 *= 1.2
        velocity2 *= 1.2

        # Create two new smaller asteroids
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = velocity1

        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = velocity2

        # Return the new asteroids so they can be added to the game
        return [asteroid1, asteroid2]

    def draw(self, screen):
        # Draw the asteroid as a circle
        pygame.draw.circle(
            screen,
            "white",
            (int(self.position.x), int(self.position.y)),
            self.radius,
            2,
        )
