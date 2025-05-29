import pygame
from utils.vector import Vector


class Bullet:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.radius = 3
        self.lifetime = 60  # Number of frames bullet exists for

    def update(self, screen_width, screen_height):
        """Update the bullet's position and lifetime."""
        self.position = self.position + self.velocity
        self.lifetime -= 1

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
        """Draw the bullet on the screen."""
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(self.position.x), int(self.position.y)),
            self.radius,
        )
