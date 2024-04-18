import pygame
import random

class Floor:
    def __init__(self, x, y, total_width, image_path):
        # Load the image and scale it horizontally to fit the segment width
        self.original_image = pygame.image.load(image_path)
        self.height = 100  # Define the height of the floor
        self.segments = []
        self.generate_segments(x, y, total_width)

    def generate_segments(self, start_x, y, total_width):
        current_x = start_x
        while current_x < start_x + total_width:
            segment_width = random.randint(200, 400)  # Random segment width
            # Scale the image to fit each segment width and the specified height
            scaled_image = pygame.transform.scale(self.original_image, (segment_width, self.height))
            self.segments.append((pygame.Rect(current_x, y, segment_width, self.height), scaled_image))
            current_x += segment_width + random.randint(50, 150)  # Add gaps

    def draw(self, screen, camera_x):
        for segment, image in self.segments:
            if segment.x - camera_x + segment.width > 0 and segment.x - camera_x < screen.get_width():
                # Draw the image for the segment
                screen.blit(image, (segment.x - camera_x, segment.y))

class Obstacle:
    def __init__(self, x, y, width, height, color=(117, 113, 97)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, self.color, self.rect.move(-camera_x, 0))
