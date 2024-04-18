import pygame

# Constants for player attributes
PLAYER_SIZE = 50
PLAYER_COLOR = (255, 0, 0)  # Red color for the player
GRAVITY = 0.5
JUMP_SPEED = -10
GROUND_Y = 980  # This should be 1080 - 100 (if the floor's height is 100 and starts 100 pixels up from the bottom)

class Player:
    def __init__(self):
        # Initialize player properties
        self.rect = pygame.Rect(860, 500, PLAYER_SIZE, PLAYER_SIZE)  # Central horizontal start
        self.velocity_y = 0  # Vertical velocity
        self.on_ground = False  # Flag to check if the player is on the ground
        self.left_boundary = 0  # Left boundary of the floor

    def handle_keys(self):
        # Handle key presses for left, right movement and jumping
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > self.left_boundary:
            self.rect.x -= 5  # Move left only if not at the left boundary
        if keys[pygame.K_d]:
            self.rect.x += 5  # Move right
        if keys[pygame.K_w] and self.on_ground:
            self.jump()  # Perform jump

    def jump(self):
        # Initiate jumping
        self.velocity_y = JUMP_SPEED
        self.on_ground = False

    def update(self, floors, obstacles, screen_height, start_position):
        # Apply gravity to player's vertical velocity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Reset ground flag
        self.on_ground = False

        # Check for collision with floor segments
        for floor in floors:
            if floor.colliderect(self.rect):
                self.rect.bottom = floor.top
                self.velocity_y = 0
                self.on_ground = True
                break

        # Check for falling below the screen
        if self.rect.bottom > screen_height:
            # Teleport the player back to the starting position if they fall through a hole
            self.rect.x, self.rect.y = start_position
            self.velocity_y = 0

    def draw(self, screen, camera_x):
        # Draw the player adjusted for camera position
        camera_adjusted_rect = self.rect.copy()
        camera_adjusted_rect.x -= camera_x
        pygame.draw.rect(screen, PLAYER_COLOR, camera_adjusted_rect)
