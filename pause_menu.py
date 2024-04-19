import sys
import pygame

def pause_menu(screen):
    pygame.font.init()
    font = pygame.font.SysFont(None, 48)
    continue_text = font.render("Resume Game", True, (255, 255, 255))
    home_text = font.render("Return to Home Screen", True, (255, 255, 255))
    continue_button = continue_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 40))
    home_button = home_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 40))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    return 'continue'
                elif home_button.collidepoint(event.pos):
                    return 'home'
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))  # Clear screen or set to a pause background
        screen.blit(continue_text, continue_button)
        screen.blit(home_text, home_button)
        pygame.display.flip()

    return 'continue'  # Default to continue if loop exits without button selection
