import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = 1
my_font = pygame.font.Font('M_PLUS_Rounded_1c/MPLUSRounded1c-ExtraBold.ttf', 30)

text_surface = my_font.render('Привет, мир, text!', True, (255, 255, 255))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((102, 100, 105))
    screen.blit(text_surface, (0, 0))
    pygame.display.flip()
    clock.tick(120)

pygame.quit()
