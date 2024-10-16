# Direcciones, arriba, abajo y los costados

# board = lo que sea que se le pase por la base de datos
def is_shapedif(group, shape):
    group_set = set(group)
    if shape == "fig01":
        default_shape = [(1, 0), (1, -1), (1, 1), (-1, 0)]  # Default T-shape
        if check_rotations(group_set, default_shape):
            return True
        return False
    elif shape == "fig05":
        default_shape = [(0, 1), (0, 2), (0, 3), (0,4)]  # Horizontal line
        if check_rotations(group_set, default_shape):
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
        default_shape = [(0, -1), (-1, -1), (-2, -1), (-2, -2)]  # Default Cubito
        if check_rotations(group_set, default_shape):
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
        default_shape = [(0, -1), (1, -1), (-1, -1), (0, -2)]  # Default Cubito
        if check_rotations(group_set, default_shape):
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
        default_shape = [(1, 0), (1, 1), (2, 1)]  
        if check_rotations(group_set, default_shape):
            return True
        return False
    elif shape == 'fige02':
        default_shape = [(1, 0), (1, -1), (0, -1)]  
        if check_rotations(group_set, default_shape):
            return True
        return False
    elif shape == 'fige03':
        default_shape = [(1, 0), (1, -1), (2, -1)]  
        if check_rotations(group_set, default_shape):
            return True
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
    """Genera las rotaciones a 90 grados"""
    rotations = [shape]
    for _ in range(3):
        new_shape = [(y, -x) for x, y in rotations[-1]]
        rotations.append(new_shape)
    return rotations

def detect_figures(board, shapes):
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


    # Checkea figuras particulares
    shapes_to_check = shapes
    figures = []
    for color, group in groups:
        for shape in shapes_to_check:
            if (len(group) == 4 and is_shapeeasy(group, shape)):
                figures.append((color, shape, group))
                break
            elif (len(group) == 5 and is_shapedif(group, shape)):
                figures.append((color, shape, group))
                break
    return figures
# Usar la funcion detect_figures para detectar las figuras en el tablero, retorna todas las figuras encontradas, no usar el main
