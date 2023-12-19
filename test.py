import pygame
import pygame.gfxdraw

display = pygame.display.set_mode([600, 600])
display.fill("white")
image = pygame.image.load("osaka.jpeg").convert_alpha()

image_copy = image.copy()
copy = display.copy()
blit_pos = pygame.Vector2(300, 300)
tick = 0
clock = pygame.Clock()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    tick += 1

    image2 = pygame.transform.rotate(image, tick % 360)

    display.fill("white")
    pygame.gfxdraw.bezier(
        display, [[0, 0], pygame.mouse.get_pos(), [600, 0]], 20, [0, 0, 0]
    )

    pygame.display.update()
