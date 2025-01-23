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
    return points

def draw_hexagon_grid(Surface, color, size, rows, columns, start_pos, is_flat_top=True):
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

    hexagons = []
    pos_x = start_pos[0]
    pos_y = start_pos[1]

    # for row in range(n):
    #     for col in range(n):
    #         points = draw_hexgon(Surface, color, size, (pos_x, pos_y), is_flat_top)
    #         hexagons.append(((row, col), (pos_x, pos_y), points))
    #         pos_x += horiz * 2
    #         pos_x -= horiz * 2
    #         pos_x += horiz
    #         pos_y += vert
    #         points = draw_hexgon(Surface, color, size, (pos_x, pos_y), is_flat_top)
    #         hexagons.append(((row, col), (pos_x, pos_y), points))
    #         pos_x += horiz
    #         pos_y -= vert
    #     pos_y += vert * 2
    #     pos_x = start_pos[0]
    
    for row in range(rows):
        for col in range(columns):
            points = draw_hexgon(Surface, color, size, (pos_x, pos_y), is_flat_top)
            hexagons.append(((row, col), (pos_x, pos_y), points))
            pos_x += horiz * 2
        pos_y += vert
        pos_x = start_pos[0]
        if row % 2 == 0:
            pos_x += horiz
        

    return hexagons

def point_in_hexagon(point, hexagon):
    x, y = point
    inside = False
    n = len(hexagon)
    p1x, p1y = hexagon[0]
    for i in range(n + 1):
        p2x, p2y = hexagon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

while running:

    screen.fill("white")

    # draw_hexagon(screen, "green", 50, (100,100), 60)
    hexagons = draw_hexagon_grid(screen, "blue", 50, 7, 3, (50,50),False)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                mouse_pos = pygame.mouse.get_pos()

                for coords, hex_pos, hex_points in hexagons:
                    if point_in_hexagon(mouse_pos, hex_points):
                        print("hex at", coords)
                        break