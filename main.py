import pygame
import random
from Hexagon import Hexagon, Hexagons
from Button import Button

pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("HexSweep.py")

running = True
is_first_hexagon_clicked = False
game_paused = False

row = 7
col = 9
difficulty = 0.2
size = 35
font_size = int(size * 0.9) 
font = pygame.font.Font("Jersey15-Regular.ttf", font_size)

start_point = (size, size)
hexagons_grid = Hexagons(size, 'blue', False, start_point, row, col)

button_color = "gray"
button_text_color = "black"
button_font_size = 40
button_font = pygame.font.Font("Jersey15-Regular.ttf", button_font_size)

start_button = Button(screen, 50, 50, 'Start', button_font, button_font_size, (100, 50), button_color, button_text_color)
restart_button = Button(screen, 50, 50, 'Restart', button_font, button_font_size, (100, 100), button_color, button_text_color)
settings_button = Button(screen, 50, 50, 'Settings', button_font, button_font_size, (100, 150), button_color, button_text_color)
exit_button = Button(screen, 50, 50, 'Exit', button_font, button_font_size, (100, 200), button_color, button_text_color)

def draw_hexagon(Surface, hexagon, points):
    pygame.draw.polygon(
        Surface,
        hexagon.color,
        points,
    )
    pygame.draw.polygon(
        Surface,
        'black',
        points,
        width=3
    )
    text_surface = font.render(str(hexagon.value), True, "black")
    text_rect = text_surface.get_rect(center=hexagon.position)
    
    screen.blit(text_surface, text_rect)

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

def generate_mines(first_coord, hexagons):
    mines_remaining = int(row * col * difficulty)
    first_coord_row = first_coord[0]
    first_coord_col = first_coord[1]

    while True:
        x = random.randrange(0, row)
        y = random.randrange(0, col)
        targeted_coords = (x, y)
        targeted_hexagon = hexagons.get_hexagon_by_coords(targeted_coords)

        if x == first_coord_row and y == first_coord_col:
            continue

        if targeted_hexagon.get_is_mined() == False:
            targeted_hexagon.set_is_mined(True)
            mines_remaining -= 1

        if mines_remaining <= 0:
            break

def check_if_hex_is_mined(hexagon):
    if hexagon.get_is_mined():
        hexagon.set_color("red")
        hexagon.set_is_revealed(True)
        hexagon.set_value('X')
        end_game()
        return
    hexagon.set_color("gray")
    hexagon.set_is_revealed(True)
    hexagon.set_value('')

def flood_fill(coords, hexagons):
    x, y = coords
    targeted_hexagon = hexagons.get_hexagon_by_coords((x, y))
    
    if not targeted_hexagon or targeted_hexagon.get_is_revealed() or targeted_hexagon.get_is_flagged():
        return

    if targeted_hexagon.get_value() != '':
        return

    if targeted_hexagon.get_is_mined():
        end_game()
        return

    mine_count = count_adjacent_mines((x, y), hexagons)
    targeted_hexagon.set_is_revealed(True)

    if mine_count > 0:
        targeted_hexagon.set_value(str(mine_count))
        targeted_hexagon.set_color("green" if mine_count == 1 else "yellow" if mine_count == 2 else "purple")
        return  

    targeted_hexagon.set_value("")
    targeted_hexagon.set_color("gray")

    if x % 2 == 0:
        neighbors = [
            (x-1, y-1), (x-1, y),
            (x, y-1), (x, y+1),
            (x+1, y-1), (x+1, y),
        ]
    else:
        neighbors = [
            (x-1, y), (x-1, y+1),
            (x, y-1), (x, y+1),
            (x+1, y), (x+1, y+1),
        ]

    for nx, ny in neighbors:
        if hexagons.get_hexagon_by_coords((nx, ny)):
            flood_fill((nx, ny), hexagons)

        if hexagons.get_hexagon_by_coords((nx, ny)):
            flood_fill((nx, ny), hexagons)


def count_adjacent_mines(coords, hexagons):
    x, y = coords
    
    if x % 2 == 0:
        neighbors = [
            (x-1, y-1), (x-1, y),
            (x, y-1), (x, y+1),
            (x+1, y-1), (x+1, y),
        ]
    else:
        neighbors = [
            (x-1, y), (x-1, y+1),
            (x, y-1), (x, y+1),
            (x+1, y), (x+1, y+1),
        ]

    mine_count = 0
    for nx, ny in neighbors:
        hex_tile = hexagons.get_hexagon_by_coords((nx, ny))
        if hex_tile and hex_tile.get_is_mined():
            mine_count += 1

    return mine_count

def end_game():
    print("you lose! :(")
    for hexagon, _ in hexagons_grid.hexagons:
        if hexagon.get_is_mined():
            hexagon.set_is_revealed(True)
            hexagon.set_value("X")
            hexagon.set_color("red")
    pygame.display.update()

while running:
    screen.fill("white")



    if game_paused == True:
        if start_button.draw():
            pass
        if restart_button.draw():
            pass
        if settings_button.draw():
            pass
        if exit_button.draw():
            running = False
    else:
        for hexagon, points in hexagons_grid.hexagons:
            draw_hexagon(screen, hexagon, points)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_paused = not game_paused
        if event.type == pygame.MOUSEBUTTONDOWN and not game_paused:
            if event.button == 1:  
                mouse_pos = pygame.mouse.get_pos()

                for hexagon, points in hexagons_grid.hexagons:
                    if point_in_hexagon(mouse_pos, points):
                        
                        if not is_first_hexagon_clicked:
                            is_first_hexagon_clicked = True
                            coords = hexagon.get_coords()
                            generate_mines(coords, hexagons_grid)

                        coords = hexagon.get_coords()
                        flood_fill(coords, hexagons_grid)
            elif event.button == 3:
                mouse_pos = pygame.mouse.get_pos()

                for hexagon, points in hexagons_grid.hexagons:
                    if point_in_hexagon(mouse_pos, points):
                        if hexagon.get_is_flagged():
                            hexagon.set_color('blue')
                            hexagon.set_value('')
                        else:
                            hexagon.set_color('orange')
                            hexagon.set_value('?')
                        hexagon.toggle_is_flagged()


pygame.quit()