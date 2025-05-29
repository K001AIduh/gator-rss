# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
import sys
import time
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initialize pygame
    pygame.init()

    # Set up the display window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")

    # Create a clock for controlling FPS
    clock = pygame.time.Clock()

    # Create groups for game objects
    updatable = pygame.sprite.Group()  # Objects that can be updated
    drawable = pygame.sprite.Group()  # Objects that can be drawn
    asteroids = pygame.sprite.Group()  # All asteroids
    shots = pygame.sprite.Group()  # All shots

    # Set containers for the different classes
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (
        updatable,
    )  # AsteroidField is only updatable, not drawable
    Shot.containers = (shots, updatable, drawable)

    # Create player at center of screen
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Delay asteroid field creation to give the player a safe start
    asteroid_field = None
    start_time = time.time()
    safe_delay = 2.0  # seconds

    # Delta time variable
    dt = 0

    # Game loop
    while True:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle space key for shooting
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Create a new shot
                    shot = player.shoot()
                    # Only add the shot if it's not None (cooldown not active)
                    if shot is not None:
                        pass  # The shot is automatically added to the groups via containers

        # Create asteroid field after delay
        if asteroid_field is None and time.time() - start_time > safe_delay:
            asteroid_field = AsteroidField()

        # Update all updatable objects
        updatable.update(dt)

        # Check for collisions between player and asteroids
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                print("Game over!")
                pygame.quit()
                sys.exit()

        # Check for collisions between shots and asteroids
        for shot in list(
            shots
        ):  # Make a copy of the shots group to avoid modification during iteration
            for asteroid in list(asteroids):  # Make a copy of the asteroids group
                # Check if shot collides with asteroid
                if shot.collides_with(asteroid):
                    # Kill the shot and split the asteroid
                    shot.kill()
                    new_asteroids = (
                        asteroid.split()
                    )  # This will handle asteroid destruction and splitting
                    # Add the new asteroids to the game
                    for new_asteroid in new_asteroids:
                        asteroids.add(new_asteroid)
                        updatable.add(new_asteroid)
                        drawable.add(new_asteroid)
                    break  # Break after destroying one asteroid per shot

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw all drawable objects
        for drawable_object in drawable:
            drawable_object.draw(screen)

        # Update the display
        pygame.display.flip()

        # Control the frame rate and update dt
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
