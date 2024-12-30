import pygame, pyscreenshot
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FUCHSIA = (255, 0, 128)

win_bg = pygame.Window("bg", (500, 500), (100, 100))
win_main = pygame.Window("main", (100, 150), (300, 250))

font = pygame.font.Font("./font/font.ttf", 90)

while True:
    win_bg.get_surface().fill(BLACK)
    win_bg.flip()
    win_main.get_surface().fill(BLACK)
    win_main.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("quit")
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if pygame.K_0 <= event.key <= pygame.K_9:
                num = event.key - pygame.K_0
                win_main.get_surface().fill(BLACK)
                text = font.render(str(num), True, WHITE)
                win_main.get_surface().blit(text, (text.get_rect().center[0], text.get_rect().center[1] - 50))
                win_main.flip()
                pyscreenshot.grab((299, 219, 401, 401)).save(f"./imgs/num/{num}.png")
            if event.key == pygame.K_a:
                win_main.get_surface().fill(BLACK)
                text = font.render(":", True, WHITE)
                win_main.get_surface().blit(text, (text.get_rect().center[0], text.get_rect().center[1] - 50))
                win_main.flip()
                pyscreenshot.grab((299, 219, 401, 401)).save(f"./imgs/num/colon.png")
