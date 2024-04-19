from random import randint
import pygame
import sys
from player import Player
from environment import Floor, Obstacle, Spike
from home_screen import home_screen
from pause_menu import pause_menu

# Initialize Pygame
pygame.init()

# Constants for the game setup
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
FPS = 60
FLOOR_HEIGHT = 100
GROUND_LEVEL = SCREEN_HEIGHT - FLOOR_HEIGHT
CAMERA_SLACK = SCREEN_WIDTH // 3
MAX_OBSTACLE_DISTANCE = 300  # Maximum distance between two obstacles
background_image_path = 'C:/Users/rgora/OneDrive/Desktop/myProjects/2DGAME/pixel-art-landscape-of-pine-forest-in-the-mountains-with-lake-and-clouds-8-bit-game-background-vector.jpg'
floor_image_path = 'C:/Users/rgora/OneDrive/Desktop/myProjects/2DGAME/pixel-art-game-background-grass-sky-clouds_210544-60.jpg'

# Load and configure the background image for parallax scrolling
try:
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (background_image.get_width(), SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Failed to load background image: {e}")
    sys.exit()


# Load floor image
floor_image = pygame.image.load(floor_image_path)
floor_image = pygame.transform.scale(floor_image, (floor_image.get_width(), FLOOR_HEIGHT))

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jump Up Super Star")

def draw_progress(screen, progress):
    """Draws the progress on the screen."""
    font = pygame.font.Font(None, 36)  # Choose a suitable size and font
    text = font.render(f"Progress: {progress}m", True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 200, 20))  # Adjust positioning as needed

def game_loop():
    """Main game loop with camera tracking and dynamic obstacle management."""
    clock = pygame.time.Clock()
    player = Player()
    floor = Floor(0, GROUND_LEVEL, 9999999, 'C:/Users/rgora/OneDrive/Desktop/myProjects/2DGAME/pixel-art-game-background-grass-sky-clouds_210544-60.jpg')  # Update this path
    obstacles = []  # List to hold obstacles
    spikes = [Spike(800, GROUND_LEVEL), Spike(1400, GROUND_LEVEL)]  # Example spikes
    camera_x = 0  # Initial camera offset
    last_obstacle_x = 0  # X position where the last obstacle was placed
    last_x = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = pause_menu(screen)
                    if action == 'home':
                        home_screen(screen, background_image)
                        return  # Return to the home screen
                    elif action == 'continue':
                        continue  # Resume game
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Camera follow logic
        player.handle_keys()
        player.update(floor.segments, obstacles, spikes, SCREEN_HEIGHT, (50, 300))
        camera_x = max(0, player.rect.centerx - SCREEN_WIDTH // 2)
        background_x = -camera_x * 0.5 % background_image.get_width()

        # Dynamic generation of floor, obstacles, and spikes
        if camera_x + SCREEN_WIDTH > last_x:
            floor.add_more_segments(camera_x + SCREEN_WIDTH * 1.5)
            new_obstacles, last_x = Obstacle.generate_obstacles(last_x, camera_x + SCREEN_WIDTH * 1.5, GROUND_LEVEL - 50, GROUND_LEVEL, 50, 100, 10, 50)
            obstacles.extend(new_obstacles)
            spikes.append(Spike(last_x + randint(100, 500), GROUND_LEVEL - 20))
            last_x += SCREEN_WIDTH

        # Drawing the background with parallax effect
        for x_offset in range(int(background_x - background_image.get_width()), int(background_x + SCREEN_WIDTH), background_image.get_width()):
            screen.blit(background_image, (x_offset, 0))

        # Draw everything
        screen.fill((0, 0, 0))  # Clear the screen
        floor.draw(screen, camera_x)
        for obstacle in obstacles:
            obstacle.draw(screen, camera_x)
        for spike in spikes:
            spike.draw(screen, camera_x)
        player.draw(screen, camera_x)

        # Draw progress and update display
        draw_progress(screen, player.rect.x // 100)  # Assuming progress is simply x coordinate
        pygame.display.flip()
        clock.tick(FPS)

# Initially display the home screen and then start the game loop
home_screen(screen, background_image)
game_loop()


if __name__ == "__main__":
    game_loop()
