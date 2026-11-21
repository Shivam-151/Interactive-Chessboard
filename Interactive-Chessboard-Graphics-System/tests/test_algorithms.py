import unittest
import numpy as np
from src.cg_algorithms import (scanline_polygon_fill, transform_points, dda_line,
    bresenham_line, midpoint_circle, cohen_sutherland_clip, board_to_screen, screen_to_board)

class TestGraphicsAlgorithms(unittest.TestCase):
    def test_scanline_square(self):
        pixels, steps = scanline_polygon_fill([(0,0),(3,0),(3,3),(0,3)])
        self.assertEqual(len(steps),3)
        self.assertEqual(len(pixels),12)
    def test_translation(self):
        out,_=transform_points([[1,2]],tx=3,ty=-1)
        np.testing.assert_allclose(out,[[4,1]])
    def test_rotation_90(self):
        out,_=transform_points([[1,0]],angle_deg=90)
        np.testing.assert_allclose(out,[[0,1]],atol=1e-9)
    def test_dda_and_bresenham_endpoints(self):
        self.assertEqual(dda_line(0,0,5,3)[-1],(5,3))
        self.assertEqual(bresenham_line(0,0,5,3)[-1],(5,3))
    def test_circle_symmetry(self):
        pts,_=midpoint_circle(0,0,5)
        self.assertIn((5,0),pts); self.assertIn((-5,0),pts)
    def test_clipping(self):
        self.assertEqual(cohen_sutherland_clip(-2,2,6,2,0,0,4,4),(0,2.0,4,2.0))
        self.assertIsNone(cohen_sutherland_clip(-2,-2,-1,-1,0,0,4,4))
    def test_coordinate_roundtrip(self):
        p=board_to_screen(4,3,(10,20),50)
        self.assertEqual(screen_to_board(*p,(10,20),50),(4,3))

if __name__=='__main__': unittest.main()
