import curses
import textwrap
def setup_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_GREEN, curses.COLOR_BLACK)

def setup_bw_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

def addstr_colorized(win, y, x, s, color_pair):
    win.addstr(y, x, s, curses.color_pair(color_pair) | curses.A_BOLD)

def display_ascii_art(stdscr, art, color_pair, vertical_offset=0):
    setup_colors()

    wrapped_art = textwrap.dedent(art).strip()
    lines = wrapped_art.splitlines()
    max_length = max(len(line) for line in lines)

    h, w = stdscr.getmaxyx()
    y_start = h // 2 - len(lines) // 2 - vertical_offset

    for i, line in enumerate(lines):
        x = w // 2 - max_length // 2
        y = y_start + i

        stdscr.attron(curses.color_pair(color_pair))
        stdscr.addstr(y, x, line)
        stdscr.attroff(curses.color_pair(color_pair))
        
    setup_bw_colors()