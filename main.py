import pygame
from math import cos, sin, sqrt
import random

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("HexSweep.py")

running = True
is_first_hexagon_clicked = False
row = 5
col = 6
checked_hex = [[0 for _ in range(col)] for _ in range(row)]
colors = [['blue' for _ in range(col)] for _ in range(row)]
hex_values = [['' for _ in range(col)] for _ in range(row)]

def draw_hexagon(Surface, color, size, position, hex_value, is_flat_top,):
    PI = 3.14
    points = []

    font = pygame.font.Font("Jersey15-Regular.ttf", 45)
    text_surface = font.render(str(hex_value), True, "black")
    text_rect = text_surface.get_rect(center=position)
    
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
    
    # pygame.draw.lines(
    #     Surface,
    #     color,
    #     True,
    #     points
    # )
    pygame.draw.polygon(
        Surface,
        color,
        points,
    )
    pygame.draw.polygon(
        Surface,
        'black',
        points,
        width=4
    )
    screen.blit(text_surface, text_rect)

    return points

def draw_hexagon_grid(Surface, colors, size, rows, columns, start_pos,hex_values, is_flat_top=True):
    # height = sqrt(3) * size
    # width = 2 * size
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

    for row in range(rows):
        for col in range(columns):
            color = colors[row][col]
            hex_value = hex_values[row][col]
            points = draw_hexagon(Surface, color, size, (pos_x, pos_y), hex_value, is_flat_top)
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

def generate_mines(row, col, first_coord):
    all_hexagons = row * col
    all_hexagons_fraction = int(all_hexagons * 0.2)
    first_coord_row = first_coord[0]
    first_coord_col = first_coord[1]
    matrix = [[0] * col for _ in range(row)]
    mines_remaining = all_hexagons_fraction

    while True:
        x = random.randrange(0, row)
        y = random.randrange(0, col)
        if x == first_coord_row and y == first_coord_col:
            continue
        if matrix[x][y] != 1:
            matrix[x][y] = 1
            mines_remaining -= 1
        if mines_remaining <= 0:
            break
    
    return matrix

def check_hex(x, y, mines, row, col, checked_hex):
    if mines[x][y] == 1:
        end_game()
    else:
        total = 0
        output = check_neighbors(x, y, mines, row, col, checked_hex, total)
        print(output)
        return

def check_neighbors(x, y, mines, row, col, checked_hex, total):
    if x >= row or y >= col or x < 0 or y < 0:
        return 0
    if checked_hex[x][y] == 1:
        return 0
    checked_hex[x][y] = 1
    total += check_neighbors(x, y-1, mines, row, col, checked_hex, total)
    total += check_neighbors(x+1, y-1, mines, row, col, checked_hex, total)
    total += check_neighbors(x-1, y, mines, row, col, checked_hex, total)
    total += check_neighbors(x+1, y, mines, row, col, checked_hex, total)
    total += check_neighbors(x-1, y+1, mines, row, col, checked_hex, total)
    total += check_neighbors(x, y+1, mines, row, col, checked_hex, total)
    if mines[x][y] == 1:
        return total + 1
    return total

def flood_fill(x, y, mines):
    if x < 0 and x > row and y < 0 and y > col:
        return
    if mines[x][y]:
        print(1)

def end_game():
    print("you lose! :(")

while running:

    screen.fill("white")
    
    hexagons = draw_hexagon_grid(screen, colors, 50, row, col, (50,50), hex_values, False)

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
                        x, y = coords[0], coords[1]
                        colors[x][y] = 'green'
                        hex_values[x][y] = '1'
                        if not is_first_hexagon_clicked:
                            mines = generate_mines(row, col, coords)
                            is_first_hexagon_clicked = True
                        else:
                            pass
                            # flood_fill(coords[0], coords[1], mines)
                            # check_hex(coords[0], coords[1], mines, row, col, checked_hex)
                            # print(mines)
                        break