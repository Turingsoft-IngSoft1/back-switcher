import unittest
from boardDetect import is_shapedif, is_shapeeasy, detect_figures

class TestBoardDetect(unittest.TestCase):
    def print_shape(self, group):
        max_x = max(x for x, y in group)
        max_y = max(y for x, y in group)
        grid = [[' ' for _ in range(max_y + 1)] for _ in range(max_x + 1)]
        for x, y in group:
            grid[x][y] = '#'
        for row in grid:
            print(''.join(row))

    def test_tetrisT_shape(self):
        print("tetrisT")
        group = [(4, 4), (3, 4), (3, 5), (3, 3), (5, 4)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig01")) # Derecha
        
        group = [(4, 4), (5, 4), (5, 5), (5, 3), (3, 4)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig01")) # izquierda

        group = [(4, 4), (4, 3), (3, 3), (5, 3), (4, 5)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig01")) # Arriba

        group = [(4, 4), (4, 5), (3, 5), (5, 5), (4, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig01")) # Abajo

    def test_line_shape(self):
        print("line")
        group = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig05"))

        group = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig05"))
    
    def test_snake1_shape(self):
        print("snake1")
        group = [(4, 4), (5, 4), (5, 3), (6, 3), (7, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig02")) # default
        group = [(4, 4), (4, 3), (3, 3), (3, 2), (3, 1)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig02")) # 90
        
        group = [(4, 4), (3, 4), (3, 5), (2, 5), (1, 5)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig02")) # 180 degrees
        
        group = [(4, 4), (4, 5), (5, 5), (5, 6), (5, 7)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig02")) # 270 degrees
   
    def test_snake2_shape(self):
        print("snake2")
        group = [(4, 4), (3, 4), (3, 3), (2, 3), (1, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig03")) # default
        
        group = [(4, 4), (4, 5), (3, 5), (3, 6), (3, 7)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig03")) # 90
        
        group = [(4, 4), (5, 4), (5, 5), (6, 5), (7, 5)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig03")) # 180 degrees
        
        group = [(4, 4), (4, 3), (5, 3), (5, 2), (5, 1)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig03")) # 270 degrees
    
    def test_abanico_shape(self):
        print("abanico")
        group = [(4, 4), (4, 3), (5, 3), (5, 2), (6, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig04")) # default
        
        group = [(4, 4), (3, 4), (3, 3), (2, 3), (2, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig04")) # 90
        
        group = [(4, 4), (5, 4), (5, 3), (6, 3), (6, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig04")) # 180 degrees
        
        group = [(4, 4), (4, 3), (3, 3), (3, 2), (2, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig04")) # 270 degrees
    
    def test_corner_shape(self):
        print("corner")
        group = [(4, 4), (4, 3), (4, 2), (5, 2), (6, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig06")) # default
        
        group = [(4, 4), (3, 4), (2, 4), (2, 3), (2, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig06")) # 90
        
        group = [(4, 4), (5, 4), (6, 4), (6, 3), (6, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig06")) # 180 degrees
        
        group = [(4, 4), (5, 4), (6, 4), (6, 5), (6, 6)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig06")) # 270 degrees
    
    def test_ele1_shape(self):
        print("ele1")
        group = [(4, 4), (4, 5), (3, 5), (2, 5), (1, 5)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig07")) # default
        
        group = [(4, 4), (5, 4), (5, 5), (5, 6), (5, 7)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig07")) # 90
        
        group = [(4, 4), (4, 3), (5, 3), (6, 3), (7, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig07")) # 180 degrees
        
        group = [(4, 4), (3, 4), (3, 3), (3, 2), (3, 1)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig07")) # 270 degrees
    
    def test_ele2_shape(self):
        print("ele2")
        group = [(4, 4), (5, 4), (6, 4), (7, 4), (7, 5)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig08")) # default
        
        group = [(4, 4), (4, 3), (4, 2), (4, 1), (5, 1)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig08")) # 90
        
        group = [(4, 4), (4, 5), (5, 5), (6, 5), (7, 5)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig08")) # 180 degrees
        
        group = [(4, 4), (5, 4), (5, 3), (5, 2), (5, 1)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig08")) # 270 degrees
    
    def test_fig09_shape(self):
        print("fig09")
        group = [(4, 4), (4, 3), (3, 3), (2, 3), (3, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig09")) # default
        
        group = [(4, 4), (4, 3), (4, 2), (3, 3), (5, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig09")) # 90
        
        group = [(4, 4), (4, 3), (5, 3), (3, 3), (3, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig09")) # 180 degrees
        
        group = [(4, 4), (5, 4), (5, 3), (6, 3), (5, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig09")) # 270 degrees
    
    def test_zigzag_shape(self):
        print("zigzag")
        group = [(4, 4), (4, 3), (3, 3), (2, 3), (2, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig10")) # default
        
        group = [(4, 4), (5, 4), (5, 3), (5, 2), (6, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig10")) # 90
    
    def test_fig09mirror_shape(self):
        print("fig09mirror")
        group = [(4, 4), (4, 3), (5, 3), (6, 3), (5, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig11")) # default
        
        group = [(4, 4), (3, 4), (3, 3), (3, 2), (2, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig11")) # 90

        group = [(4, 4), (4, 3), (5, 3), (3, 3), (5, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig11")) # 180

        group = [(4, 4), (4, 3), (4, 2), (5, 3), (3, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig11")) # 270
    
    def test_zigzagmirror_shape(self):
        print("zigzagmirror")
        group = [(4, 4), (4, 3), (5, 3), (6, 3), (6, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig12")) # default
        
        group = [(4, 4), (3, 4), (3, 3), (3, 2), (2, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig12")) # 90

    def test_baton_shape(self):
        print("baton")
        group = [(4, 4), (5, 4), (6, 4), (7, 4), (6, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig13")) # default
        
        group = [(4, 4), (4, 3), (4, 2), (4, 1), (3, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig13")) # 90

        group = [(4, 4), (5, 4), (6, 4), (7, 4), (5, 5)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig13")) # 180

        group = [(4, 4), (4, 3), (4, 2), (4, 1), (5, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig13")) # 270

    def test_batonmirrored_shape(self):
        print("batonmirrored")
        group = [(4, 4), (5, 4), (6, 4), (7, 4), (6, 5)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig14")) # default
        
        group = [(4, 4), (4, 3), (4, 2), (4, 1), (5, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig14")) # 90

        group = [(4, 4), (5, 4), (6, 4), (7, 4), (5, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig14")) # 180

        group = [(4, 4), (4, 3), (4, 2), (4, 1), (3, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig14")) # 270

    def test_cubewithtail_shape(self):
        print("cubewithtail")
        group = [(4, 4), (5, 4), (6, 4), (5, 5), (6, 5)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig15")) # default
        
        group = [(4, 4), (4, 3), (4, 2), (5, 3), (5, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig15")) # 90

        group = [(4, 4), (3, 4), (2, 4), (3, 3), (2, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig15")) # 180

        group = [(4, 4), (4, 5), (4, 6), (3, 5), (3, 6)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig15")) # 270
    
    def test_cubeta_shape(self):
        print("cubeta")
        group = [(4, 4), (4, 3), (5, 3), (6, 3), (6, 4)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig16")) # default
        
        group = [(4, 4), (3, 4), (3, 3), (3, 2), (4, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig16")) # 90

        group = [(4, 4), (4, 5), (5, 5), (6, 5), (6, 4)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig16")) # 180

        group = [(4, 4), (5, 4), (5, 3), (5, 2), (4, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig16")) # 270
    
    def test_dpad_shape(self):
        print("dpad")
        group = [(4, 4), (4, 3), (4, 2), (3, 3), (5, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig17")) # default

    def test_cubewithtailmirrored_shape(self):
        print("cubewithtailmirrored")
        group = [(4, 4), (5, 4), (6, 4), (5, 3), (6, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig18")) # default
        
        group = [(4, 4), (4, 3), (4, 2), (3, 3), (3, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig18")) # 90

        group = [(4, 4), (3, 4), (2, 4), (3, 5), (2, 5)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig18")) # 180

        group = [(4, 4), (4, 5), (4, 6), (5, 5), (5, 6)]
        self.print_shape(group)
        self.assertTrue(is_shapedif(group, "fig18")) # 270

    def test_smallzigzag_shape(self):
        print("smallzigzag")
        group = [(4, 4), (5, 4), (5, 5), (6, 5)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige01")) # default
        
        group = [(4, 4), (4, 3), (5, 3), (5, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige01")) # 90
    
    def test_cube_shape(self):
        print("cube")
        group = [(4, 4), (5, 4), (4, 3), (5, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige02")) # default
    
    def test_smallzigzagmirrored_shape(self):
        print("smallzigzagmirrored")
        group = [(4, 4), (5, 4), (5, 3), (6, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige03")) # default
        
        group = [(4, 4), (4, 3), (3, 3), (3, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige03")) # 90

    def test_smalltetrisT_shape(self):
        print("smalltetrisT")
        group = [(4, 4), (3, 4), (3, 5), (3, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige04")) # Derecha
        
        group = [(4, 4), (5, 4), (5, 5), (5, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige04")) # izquierda

        group = [(4, 4), (4, 3), (3, 3), (5, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige04")) # Arriba

        group = [(4, 4), (4, 5), (3, 5), (5, 5)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige04")) # Abajo
    
    def test_smallele_shape(self):
        print("smallele")
        group = [(4, 4), (5, 4), (6, 4), (6, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige05")) # default
        
        group = [(4, 4), (4, 3), (4, 2), (3, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige05")) # 90

        group = [(4, 4), (4, 3), (5, 3), (6, 3)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige05")) # 180

        group = [(4, 4), (3, 4), (3, 3), (3, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige05")) # 270
    def test_smalline_shape(self):
        print("smalline")
        group = [(4, 4), (5, 4), (6, 4), (7, 4)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige06")) # horizontal
        
        group = [(4, 4), (4, 5), (4, 6), (4, 7)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige06")) # vertical
    def test_smallelemirrored_shape(self):
        print("smallelemirrored")
        group = [(4, 4), (5, 4), (6, 4), (6, 5)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige07")) # default
        
        group = [(4, 4), (4, 3), (4, 2), (5, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige07")) # 90

        group = [(4, 4), (4, 5), (5, 5), (6, 5)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige07")) # 180

        group = [(4, 4), (5, 4), (5, 3), (5, 2)]
        self.print_shape(group)
        self.assertTrue(is_shapeeasy(group, "fige07")) # 270

    def test_detect_figures(self):
        board = [["Y", "G", "R", "Y", "R", "G"], 
             ["R", "B", "G", "B", "Y", "B"], 
             ["R", "Y", "B", "B", "G", "B"], 
             ["R", "G", "B", "B", "G", "B"], 
             ["R", "G", "G", "G", "Y", "B"], 
             ["G", "R", "R", "Y", "Y", "B"]]
        shapes = ["fig05","fige06"]
        result = detect_figures(board, shapes)
        print('result:', result)
        expected_result = [('R', 'fige06', [(1, 0), (2, 0), (3, 0), (4, 0)]), ('B', 'fig05', [(1, 5), (2, 5), (3, 5), (4, 5), (5, 5)])]
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()