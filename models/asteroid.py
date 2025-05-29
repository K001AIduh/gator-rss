import pygame
import random
import math
from utils.vector import Vector


class Asteroid:
    def __init__(self, position, size):
        self.position = position
        self.size = size  # 3 = large, 2 = medium, 1 = small
        self.velocity = Vector(random.uniform(-2, 2), random.uniform(-2, 2))

        # Radius depends on size
        self.radius = size * 10

        # Generate a random polygon shape
        self.vertices = []
        num_vertices = random.randint(7, 12)
        for i in range(num_vertices):
            angle = i * (2 * math.pi / num_vertices)
            distance = self.radius * random.uniform(0.8, 1.2)
            self.vertices.append(
                Vector(math.cos(angle) * distance, math.sin(angle) * distance)
            )

    def update(self, screen_width, screen_height):
        """Update the asteroid's position."""
        self.position = self.position + self.velocity

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
        """Draw the asteroid on the screen."""
        points = []
        for vertex in self.vertices:
            points.append(
                (int(self.position.x + vertex.x), int(self.position.y + vertex.y))
            )

        pygame.draw.polygon(screen, (255, 255, 255), points, 2)
