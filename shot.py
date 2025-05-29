import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS


class Shot(CircleShape):
    def __init__(self, x, y):
        # Call parent constructor with the shot radius
        super().__init__(x, y, SHOT_RADIUS)

    def update(self, dt):
        # Move the shot in a straight line at constant speed
        self.position += self.velocity * dt

    def draw(self, screen):
        # Draw the shot as a small white circle
        pygame.draw.circle(
            screen, "white", (int(self.position.x), int(self.position.y)), self.radius
        )
