import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import time
import sys
from math import ceil
from Hexagon import Hexagon, Hexagons
from Button import Button

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 416
SCREEN_HEIGHT = 392
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("HexSweep")

if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

pygame_icon_path = os.path.join(base_path, 'assets', 'hexagon.png')

pygame_icon = pygame.image.load(pygame_icon_path)
pygame.display.set_icon(pygame_icon)

running = True
is_first_hexagon_clicked = False
game_paused = True
game_finished = False
is_hexagons_top_flat = False

row = 6
col = 6
difficulty = 0.2
size = 35
font_size = int(size * 0.9) 
font_path = os.path.join(base_path, 'assets', 'Jersey15-Regular.ttf')
font = pygame.font.Font(font_path, font_size)

start_point = (size + size * 0.2, 2 * size + size * 0.5)
hexagons_grid = Hexagons(size, 'blue', is_hexagons_top_flat, start_point, row, col)

button_color = "gray"
button_text_color = "black"
button_font_size = int(size + size * 0.1)
button_font = pygame.font.Font(font_path, button_font_size)
button_width = int(button_font_size * 3.5)
button_height = button_font_size

play_button = Button(screen, button_width, button_height, 'Play', button_font, button_font_size, (SCREEN_WIDTH - SCREEN_WIDTH * 0.5 - button_width * 0.5, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.8), button_color, button_text_color)
restart_button = Button(screen, button_width, button_height, 'Restart', button_font, button_font_size, (SCREEN_WIDTH - SCREEN_WIDTH * 0.5 - button_width * 0.5, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.8 + button_height + button_height * 0.1), button_color, button_text_color)
settings_button = Button(screen, button_width, button_height, 'Settings', button_font, button_font_size, (SCREEN_WIDTH - SCREEN_WIDTH * 0.5 - button_width * 0.5, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.8 + 2 * (button_height + button_height * 0.1)), button_color, button_text_color)
exit_button = Button(screen, button_width, button_height, 'Exit', button_font, button_font_size, (SCREEN_WIDTH - SCREEN_WIDTH * 0.5 - button_width * 0.5, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.8 + 3 * (button_height + button_height * 0.1)), button_color, button_text_color)

total_mines = 0
total_mines_label = int(row * col * difficulty)

stopwatch_running = False
start_time = 0
elapsed_time = 0

restart_button_in_game = Button(screen, button_width, button_height, 'Restart', button_font, button_font_size, (SCREEN_WIDTH - SCREEN_WIDTH * 0.5 - button_width * 0.5, SCREEN_HEIGHT - SCREEN_HEIGHT), button_color, button_text_color)

bg_music_path = os.path.join(base_path, 'assets', 'Background_music.mp3')
pygame.mixer.music.load(bg_music_path)
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

winning_sound_path = os.path.join(base_path, 'assets', 'Winning_sound.mp3')
loosing_sound_path = os.path.join(base_path, 'assets', 'Loose_sound.mp3')
winning_sound = pygame.mixer.Sound(winning_sound_path)
loosing_sound = pygame.mixer.Sound(loosing_sound_path)

def set_game_parameters(new_row, new_col, new_difficulty, new_top=None):
    global row, col, difficulty, size, font_size, font, start_point, hexagons_grid, button_color, button_text_color, button_font_size
    global button_font, button_width, button_height, SCREEN_WIDTH, SCREEN_HEIGHT, play_button, restart_button, settings_button, exit_button 
    global total_mines, total_mines_label, stopwatch_running, start_time, elapsed_time, is_hexagons_top_flat, restart_button_in_game, font_path
    
    row = new_row
    col = new_col
    size = 35
    if is_hexagons_top_flat:
        SCREEN_WIDTH = 3/2 * size * row + size
        SCREEN_HEIGHT = 1.73205080757 * size * col + 2.9 * size
    else:
        SCREEN_WIDTH = 1.73205080757 * size * row + 1.5 * size
        SCREEN_HEIGHT = 3/2 * size * col + 2.2 * size
    difficulty = new_difficulty
    font_size = int(size * 0.9) 
    font = pygame.font.Font(font_path, font_size)
    total_mines = 0
    total_mines_label = int(row * col * difficulty)

    if new_top != None:
        is_hexagons_top_flat = new_top
        
    start_point = start_point = (size + size * 0.2, 2 * size + size * 0.5)
    hexagons_grid = Hexagons(size, 'blue', is_hexagons_top_flat, start_point, row, col)

    button_color = "gray"
    button_text_color = "black"
    button_font_size = int(size + size * 0.1)
    button_font = pygame.font.Font(font_path, font_size)
    button_width = int(button_font_size * 3.5)
    button_height = button_font_size

    play_button = Button(screen, button_width, button_height, 'Play', button_font, button_font_size, (SCREEN_WIDTH - SCREEN_WIDTH * 0.5 - button_width * 0.5, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.8), button_color, button_text_color)
    restart_button = Button(screen, button_width, button_height, 'Restart', button_font, button_font_size, (SCREEN_WIDTH - SCREEN_WIDTH * 0.5 - button_width * 0.5, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.8 + button_height + button_height * 0.1), button_color, button_text_color)
    settings_button = Button(screen, button_width, button_height, 'Settings', button_font, button_font_size, (SCREEN_WIDTH - SCREEN_WIDTH * 0.5 - button_width * 0.5, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.8 + 2 * (button_height + button_height * 0.1)), button_color, button_text_color)
    exit_button = Button(screen, button_width, button_height, 'Exit', button_font, button_font_size, (SCREEN_WIDTH - SCREEN_WIDTH * 0.5 - button_width * 0.5, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.8 + 3 * (button_height + button_height * 0.1)), button_color, button_text_color)
    
    stopwatch_running = False
    start_time = 0
    elapsed_time = 0

    restart_button_in_game = Button(screen, button_width, button_height, 'Restart', button_font, button_font_size, (SCREEN_WIDTH - SCREEN_WIDTH * 0.5 - button_width * 0.5, SCREEN_HEIGHT - SCREEN_HEIGHT), button_color, button_text_color)

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
    global total_mines
    total_mines = int(row * col * difficulty)

    first_coord_row, first_coord_col = first_coord

    all_coords = [(x, y) for x in range(row) for y in range(col) if (x, y) != (first_coord_row, first_coord_col)]

    mine_coords = set(random.sample(all_coords, total_mines))

    for x, y in mine_coords:
        hexagons.get_hexagon_by_coords((x, y)).set_is_mined(True)

def flood_fill(coords, hexagons):
    global is_hexagons_top_flat
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
        targeted_hexagon.set_color(
            "green" if mine_count == 1 
            else "yellow" if mine_count == 2 
            else "purple" if mine_count == 3 
            else "pink" if mine_count == 4 
            else "brown" if mine_count == 5 
            else "cyan" )
        return  

    targeted_hexagon.set_value("")
    targeted_hexagon.set_color("gray")
    
    if is_hexagons_top_flat:
        if y % 2 == 0:
            neighbors = [
                (x-1, y-1), (x, y-1),
                (x-1, y+1), (x, y+1),
                (x-1, y), (x+1, y)
            ]
        else:
            neighbors = [
                (x, y-1), (x+1, y-1),
                (x, y+1), (x+1, y+1),
                (x-1, y), (x+1, y)
            ]
    else:
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
    global is_hexagons_top_flat
    x, y = coords
    
    if is_hexagons_top_flat:
        if y % 2 == 0:
            neighbors = [
                (x-1, y-1), (x, y-1),
                (x-1, y+1), (x, y+1),
                (x-1, y), (x+1, y)
            ]
        else:
            neighbors = [
                (x, y-1), (x+1, y-1),
                (x, y+1), (x+1, y+1),
                (x-1, y), (x+1, y)
            ]
    else:
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

def check_remaining_hex(hexagons):
    global row, col, total_mines, stopwatch_running, game_finished, restart_button_in_game
    revealed_hex = 0
    total_hex = row * col
    for i in range(row):
        for j in range(col):
            targeted_hexagon = hexagons.get_hexagon_by_coords((i, j))
            if targeted_hexagon.get_is_revealed():
                revealed_hex += 1
    if revealed_hex + total_mines == total_hex:
        winning_sound.play()
        restart_button_in_game.set_text("You won!")
        game_finished = True
        stopwatch_running = False

def end_game():
    global game_finished, stopwatch_running, restart_button_in_game
    game_finished = True
    stopwatch_running = False
    loosing_sound.play()
    restart_button_in_game.set_text("You lose!")
    for hexagon, _ in hexagons_grid.hexagons:
        if hexagon.get_is_mined():
            hexagon.set_is_revealed(True)
            hexagon.set_value("X")
            hexagon.set_color("red")
    pygame.display.update()

def play_game():
    global game_paused, stopwatch_running, start_time
    game_paused = False
    if game_finished:
        return
    if not stopwatch_running:  
        start_time = time.time() - elapsed_time  
        stopwatch_running = True

def restart_game():
    global game_paused, is_first_hexagon_clicked, hexagons_grid, game_finished, total_mines_label, stopwatch_running, start_time, elapsed_time, is_hexagons_top_flat

    is_first_hexagon_clicked = False
    game_paused = False
    game_finished = False
    hexagons_grid = Hexagons(size, 'blue', is_hexagons_top_flat, start_point, row, col)
    total_mines_label = int(row * col * difficulty)
    
    stopwatch_running = True
    start_time = time.time()
    elapsed_time = 0

def change_settings():
    global is_first_hexagon_clicked, hexagons_grid, SCREEN_WIDTH, SCREEN_HEIGHT, screen, font, button_width
    global button_height, game_finished, button_font, button_font_size, button_text_color, button_color, is_hexagons_top_flat
    settings_running = True

    back_button = Button(screen, button_width, button_height, 'Back', button_font, button_font_size, (SCREEN_WIDTH - SCREEN_WIDTH * 0.5 - 50, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.1-25), "red", button_text_color)
    difficulty_text = font.render("Diffuculty:", True, "black")

    difficulty_beginner = Button(screen, button_width, button_height, 'beginner', button_font, button_font_size, (SCREEN_WIDTH - SCREEN_WIDTH * 0.9, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.8), button_color, button_text_color)
    difficulty_normal = Button(screen, button_width, button_height, 'normal', button_font, button_font_size, (SCREEN_WIDTH - SCREEN_WIDTH * 0.9, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.6), button_color, button_text_color)
    difficulty_expert = Button(screen, button_width, button_height, 'expert', button_font, button_font_size, (SCREEN_WIDTH - SCREEN_WIDTH * 0.9, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.4), button_color, button_text_color)

    sound = pygame.mixer.music.get_volume()
    sound = ceil(sound * 100) / 100 
    sound_text = font.render("Sound:", True, "black")
    sound_plus = Button(screen, button_width/3, button_height, '+', button_font, button_font_size, (SCREEN_WIDTH - SCREEN_WIDTH * 0.25, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.75), button_color, button_text_color)
    sound_minus = Button(screen, button_width/3, button_height, '-', button_font, button_font_size, (SCREEN_WIDTH - SCREEN_WIDTH * 0.4, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.75), button_color, button_text_color)
    
    difficulty_text_pos = (SCREEN_WIDTH - SCREEN_WIDTH * 0.9, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.9)
    sound_text_pos = (SCREEN_WIDTH - SCREEN_WIDTH * 0.4, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.9)
    sound_percent_pos = (SCREEN_WIDTH - SCREEN_WIDTH * 0.4, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.83)
    sound_font = font

    hexagon_top_text = font.render("Top:", True, "black")
    hexagon_top_text_pos = (SCREEN_WIDTH - SCREEN_WIDTH * 0.4, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.6)
    hexagons_top = Button(screen, button_width, button_height, 'Flat', button_font, button_font_size, (SCREEN_WIDTH - SCREEN_WIDTH * 0.4, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.5), button_color, button_text_color)
    if is_hexagons_top_flat:
        hexagons_top.set_text("Flat")
    else:
        hexagons_top.set_text("Pointy")

    while settings_running:
        screen.fill("white")
        
        if back_button.draw():
            is_first_hexagon_clicked = False
            game_finished = False
            hexagons_grid = Hexagons(size, 'blue', is_hexagons_top_flat, start_point, row, col)
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            settings_running = False
        
        sound_percent = sound_font.render(f"{int(sound*100)}%", True, "black")
        screen.blit(difficulty_text, difficulty_text_pos)
        screen.blit(sound_text, sound_text_pos)
        screen.blit(sound_percent, sound_percent_pos)
        screen.blit(hexagon_top_text, hexagon_top_text_pos)

        if difficulty_beginner.draw():
            set_game_parameters(6, 6, 0.2)
        if difficulty_normal.draw():
            set_game_parameters(8, 8, 0.3)
        if difficulty_expert.draw():
            set_game_parameters(10, 10, 0.4)

        if sound_plus.draw():
            sound = min(1, round(sound + 0.05, 2)) 
            pygame.mixer.music.set_volume(sound)
        if sound_minus.draw():
            sound = max(0, round(sound - 0.05, 2))
            pygame.mixer.music.set_volume(sound)

        if hexagons_top.draw():
            is_hexagons_top_flat = not is_hexagons_top_flat
            if is_hexagons_top_flat:
                hexagons_top.set_text("Flat")
            else:
                hexagons_top.set_text("Pointy")
            set_game_parameters(row, col, difficulty, is_hexagons_top_flat)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def start_stopwatch():
    global stopwatch_running, start_time
    if not stopwatch_running:  
        start_time = time.time() - elapsed_time  
        stopwatch_running = True

def stop_stopwatch():
    global stopwatch_running, elapsed_time
    if stopwatch_running:
        elapsed_time = time.time() - start_time  
        stopwatch_running = False

def main():
    global running, game_paused, total_mines_label, stopwatch_running, start_time, is_first_hexagon_clicked
    while running:
        screen.fill("white")
        if game_paused == True:
            if play_button.draw():
                play_game()
            if restart_button.draw():
                restart_game()
            if settings_button.draw():
                change_settings()
            if exit_button.draw():
                running = False
        else:
            for hexagon, points in hexagons_grid.hexagons:
                draw_hexagon(screen, hexagon, points)
            total_mines_font = font.render(f"{total_mines_label}", True, "black")
            screen.blit(total_mines_font, (SCREEN_WIDTH - SCREEN_WIDTH * 0.9, size * 0.1))

            if stopwatch_running:
                elapsed_time = time.time() - start_time
            time_display = font.render(f"{elapsed_time:.1f}", True, "black")
            screen.blit(time_display, (SCREEN_WIDTH - SCREEN_WIDTH * 0.2, size * 0.1))    
            if restart_button_in_game.draw():
                restart_game()
                restart_button_in_game.set_text('Restart')

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused
                    if not game_finished:
                        if stopwatch_running:
                            elapsed_time = time.time() - start_time  
                            stopwatch_running = False
                        else:
                            start_time = time.time() - elapsed_time  
                            stopwatch_running = True
            
            elif event.type == pygame.MOUSEBUTTONDOWN and not (game_paused or game_finished):
                mouse_pos = pygame.mouse.get_pos()

                clicked_hex = next(
                    (hexagon for hexagon, points in hexagons_grid.hexagons if point_in_hexagon(mouse_pos, points)),
                    None
                )

                if clicked_hex:  
                    if event.button == 1:  
                        if not is_first_hexagon_clicked:
                            is_first_hexagon_clicked = True
                            generate_mines(clicked_hex.get_coords(), hexagons_grid)
                        flood_fill(clicked_hex.get_coords(), hexagons_grid)

                    elif event.button == 3:  
                        if clicked_hex.get_is_flagged():
                            reserv = clicked_hex.get_reserve()
                            clicked_hex.set_color(reserv[0])
                            clicked_hex.set_value(reserv[1])
                            total_mines_label += 1
                        else:
                            clicked_hex.set_reserve()
                            clicked_hex.set_color('orange')
                            clicked_hex.set_value('?')
                            total_mines_label -= 1
                        clicked_hex.toggle_is_flagged()

                    check_remaining_hex(hexagons_grid)

if __name__ == "__main__":
    main()
pygame.quit()