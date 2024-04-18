import pygame
import sys
import random
from player import Player
from environment import Floor, Obstacle

# Initialize Pygame
pygame.init()

# Constants for the game setup
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
FPS = 60
FLOOR_HEIGHT = 100
GROUND_LEVEL = SCREEN_HEIGHT - FLOOR_HEIGHT
CAMERA_SLACK = SCREEN_WIDTH // 3
MAX_OBSTACLE_DISTANCE = 300  # Maximum distance between two obstacles
background_image_path = 'C:/Users/rgora/OneDrive/Desktop/myProjects/2DGAME/pixel-art-landscape-of-pine-forest-in-the-mountains-with-lake-and-clouds-8-bit-game-background-vector.jpg'  # Path to the background image
floor_image_path = 'C:/Users/rgora/OneDrive/Desktop/myProjects/2DGAME/pixel-art-game-background-grass-sky-clouds_210544-60.jpg'  # Path to the floor image

# Load the background image and scale it to the screen height
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (background_image.get_width(), SCREEN_HEIGHT))
background_x = 0  # Initial background x-coordinate

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jump Up Super Star")

def game_loop():
    clock = pygame.time.Clock()
    player = Player()
    player.left_boundary = 0 # Assuming floor starts at x=0
    floor = Floor(0, SCREEN_HEIGHT - 100, 3000, floor_image_path)  # Initialize the floor with the provided image
    obstacles = [Obstacle(600, GROUND_LEVEL - 150, 50, 50), Obstacle(1200, GROUND_LEVEL - 150, 80, 50)]  # Initial obstacles
    last_obstacle_x = 1200  # Starting x-coordinate for dynamic obstacle generation
    camera_x = 0
    start_position = (50, 300)  # Player's start position

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.handle_keys()
        player.update(floor.segments, obstacles, SCREEN_HEIGHT, start_position) # Update player state with floor and obstacle collisions

        # Camera follow logic
        if player.rect.centerx > camera_x + SCREEN_WIDTH - CAMERA_SLACK:
            camera_x = player.rect.centerx - (SCREEN_WIDTH - CAMERA_SLACK)
        elif player.rect.centerx < camera_x + CAMERA_SLACK:
            camera_x = player.rect.centerx - CAMERA_SLACK

        background_x = -camera_x % background_image.get_width()  # Calculate background position for scrolling

        # Drawing section
        screen.fill((0, 0, 0))  # Clear screen
                # Draw the background in a loop to cover the entire screen width
        for x in range(background_x - background_image.get_width(), SCREEN_WIDTH, background_image.get_width()):
            screen.blit(background_image, (x, 0))
        
        floor.draw(screen, camera_x)  # Draw the floor with segments
        for obstacle in obstacles:
            obstacle.draw(screen, camera_x)  # Draw each obstacle
        player.draw(screen, camera_x)  # Draw the player

        pygame.display.flip()  # Update the display
        clock.tick(FPS)  # Maintain the frame rate

if __name__ == "__main__":
    game_loop()
