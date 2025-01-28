from math import sqrt, sin, cos

class Hexagon:
    def __init__(self, size, color, is_flat_top, position, is_mined, coords, value=''):
        self.size = size
        self.color = color
        self.is_flat_top = is_flat_top
        self.position = position
        self.is_mined = is_mined
        self.coords = coords
        self.value = value

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

    def set_color(self, color='blue'):
        self.color = color
    
    def set_value(self, value=''):
        self.value = value

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
                hexagon = Hexagon(size, color, is_flat_top, (pos_x, pos_y), False, (row, col))
                points = hexagon.get_points()
                self.hexagons.append((hexagon, points))

                pos_x += horiz * 2
            pos_y += vert
            pos_x = start_pos[0]
            if row % 2 == 0:
                pos_x += horiz