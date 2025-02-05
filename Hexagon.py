from math import sqrt, sin, cos

class Hexagon:
    def __init__(self, size, color, is_flat_top, position, coords, value='', is_mined=False, is_flagged=False, is_revealed=False):
        self.size = size
        self.color = color
        self.is_flat_top = is_flat_top
        self.position = position
        self.coords = coords
        self.value = value
        self.is_mined = is_mined
        self.is_flagged = is_flagged
        self.is_revealed = is_revealed
        self.reserve = [color, value]

    def get_points(self):
        PI = 3.14
        points = []
        
        i = 0
        for j in range(6):
            if self.is_flat_top:
                angle_deg = 60 * i
            else:
                angle_deg = 60 * i - 30
            angle_rad = PI / 180 * angle_deg
            x = self.position[0] + self.size * cos(angle_rad)
            y = self.position[1] + self.size * sin(angle_rad)
            points.append((x,y))
            i += 1
        
        return points

    def toggle_is_flagged(self):
        self.is_flagged = not self.is_flagged

    def set_color(self, color='blue'):
        self.color = color
    
    def set_value(self, value=''):
        self.value = value

    def set_is_mined(self, is_mined):
        self.is_mined = is_mined

    def set_is_flagged(self, is_flagged):
        self.is_flagged = is_flagged

    def set_is_revealed(self, is_revealed):
        self.is_revealed = is_revealed

    def get_is_mined(self):
        return self.is_mined
    
    def get_coords(self):
        return self.coords
    
    def get_is_flagged(self):
        return self.is_flagged
    
    def get_is_revealed(self):
        return self.is_revealed
    
    def get_value(self):
        return self.value
    
    def set_reserve(self):
        self.reserve = [self.color, self.value]

    def get_reserve(self):
        return self.reserve

class Hexagons:
    def __init__(self, size, color, is_flat_top, start_pos, rows, columns):
        self.hexagons = []
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

        for row in range(rows):
            for col in range(columns):
                hexagon = Hexagon(size, color, is_flat_top, (pos_x, pos_y), (row, col))
                points = hexagon.get_points()
                self.hexagons.append((hexagon, points))

                pos_x += horiz * 2
            pos_y += vert
            pos_x = start_pos[0]
            if row % 2 == 0:
                pos_x += horiz

    def get_hexagon_by_coords(self, target_coords):
        for hexagon, _ in self.hexagons:
            if hexagon.get_coords() == target_coords:
                return hexagon
        return None