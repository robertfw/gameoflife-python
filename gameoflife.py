import curses
import itertools
import time

PATTERNS = [
    #blinker
    [(0, 1), (1, 1), (2, 1)],

    #toad
    [(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2)],

    #beacon
    [(0,0), (0, 1), (1, 0), (2, 3), (3, 2), (3, 3)],

    #glider
    [(1, 0), (2, 1), (2, 2), (1, 2), (0, 2)],    
    
    #rpentomino
    [(1, 0), (2, 1), (1, 1), (0, 1), (0, 2)],

    #diehard
    [(0, 6), (1, 0), (1, 1), (2, 1), (2, 5), (2, 6), (2, 7)],

    #acorn
    [(0, 1), (1, 3), (2, 0), (2, 1), (2, 4), (2, 5), (2, 6)],
]

MAX_LOOPS = 10
MAX_ITERATIONS = 5206 + MAX_LOOPS  # acorn is the longest lived @5206 iterations
ALIVE_CHAR = 'O'

PREVIEW_PAUSE_SECONDS = 1.5
OUTRO_PAUSE_SECONDS = 1.5
ITERATION_PAUSE = 0.1

def get_neighbours(yx):
    return set(
        (yx[0] + dy, yx[1] + dx)
        for dx in range(-1, 2)
        for dy in range(-1, 2)
        if not (dx == 0 and dy == 0)
    )

def main(stdscr=None):
    stdscr.nodelay(True)
    max_y, max_x = stdscr.getmaxyx()
    quit_requested = False
    pattern_cycle = itertools.cycle(PATTERNS)

    while(not quit_requested):
        alive_cells = set(
            (max_y // 2 + y, max_x // 2 + x)
            for y, x in next(pattern_cycle)
        )

        iterations = 0
        loop_counter = 0

        # TODO!: loop detection only detects period=2 loops
        loop_detection_last_state = None
        
        while(alive_cells 
              and iterations < MAX_ITERATIONS 
              and loop_counter < MAX_LOOPS 
              and not quit_requested
        ):
            # check for user key press, if any found, quit
            if stdscr.getch() != curses.ERR:
                quit_requested = True

            if iterations % 2 == 0:
                loop_detection_this_state = ""
            else:
                loop_detection_this_state = None


            for y, x in itertools.product(range(max_y), range(max_x)):
                try:
                    char = ALIVE_CHAR if (y, x) in alive_cells else ' '
                    stdscr.addch(y, x, char)
                    
                    if loop_detection_this_state is not None:
                        loop_detection_this_state += char
                except curses.error:
                    pass

            if loop_detection_this_state:
                if loop_detection_this_state == loop_detection_last_state:
                    loop_counter += 1
                else:
                    loop_counter = 0

                loop_detection_last_state = loop_detection_this_state

            stdscr.refresh()

            next_alive_cells = set()

            for yx in alive_cells | set.union(*map(get_neighbours, alive_cells)):
                num_living_neighbours = len(alive_cells & get_neighbours(yx))

                if (
                    (yx in alive_cells and 2 <= num_living_neighbours <= 3) 
                    or 
                    (yx not in alive_cells and num_living_neighbours == 3)
                ):
                    next_alive_cells.add(yx)

            alive_cells = next_alive_cells
            
            if iterations == 0:
                # on the first iteration pause briefly to show the initial state
                time.sleep(PREVIEW_PAUSE_SECONDS)
            else:
                # otherwise a very small pause
                time.sleep(ITERATION_PAUSE)
            
            iterations += 1

        # if we're not quitting we're resetting after a loop was detected
        # pause briefly to show the final state
        if not quit_requested:
            time.sleep(OUTRO_PAUSE_SECONDS)

if __name__ == '__main__':
    curses.wrapper(main)
