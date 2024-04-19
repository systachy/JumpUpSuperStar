import pygame
from random import randint

class Floor:
    def __init__(self, x, y, total_width, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.image.get_width(), 100))
        self.segments = []
        self.generate_floor(x, y, total_width)

    def generate_floor(self, start_x, y, total_width):
        current_x = start_x
        while current_x < start_x + total_width:
            self.segments.append((pygame.Rect(current_x, y, self.image.get_width(), self.image.get_height()), self.image))
            current_x += self.image.get_width()

    def draw(self, screen, camera_x):
        for segment, image in self.segments:
            if segment.x - camera_x < 1980:  # Draw only visible segments
                screen.blit(image, (segment.x - camera_x, segment.y))

    def add_more_segments(self, end_x):
        last_x = self.segments[-1][0].x + self.image.get_width()
        while last_x < end_x:
            self.segments.append((pygame.Rect(last_x, self.segments[0][0].y, self.image.get_width(), self.image.get_height()), self.image))
            last_x += self.image.get_width()


class Obstacle:
    def __init__(self, x, y, width, height, color=(117, 113, 97)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, self.color, self.rect.move(-camera_x, 0))

    def generate_obstacles(start_x, end_x, min_y, max_y, min_width, max_width, min_height, max_height):
        obstacles = []
        current_x = start_x
        while current_x < end_x:
            width = randint(min_width, max_width)
            height = randint(min_height, max_height)
            y = max_y - height  # Ensure the obstacle is fully visible
            obstacles.append(Obstacle(current_x, y, width, height))
            current_x += width + randint(50, 200)  # Distance between obstacles
        return obstacles, current_x


class Spike:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y - 20, 40, 20)  # Assuming spike height of 20
        self.color = (230, 10, 80)  # Dark grey color

    def draw(self, screen, camera_x):
        # Draw a triangle spike
        pygame.draw.polygon(screen, self.color, [(self.rect.x - camera_x, self.rect.y + self.rect.height),
                                                 (self.rect.x - camera_x + self.rect.width / 2, self.rect.y),
                                                 (self.rect.x - camera_x + self.rect.width, self.rect.y + self.rect.height)])
