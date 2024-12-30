import pygame, pyscreenshot
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

win_bg = pygame.Window("bg", (500, 500), (100, 100))
win_main = pygame.Window("main", (100, 150), (300, 250))

# dance = pygame.image.load('./imgs/dance.png')

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
            if event.key == pygame.K_b:
                win_bg.get_surface().fill(BLACK)
                win_bg.flip()
                pyscreenshot.grab((100, 100, 600, 600)).save("./imgs/black.png")
            if event.key == pygame.K_w:
                win_bg.get_surface().fill(WHITE)
                win_bg.flip()
                pyscreenshot.grab((100, 100, 600, 600)).save("./imgs/white.png")
