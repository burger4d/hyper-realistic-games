import pygame

def main():
    pygame.init()


    WINDOW_SIZE = (800, 600)

    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption('Infinite Screen Menu')

    background_image = pygame.image.load('screen.png')

    background_rect = background_image.get_rect()
    background_rect.center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2)

    font = pygame.font.Font(None, 36)

    title_text = font.render('Infinite Screen Menu', True, (255, 255, 255))

    title_pos = (WINDOW_SIZE[0] / 2 - title_text.get_width() / 2, 50)

    button1_text = font.render('Asteroid', True, (255, 255, 255))
    button2_text = font.render( 'The forest', True, (255, 255, 255))

    button1_pos = (WINDOW_SIZE[0] / 2 - button1_text.get_width() / 2, 200)
    button2_pos = (WINDOW_SIZE[0] / 2 - button2_text.get_width() / 2, 300)
    
    button_size = (200, 50)

    button1_rect = pygame.Rect(button1_pos, button_size)
    button2_rect = pygame.Rect(button2_pos, button_size)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button1_rect.collidepoint(event.pos):
                    print('Button 1 clicked - pass')
                    pygame.quit()
                    exec("from asteroids import game_asteroids, asteroids_init, menu_asteroids\nasteroids_init()\nmenu_asteroids()")
                elif button2_rect.collidepoint(event.pos):
                    print('Button 2 clicked - pass')
                    pygame.quit()
                    exec("from gpt import *")
                    break
        screen.blit(background_image, background_rect)
        screen.blit(title_text, title_pos)
        pygame.draw.rect(screen, (0, 255, 0), button1_rect)
        screen.blit(button1_text, (button1_pos[0] + 10, button1_pos[1] + 10))
        pygame.draw.rect(screen, (0, 255, 0), button2_rect)
        screen.blit(button2_text, (button2_pos[0] + 10, button2_pos[1] + 10))
        pygame.display.update()

    pygame.quit()
main()
