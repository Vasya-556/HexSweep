import pygame
from math import cos, sin, sqrt

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("HexSweep.py")

running = True

def draw_hexgon(Surface, color, size, position, is_flat_top):
    PI = 3.14
    points = []

    i = 0
    for j in range(6):
        if is_flat_top:
            angle_deg = 60 * i
        else:
            angle_deg = 60 * i - 30
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

def draw_hexagon_grid(Surface, color, size, n, start_pos, is_flat_top=True):
    height = sqrt(3) * size
    width = 2 * size
    if is_flat_top:    
        horiz = 3/2 * size
        vert = sqrt(3) * size
        vert = vert/2
    else:
        horiz = sqrt(3) * size
        horiz = horiz/2
        vert = 3/2 * size

    pos_x = start_pos[0]
    pos_y = start_pos[1]

    for i in range(n):
        for j in range(n):
            draw_hexgon(Surface, color, size, (pos_x, pos_y), is_flat_top)
            pos_x += horiz * 2
            pos_x -= horiz * 2
            pos_x += horiz
            pos_y += vert
            draw_hexgon(Surface, color, size, (pos_x, pos_y), is_flat_top)
            pos_x += horiz
            pos_y -= vert
        pos_y += vert * 2
        pos_x = start_pos[0]

while running:

    screen.fill("white")

    # draw_hexagon(screen, "green", 50, (100,100), 60)
    draw_hexagon_grid(screen, "blue", 50, 3, (100,100),False)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()