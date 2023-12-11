import curses
from logic import get_active_matches
from colors import display_ascii_art
from ascii import matches_art
import curses

def display_matches(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    display_ascii_art(stdscr, matches_art, color_pair=6, vertical_offset=7)

    stdscr.addstr(h // 2, w // 2 - 10, "Ładowanie danych...", curses.A_BOLD)
    stdscr.refresh()

    stdscr.timeout(1000)

    try:
        matches = get_active_matches()
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(h // 2, w // 2 - len(str(e)) // 2, str(e), curses.A_BOLD)
        stdscr.refresh()
        stdscr.getch()
        return

    stdscr.timeout(-1)

    stdscr.clear()
    h, w = stdscr.getmaxyx()

    display_ascii_art(stdscr, matches_art, color_pair=6, vertical_offset=7)

    if not matches:
        stdscr.addstr(h // 2, w // 2 - 15, "Brak aktywnych meczów.", curses.A_BOLD)
    else:
        y = h // 2 - len(matches) // 2

        for match in matches:
            x = w // 2 - len(match) // 2
            stdscr.addstr(y, x, match)
            y += 1

    stdscr.addstr(h - 2, 4, "Naciśnij dowolny klawisz, aby powrócić do menu", curses.A_BOLD)
    stdscr.refresh()
    stdscr.getch()

