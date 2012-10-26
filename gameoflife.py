import curses
import time

# live with 0-1 neighbours: die
# live with 2-3 neighbours: live
# live with 4+ neighbours: die
# dead with 3 neighbours: live

DEBUG = False

width = 100
height = 100


def all_cells():
    for y in range(height):
        for x in range(width):
            yield (y, x)


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
    for pos in all_cells():
        try:
            cell_state = is_alive(state, pos)
            if cell_state:
                char = 'X'
            else:
                char = '.'

            stdscr.addch(pos[0], pos[1], char)
        except curses.error:
            pass

    stdscr.refresh()


def update_debug_display(state):
    for y in range(height):
        line = ''
        for x in range(width):
            #line += str(num_neighbours(state, (y, x)))
            line += 'X' if is_alive(state, (y, x)) else '-'
        print line

    print '====================='


def main(stdscr=None):
    state = {}

    coords = [(1, 0), (2, 1), (2, 2), (1, 2), (0, 2)]  # glider
    #coords = [(0, 1), (1, 1), (2, 1)]  # traffic light
    for pos in coords:
        state[pos] = True

    while(True):
        if stdscr:
            update_display(stdscr, state)
        else:
            update_debug_display(state)

        state = evolve(state)
        time.sleep(0.1)

if not DEBUG:
    curses.wrapper(main)
else:
    main()
