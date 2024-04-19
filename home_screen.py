import pygame
import sys
import random

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def home_screen(screen, background_image):
    font = pygame.font.Font(None, 36)
    large_font = pygame.font.Font(None, 72)
    title = "Jump Up Super Star"
    quotes = [
        "\"Get over here!\"",
        "\"What is better? To be born good or to overcome your evil nature through great effort?\"",
        "\"The right man in the wrong place can make all the difference in the world.\"",
        "\"The right man in the wrong place can make all the difference in the world.\"",
        "\"Bring me a bucket, and I'll show you a bucket!\"",
        "\"Wanting something does not give you the right to have it.\"",
        "\"A hero need not speak. When he is gone, the world will speak for him.\"",
        "\"No gods or kings. Only man.\"",
        "\"It's time to kick ass and chew bubblegum... and I'm all outta gum.\"",
        "\“…”",
        "\"If our lives are already written, it would take a courageous man to change the script.\"",
        "\"It's easy to forget what a sin is in the middle of a battlefield.\"",
        "\"Don't wish it were easier, wish you were better.\"",
        "\"Trust me.\"",
        "\"Nothing is true, everything is permitted.\"",
        "\"Nothing is more badass than treating a woman with respect!\"",
        "\"It’s dangerous to go alone, take this!\"",
        "\"War. War never changes.\"",
        "\"AAAAAAAAAAAAHHHRHGHHHGH thump\"",
        "\"Protocol one: link to Pilot. Protocol two: uphold the mission. Protocol three: protect the Pilot.\"",
        "\"I miss the internet\"",
        "\"Stay awhile, and listen!\"",
        "\"Thank you Mario! But our Princess is in another castle!\"",
        "\"It's a-me, Mario!\"",
        "\"…*cocks shotgun*\"",
        "\"Finish him!\"",
        "\"Snake? Snake? SNAAAAAAAAKE!!!\"",
        "\"Grass grows, birds fly, sun shines, and brother, I hurt people.\"",
        "\"Hey! Listen!\""
    ]
    angle_text = random.choice(quotes)
    angle_text_alpha = 255
    fading_out = True

    button_play = pygame.Rect(screen.get_width() / 2 - 150, screen.get_height() / 2 - 50, 300, 50)
    button_quit = pygame.Rect(screen.get_width() / 2 - 150, screen.get_height() / 2 + 10, 300, 50)

    running = True
    while running:
        screen.blit(background_image, (0, 0))
        if fading_out:
            angle_text_alpha -= 5
            if angle_text_alpha < 50:
                fading_out = False
        else:
            angle_text_alpha += 5
            if angle_text_alpha > 255:
                fading_out = True

        text_surface = font.render(angle_text, True, (255, 255, 255))
        text_surface.set_alpha(angle_text_alpha)
        draw_text(title, large_font, (255, 255, 255), screen, screen.get_width() / 2, 100)
        draw_text(angle_text, font, (255, 255, 255), screen, screen.get_width() * 0.5, 200)
        pygame.draw.rect(screen, [0, 0, 255], button_play)
        draw_text('Play', font, (255, 255, 255), screen, button_play.centerx, button_play.centery)
        pygame.draw.rect(screen, [0, 0, 255], button_quit)
        draw_text('Quit', font, (255, 255, 255), screen, button_quit.centerx, button_quit.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.collidepoint(event.pos):
                    running = False  # Close the home screen
                elif button_quit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()