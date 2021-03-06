import random


def check_move(new_x, new_y, board):
    """Validates move"""
    if board[new_y][new_x] == 0:
        return 0
    elif board[new_y][new_x] == 1:
        return -1
    else:
        return 1


def move(board, x, y, direct):
    """Moves traveller by one up,right,down or left"""
    new_x, new_y = x, y
    if direct == 'U':
        if check_move(x, y - 1, board) == 0:
            new_y = y - 1
            board[y][x], board[y - 1][x] = board[y - 1][x], board[y][x]
        elif check_move(x, y - 1, board) == -1:
            pass
    elif direct == 'D':
        if check_move(x, y + 1, board) == 0:
            new_y = y + 1
            board[y][x], board[y + 1][x] = board[y + 1][x], board[y][x]
        elif check_move(x, y + 1, board) == -1:
            pass
    elif direct == 'L':
        if check_move(x - 1, y, board) == 0:
            new_x = x - 1
            board[y][x], board[y][x - 1] = board[y][x - 1], board[y][x]
        elif check_move(x - 1, y, board) == -1:
            pass
    else:
        if check_move(x + 1, y, board) == 0:
            new_x = x + 1
            board[y][x], board[y][x + 1] = board[y][x + 1], board[y][x]
        elif check_move(x + 1, y, board) == -1:
            pass
    return board, new_x, new_y


def explore(board, x0, y0, path):
    """In this function agent is exploring the map - goes randomly everywhere one by one till meets wall.
    After meeting wall he stays and returns his path."""
    b = copy.deepcopy(board)
    x, y = x0, y0
    i = 0
    index = i
    while i >= 0:
        history = copy.deepcopy(b)
        b, x, y = move(b, x, y, path[i])
        if history == b:
            index = i
            i = -999
            break
        i += 1
    return path[:index], x, y, b


def remove_constant_points(li):
    """ IF we have situation that traveller went up and back like UP or RL we can clean it from path."""
    z = ''.join(li)
    while "UD" in z or "DU" in z or "LR" in z or "RL" in z:
        z = z.replace("UD", "")
        z = z.replace("DU", "")
        z = z.replace("LR", "")
        z = z.replace("RL", "")
    return list(z)


def choose_dir(z):
    """Choosing direction by given number"""
    if z == 0:
        return 'U'
    elif z == 1:
        return 'D'
    elif z == 2:
        return 'L'
    elif z == 3:
        return 'R'


def get_neighbours(x, y, board):
    """Return neighbours of place"""
    D = board[y + 1][x]
    U = board[y - 1][x]
    L = board[y][x - 1]
    R = board[y][x + 1]
    return [U, D, L, R]


def random_path(n, m):
    """Gets random path: size 2*(n+m-1), without repetitions"""
    dirs = ['U', 'D', 'L', 'R']
    size = n * m - 2 * (n + m - 1)
    rand_path = [random.choice(dirs) for x in range(size)]
    rand_path = remove_constant_points(rand_path)
    while len(rand_path) != size:
        part = [random.choice(dirs) for x in range(size - len(rand_path))]
        rand_path.extend(part)
        rand_path = remove_constant_points(rand_path)
    return rand_path


def check_way(board, x, y, path):
    """Checks if after path traveller is in exit and during the way he has not met a wall."""
    endX, endY = x, y
    for d in path:
        if d == 'U':
            endY -= 1
        elif d == 'D':
            endY += 1
        elif d == 'R':
            endX += 1
        else:
            endX -= 1
        if board[endY][endX] == 1:
            return False
        elif board[endY][endX] == 8:
            return True


def initial_solution(b, *arg):
    """Finds initial solution for simulated annealing (random,stay,radnom,stay ...)
    Traveller follows random path till he meets wall, than he stays and loss other path.
    Procedure is being followed until he finds exit."""
    board = copy.deepcopy(b)
    full_path = []
    n = len(board)
    m = len(board[0])
    b = copy.deepcopy(board)
    startX, startY = arg
    x, y = arg

    while 8 not in get_neighbours(x, y, b):
        sec, x, y, b = explore(b, x, y, random_path(n, m))
        full_path.extend(sec)
    full_path.append(choose_dir(get_neighbours(x, y, b).index(8)))
    full_path = remove_constant_points(full_path)
    check_way(board, startX, startY, full_path)
    return full_path
