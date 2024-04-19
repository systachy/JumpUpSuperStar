import pygame

# Constants for player attributes
PLAYER_SIZE = 50
PLAYER_COLOR = (255, 0, 0)  # Red color for the player
GRAVITY = 0.5
JUMP_SPEED = -13
GROUND_Y = 980  # Adjusted to actual gameplay screen size minus floor height

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

    def update(self, floors, obstacles, spikes, screen_height, start_position):
        # Apply gravity to player's vertical velocity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Reset ground flag
        self.on_ground = False

        # Check for collision with floor segments
        for segment, _ in floors:  # Unpack the tuple here
            if segment.colliderect(self.rect):
                self.rect.bottom = segment.top
                self.velocity_y = 0
                self.on_ground = True
                break

        # Check for collision with obstacles
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                # Check if landing on the obstacle
                if self.velocity_y > 0 and self.rect.bottom <= obstacle.rect.top + 10:
                    # Correctly landing on the obstacle
                    self.rect.bottom = obstacle.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0 and self.rect.top >= obstacle.rect.bottom - 10:
                    # Hitting the obstacle from below
                    self.rect.top = obstacle.rect.bottom
                    self.velocity_y = 0
                else:
                    # Determine the side collision based on the center points
                    if self.rect.centerx < obstacle.rect.centerx:
                        # Collision from left
                        self.rect.right = obstacle.rect.left
                    else:
                        # Collision from right
                        self.rect.left = obstacle.rect.right

        # Check for collision with spikes
        for spike in spikes:
            if self.rect.colliderect(spike.rect):
                self.rect.x, self.rect.y = start_position  # Reset to start position
                self.velocity_y = 0
                return  # Early return to ensure we don't run further checks

        # Check if player falls below the screen
        if self.rect.bottom > screen_height:
            self.rect.x, self.rect.y = start_position
            self.velocity_y = 0



            # Check for collision with spikes
            for spike in spikes:
                if self.rect.colliderect(spike.rect):
                    self.rect.x, self.rect.y = start_position  # Teleport to start position
                    self.velocity_y = 0
                    return  # Early return to ensure we don't run further checks

            # Check if player falls below the screen
            if self.rect.bottom > screen_height:
                # Teleport the player back to the starting position if they fall through a hole
                self.rect.x, self.rect.y = start_position
                self.velocity_y = 0

    def draw(self, screen, camera_x):
        # Draw the player adjusted for camera position
        camera_adjusted_rect = self.rect.copy()
        camera_adjusted_rect.x -= camera_x
        pygame.draw.rect(screen, PLAYER_COLOR, camera_adjusted_rect)
