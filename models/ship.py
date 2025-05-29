import pygame
import math
from utils.vector import Vector
from models.bullet import Bullet


class Ship:
    def __init__(self, position):
        self.position = position
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.angle = 0  # Angle in degrees, 0 is up
        self.radius = 15
        self.max_speed = 5

    def rotate(self, angle_change):
        """Rotate the ship by the given angle change."""
        self.angle += angle_change
        # Keep angle between 0 and 360
        self.angle %= 360

    def accelerate(self, thrust):
        """Apply thrust in the direction the ship is facing."""
        # Convert angle to direction vector
        direction = Vector(0, -1).rotate(self.angle)
        # Apply thrust in that direction
        self.velocity = self.velocity + direction * thrust

        # Limit speed
        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

    def update(self, screen_width, screen_height):
        """Update the ship's position based on velocity."""
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

    def shoot(self):
        """Create a bullet in the direction the ship is facing."""
        # Get direction vector
        direction = Vector(0, -1).rotate(self.angle)
        # Create bullet at ship's position plus a bit in the direction to avoid collision
        bullet_pos = self.position + direction * (self.radius + 5)
        # Create bullet with direction and some speed
        return Bullet(bullet_pos, direction * 10)

    def draw(self, screen):
        """Draw the ship on the screen."""
        # Calculate the three points of the triangle
        angle_rad = math.radians(self.angle)

        # Ship points as offsets from center
        point1 = Vector(0, -self.radius)  # Nose of the ship
        point2 = Vector(-self.radius, self.radius)  # Bottom left
        point3 = Vector(self.radius, self.radius)  # Bottom right

        # Rotate points
        point1 = point1.rotate(self.angle)
        point2 = point2.rotate(self.angle)
        point3 = point3.rotate(self.angle)

        # Add center position to get actual screen coordinates
        point1 = (int(self.position.x + point1.x), int(self.position.y + point1.y))
        point2 = (int(self.position.x + point2.x), int(self.position.y + point2.y))
        point3 = (int(self.position.x + point3.x), int(self.position.y + point3.y))

        # Draw the triangle
        pygame.draw.polygon(screen, (255, 255, 255), [point1, point2, point3], 2)
