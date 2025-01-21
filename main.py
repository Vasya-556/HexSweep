import pygame
from math import cos, sin, sqrt

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("HexSweep.py")

running = True

def draw_hexagon(Surface, color, size, position):
    PI = 3.14
    points = []

    i = 0
    for j in range(6):
        angle_deg = 60 * i
        angle_rad = PI / 180 * angle_deg
        x = position[0] + size * cos(angle_rad)
        y = position[1] + size * sin(angle_rad)
        points.append((x,y))
        i += 1
    
    pygame.draw.lines(
        Surface,
        color,
        True,
        points
    )

def draw_hexagon_grid(Surface, color, size, n, start_pos):
    height = sqrt(3) * size
    width = 2 * size
    horiz = 3/2 * size
    vert = sqrt(3) * size
    draw_hexagon(Surface, color, size, start_pos)


while running:

    screen.fill("white")

    # draw_hexagon(screen, "green", 50, (100,100), 60)
    draw_hexagon_grid(screen, "blue", 50, 5, (100,100))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()