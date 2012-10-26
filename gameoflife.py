import curses
import time

# live with 0-1 neighbours: die
# live with 2-3 neighbours: live
# live with 4+ neighbours: die
# dead with 3 neighbours: live

DEBUG = False

width = 100
height = 100


def evolve(state):
    new_state = {}

    for y in range(height):
        for x in range(width):
            alive = state.get((y, x), False)
            neighbours = 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx = x + dx
                    ny = y + dy
                    if nx == x and ny == y:
                        continue

                    neighbour_state = state.get((ny, nx), False)
                    if neighbour_state:
                        neighbours += 1

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

            new_state[(y, x)] = new_cell_state

    if DEBUG:
        print '-----------------------'

    return new_state


def update_display(pad, state):
    for y in range(height):
        for x in range(width):
            try:
                cell_state = state.get((y, x), None)
                if cell_state:
                    char = 'X'
                else:
                    char = '-'

                pad.addch(y, x, char)
            except curses.error:
                pass

    pad.refresh(0, 0, 5, 5, 20, 75)


def main(stdscr=None):
    if stdscr:
        pad = curses.newpad(width, height)

    state = {}

    coords = [(1, 0), (2, 1), (2, 2), (1, 2), (0, 2)]
    for pos in coords:
        state[pos] = True

    while(True):
        if stdscr:
            update_display(pad, state)

        state = evolve(state)
        time.sleep(.01)

if not DEBUG:
    curses.wrapper(main)
else:
    main()
