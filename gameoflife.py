import curses
import time

# live with 0-1 neighbours: die
# live with 2-3 neighbours: live
# live with 4+ neighbours: die
# dead with 3 neighbours: live

DEBUG = False

width = 100
height = 100


def is_alive(state, pos):
    return state.get(pos, False)


def get_relative_neighbours():
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if not (dx == 0 and dy == 0):
                yield (dy, dx)


def get_neighbours(pos):
    '''Returns a generator that yields neighbour positions'''
    for nrel in get_relative_neighbours():
        yield (pos[0] + nrel[0], pos[1] + nrel[1])


def num_neighbours(state, pos):
    return sum(int(is_alive(state, npos)) for npos in get_neighbours(pos))


def outcome(alive, neighbours):
    if alive:
        if neighbours < 2 or neighbours > 3:
            new_cell_state = False
        else:
            new_cell_state = True
    else:
        if neighbours == 3:
            new_cell_state = True
        else:
            new_cell_state = False

    return new_cell_state


def evolve(state):
    new_state = {}

    cells_to_check = []
    for pos in [pos for pos in state if state[pos]]:
        if pos not in cells_to_check:
            cells_to_check.append(pos)

        for npos in get_neighbours(pos):
            if npos not in cells_to_check:
                cells_to_check.append(npos)

    for pos in cells_to_check:
        new_state[pos] = outcome(is_alive(state, pos), num_neighbours(state, pos))

    return new_state


def update_display(stdscr, state):
    dimensions = stdscr.getmaxyx()
    for y in range(dimensions[0]):
        for x in range(dimensions[1]):
            pos = (y, x)
            try:
                cell_state = is_alive(state, pos)
                if cell_state:
                    char = 'X'
                else:
                    char = ' '

                stdscr.addch(pos[0], pos[1], char)
            except curses.error:
                pass

    stdscr.refresh()


# def update_debug_display(state):
#     for y in range(height):
#         line = ''
#         for x in range(width):
#             line += 'X' if is_alive(state, (y, x)) else '-'
#         print line

#     print '====================='


def set_state(state, coords, start_pos=None):
    if start_pos is None:
        start_pos = (0, 0)

    for pos in coords:
        state[(start_pos[0] + pos[0], start_pos[1] + pos[1])] = True

    return state


def main(stdscr=None):
    state = {}

    #glider = [(1, 0), (2, 1), (2, 2), (1, 2), (0, 2)]
    #blinker = [(0, 1), (1, 1), (2, 1)]
    rpentomino = [(1, 0), (2, 1), (1, 1), (0, 1), (0, 2)]

    dimensions = stdscr.getmaxyx()
    midpoint = (dimensions[0] / 2, dimensions[1] / 2)

    state = set_state(state, rpentomino, midpoint)

    while(True):
        update_display(stdscr, state)
        state = evolve(state)
        time.sleep(0.1)

curses.wrapper(main)
