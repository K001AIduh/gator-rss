import pygame
from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOOT_COOLDOWN,
)
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        # Call the parent class constructor with the player radius
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0  # Cooldown timer for shooting

    def rotate(self, dt):
        # Update the rotation by the specified amount
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt, direction=1):
        # Calculate the forward vector based on the player's rotation
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        # Move the player in the specified direction
        self.position += forward * PLAYER_SPEED * dt * direction

    def shoot(self):
        # Only allow shooting if the cooldown timer is 0
        if self.shoot_timer <= 0:
            # Reset the cooldown timer
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN

            # Create a shot at the player's position
            shot = Shot(self.position.x, self.position.y)

            # Set the shot's velocity in the direction the player is facing
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            shot.velocity = forward * PLAYER_SHOOT_SPEED

            return shot
        return None  # Return None if we can't shoot yet

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        # Decrease the shoot timer
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        keys = pygame.key.get_pressed()

        # Handle rotation
        if keys[pygame.K_a]:
            # Rotate left (negative direction)
            self.rotate(-dt)
        if keys[pygame.K_d]:
            # Rotate right (positive direction)
            self.rotate(dt)

        # Handle movement
        if keys[pygame.K_w]:
            # Move forward
            self.move(dt, 1)
        if keys[pygame.K_s]:
            # Move backward
            self.move(dt, -1)

    def draw(self, screen):
        # Draw the player as a white triangle
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
