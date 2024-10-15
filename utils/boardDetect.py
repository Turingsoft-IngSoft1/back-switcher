import random

from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base

# Crea una lista de 9*4 colores
#color_list = ['y'] * 9 + ['b'] * 9 + ['g'] * 9 + ['r'] * 9

# Randomiza los colores
#random.shuffle(color_list)

# Crea una matrix de 6x6 random
#board = [color_list[i*6:(i+1)*6] for i in range(6)]
 
#board = \
#[['y', 'g', 'b', 'g', 'g', 'g'],
# ['y', 'r', 'b', 'b', 'g', 'g'],
# ['y', 'g', 'b', 'g', 'g', 'g'],
# ['b', 'r', 'y', 'r', 'r', 'r'],
# ['b', 'b', 'r', 'g', 'g', 'g'],
# ['b', 'b', 'y', 'r', 'g', 'r']]
# Print the board

#print("Board:")
#for row in board:
#    print(row)

# Direcciones, arriba, abajo y los costados

# board = lo que sea que se le pase por la base de datos

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_valid(x, y, color, visited):
    return 0 <= x < 6 and 0 <= y < 6 and not visited[x][y] and board[x][y] == color

def flood_fill(x, y, color, visited, group):
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if not visited[cx][cy]:
            visited[cx][cy] = True
            group.append((cx, cy))
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if is_valid(nx, ny, color, visited):
                    stack.append((nx, ny))

# Encuentra un grupo de colores iguales
visited = [[False for _ in range(6)] for _ in range(6)]
groups = []

for i in range(6):
    for j in range(6):
        if not visited[i][j]:
            group = []
            flood_fill(i, j, board[i][j], visited, group)
            if group:
                groups.append((board[i][j], group))

# Printea todos los grupos que encontro
print("\nGroups of the same color:")
for color, group in groups:
    print(f"Color {color}: {group}")

    def is_shapedif(group, shape):
        group_set = set(group)
        if shape == "fig01":
            default_shape = [(1, 0), (1, -1), (1, 1), (-1, 0)]  # Default T-shape
            if check_rotations(group_set, default_shape):
                return True
            return False
        elif shape == "fig05":
            # Check for horizontal line
            for x, y in group:
                if all((x, y + i) in group for i in range(5)):
                    return True
            # Check for vertical line
            for x, y in group:
                if all((x + i, y) in group for i in range(5)):
                    return True
            return False
        elif shape == 'fig02':
            default_shape = [(1, 0), (1, -1), (2, -1), (3, -1)]  # Default shape
            if check_rotations(group_set, default_shape):
                return True
            return False
        elif shape == 'fig03':
            default_shape = [(-1, 0), (-1, -1), (-2, -1), (-3, -1)]  # Default shape
            if check_rotations(group_set, default_shape):
                return True
            return False
        elif shape == 'fig04':
            default_shape = [(0, -1), (1, -1), (1, -2), (2, -2)]  # Default shape
            if check_rotations(group_set, default_shape):
                return True
            return False
        elif shape == 'fig06':
            default_shape = [(0, -1), (0, -2), (1, -2), (2, -2)]  # Default shape
            if check_rotations(group_set, default_shape):
                return True
            return False
        elif shape == 'fig07':
            default_shape = [(1, 0), (2, 0), (3, 0), (3, -1)]  # Default shape
            if check_rotations(group_set, default_shape):
                return True
            return False
        elif shape == 'fig08':
            default_shape = [(1, 0), (2, 0), (3, 0), (3, 1)]  # Default mirrored shape
            if check_rotations(group_set, default_shape):
                return True
            return False
        elif shape == 'fig09':
            default_shape = [(0, -1), (-1, -1), (-2, -1), (-1, -2)]  # Default shape
            if check_rotations(group_set, default_shape):
                return True
            return False
        elif shape == 'fig10':
            for x, y in group:
                if ((x, y - 1) in group and
                    (x - 1, y - 1) in group and
                    (x - 2, y - 1) in group and
                    (x - 2, y - 2) in group): # Default 
                    return True
                elif ((x + 1, y) in group and
                    (x + 1, y - 1) in group and
                    (x + 1, y - 2) in group and
                    (x + 2, y - 2) in group): # 90 degrees derecha
                    return True
            return False
        elif shape == 'fig11':
            default_shape = [(0, -1), (1, -1), (2, -1), (1, -2)]  # Default shape
            if check_rotations(group_set, default_shape):
                return True
            return False
        elif shape == 'fig12':
            default_shape = [(0, -1), (1, -1), (2, -1), (2, -2)]  # Default shape
            if check_rotations(group_set, default_shape):
                return True
            return False
        elif shape == 'fig13':
            default_shape = [(1, 0), (2, 0), (3, 0), (2, -1)]  # Default shape
            if check_rotations(group_set, default_shape):
                return True
            return False
        elif shape == 'fig14':
            default_shape = [(1, 0), (2, 0), (3, 0), (2, 1)]  # Default mirrored shape
            if check_rotations(group_set, default_shape):
                return True
            return False
        elif shape == 'fig15':
            default_shape = [(1, 0), (2, 0), (1, 1), (2, 1)]  # Default shape
            if check_rotations(group_set, default_shape):
                return True
            return False
        elif shape == 'fig16':
            default_shape = [(0, -1), (1, -1), (2, -1), (2, 0)]  # Default shape
            if check_rotations(group_set, default_shape):
                return True
            return False
        elif shape == 'fig17':
            for x, y in group:
                if ((x, y - 1) in group and
                    (x + 1, y - 1) in group and
                    (x - 1, y - 1) in group and
                    (x, y - 2) in group): # Default 
                    return True
                return False
        elif shape == 'fig18':
            default_shape = [(1, 0), (2, 0), (1, -1), (2, -1)]  # Default shape
            if check_rotations(group_set, default_shape):
                return True
            return False
        else:
            return False

    def is_shapeeasy(group, shape):
            group_set = set(group)
            if shape == 'fige01':
                for x, y in group:
                    if ((x + 1, y) in group and
                        (x + 1, y + 1) in group and
                        (x + 2, y + 1) in group): # Default 
                        return True
                    elif ((x, y - 1) in group and
                        (x + 1, y - 1) in group and
                        (x + 1, y - 2) in group): # 90 degrees derecha
                        return True
                    return False
            elif shape == 'fige02':
                for x, y in group:
                    if ((x + 1, y) in group and
                        (x + 1, y - 1) in group and
                        (x, y - 1) in group): # Default 
                        return True
                    return False
            elif shape == 'fige03':
                for x, y in group:
                    if ((x + 1, y) in group and
                        (x + 1, y - 1) in group and
                        (x + 2, y - 1) in group): # Default 
                        return True
                    elif ((x, y - 1) in group and
                        (x - 1, y - 1) in group and
                        (x - 1, y - 2) in group): # 90 degrees derecha
                        return True
                    return False
                return False
            elif shape == 'fige04':
                default_shape = [(1, 0), (1, -1), (1, 1)]  # Default T-shape
                if check_rotations(group_set, default_shape):
                    return True
                return False
            elif shape == 'fige05':
                default_shape = [(1, 0), (2, 0), (2, -1)]  # Default shape
                if check_rotations(group_set, default_shape):
                    return True
                return False
            elif shape == 'fige06':
                default_shape = [(0, 1), (0, 2), (0, 3)]  # Horizontal line
                if check_rotations(group_set, default_shape):
                    return True
                return False
            elif shape == 'fige07':
                default_shape = [(0, -1), (-2, -1), (-2, -1)]
                if check_rotations(group_set, default_shape):
                    return True
                return False
            else:
                return False

def check_rotations(group_set, default_shape):
    rotations = generate_rotations(default_shape)      
    for x, y in group_set:
        for rotation in rotations:
            if all((x + dx, y + dy) in group_set for dx, dy in rotation):
                return True
    return False
            
def generate_rotations(shape):
    """Generate all 90-degree rotations of the given shape."""
    rotations = [shape]
    for _ in range(3):
        new_shape = [(y, -x) for x, y in rotations[-1]]
        rotations.append(new_shape)
    return rotations

# Checkea figuras particulares
shapes_to_check = [
    "fig01", "fig05", "fig02", "fig03", "fig04", "fig06", "fig07", "fig08", "fig09", "fig10", 
    "fig11", "fig12", "fig13", "fig14", "fig15", "fig16", "fig17", "fig18", "fige01", "fige02", 
    "fige03", "fige04", "fige05", "fige06", "fige07"
]
for color, group in groups:
    for shape in shapes_to_check:
        if (len(group) == 4 and is_shapeeasy(group, shape)):
            print(f"Color {color} forms a {shape} with positions: {group}")
            break
        elif (len(group) == 5 and is_shapedif(group, shape)):
            print(f"Color {color} forms a {shape} with positions: {group}")
            break