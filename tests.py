import unittest
import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from math import sqrt, sin, cos
from Hexagon import Hexagon, Hexagons
from Button import Button  

class TestHexagon(unittest.TestCase):
    def setUp(self):
        self.hexagon = Hexagon(size=10, color='red', is_flat_top=True, position=(0, 0), coords=(0, 0))

    def test_get_points_flat_top(self):
        points = self.hexagon.get_points()
        self.assertEqual(len(points), 6, "There should be 6 points for a hexagon")
        self.assertIsInstance(points, list)
        self.assertIsInstance(points[0], tuple)

    def test_toggle_is_flagged(self):
        self.assertFalse(self.hexagon.get_is_flagged(), "Initially, is_flagged should be False")
        self.hexagon.toggle_is_flagged()
        self.assertTrue(self.hexagon.get_is_flagged(), "After toggling, is_flagged should be True")
        self.hexagon.toggle_is_flagged()
        self.assertFalse(self.hexagon.get_is_flagged(), "After toggling again, is_flagged should be False")

    def test_set_color(self):
        self.hexagon.set_color('blue')
        self.assertEqual(self.hexagon.color, 'blue', "The color should be updated to 'blue'")

    def test_set_value(self):
        self.hexagon.set_value('mine')
        self.assertEqual(self.hexagon.get_value(), 'mine', "The value should be updated to 'mine'")

    def test_set_is_mined(self):
        self.hexagon.set_is_mined(True)
        self.assertTrue(self.hexagon.get_is_mined(), "The hexagon should be mined")

    def test_get_reserve(self):
        self.hexagon.set_color('green')
        self.hexagon.set_value('empty')
        self.hexagon.set_reserve()
        reserve = self.hexagon.get_reserve()
        self.assertEqual(reserve, ['green', 'empty'], "The reserve should contain the correct color and value")


class TestHexagons(unittest.TestCase):
    def setUp(self):
        self.hexagons_grid = Hexagons(size=10, color='blue', is_flat_top=True, start_pos=(0, 0), rows=3, columns=3)

    def test_hexagons_creation(self):
        self.assertEqual(len(self.hexagons_grid.hexagons), 9, "There should be 9 hexagons in the grid (3x3)")
        for hexagon, points in self.hexagons_grid.hexagons:
            self.assertEqual(len(points), 6, "Each hexagon should have 6 points")
            self.assertIsInstance(points, list)
            self.assertIsInstance(points[0], tuple)

    def test_get_hexagon_by_coords(self):
        hexagon = self.hexagons_grid.get_hexagon_by_coords((1, 1))
        self.assertIsNotNone(hexagon, "Hexagon should be found by coords (1, 1)")
        self.assertEqual(hexagon.get_coords(), (1, 1), "The hexagon's coordinates should match (1, 1)")

        hexagon = self.hexagons_grid.get_hexagon_by_coords((10, 10))
        self.assertIsNone(hexagon, "No hexagon should be found for coords (10, 10)")

    def test_offset_positions(self):
        hexagon1, _ = self.hexagons_grid.hexagons[0]
        hexagon2, _ = self.hexagons_grid.hexagons[1]
        self.assertNotEqual(hexagon1.position, hexagon2.position, "The positions of adjacent hexagons should be different")

    def test_grid_creation_with_non_flat_top(self):
        hexagons_grid = Hexagons(size=10, color='green', is_flat_top=False, start_pos=(0, 0), rows=3, columns=3)
        self.assertEqual(len(hexagons_grid.hexagons), 9, "There should be 9 hexagons in the grid (3x3) for pointy-top")
        for hexagon, points in hexagons_grid.hexagons:
            self.assertEqual(len(points), 6, "Each hexagon should have 6 points")

    def test_get_hexagon_by_invalid_coords(self):
        hexagon = self.hexagons_grid.get_hexagon_by_coords((-1, -1))
        self.assertIsNone(hexagon, "There should be no hexagon for invalid coordinates")


class TestButton(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.button = Button(self.screen, 200, 50, text='Click Me', pos=(300, 275))

    def tearDown(self):
        pygame.quit()

    def test_draw_button_default(self):
        pygame.mouse.set_pos(0, 0)
        
        self.button.draw()
        
        self.assertEqual(self.button.color, (196, 196, 194))  

    def test_draw_button_reset_after_click(self):
        mouse_pos = (350, 300)  
        pygame.mouse.set_pos(mouse_pos)

        pygame.event.post(pygame.event.Event(MOUSEBUTTONDOWN, pos=mouse_pos, button=1))
        pygame.event.pump()  
        
        self.button.draw()
        
        pygame.event.post(pygame.event.Event(MOUSEBUTTONUP, pos=mouse_pos, button=1))
        pygame.event.pump()  
        
        clicked_after_release = self.button.draw()
        self.assertFalse(clicked_after_release)  

    def test_set_text(self):
        self.button.set_text('New Text')
        self.assertEqual(self.button.text, 'New Text')

if __name__ == '__main__':
    unittest.main()