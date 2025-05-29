import pygame
from vector import Vector


class Bullet:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.radius = 3
        self.lifetime = 1.5  # seconds

    def update(self, dt, screen_width, screen_height):
        """Update bullet position and lifetime."""
        # Update position
        self.position = self.position + self.velocity * dt

        # Decrease lifetime
        self.lifetime -= dt

        # Wrap around screen edges
        if self.position.x < 0:
            self.position.x = screen_width
        elif self.position.x > screen_width:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = screen_height
        elif self.position.y > screen_height:
            self.position.y = 0

    def draw(self, screen):
        """Draw the bullet as a small white circle."""
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(self.position.x), int(self.position.y)),
            self.radius,
        )
