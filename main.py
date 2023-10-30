import sys
import curses
from football_leagues import get_top_european_leagues
import matches
from news import get_selected_news
from quiz import select_quiz
def display_menu(stdscr, selected_row):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    menu = ["Informacje o ligach", "Mecze", "Aktualności", "Ciekawostki", "Quizy piłkarskie", "Ulubione drużyny", "Wyjście"]

    for i, option in enumerate(menu):
        x = w // 2 - len(option) // 2
        y = h // 2 - len(menu) // 2 + i
        if i == selected_row:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, option)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, option)

    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    selected_row = 0

    while True:
        display_menu(stdscr, selected_row)
        key = stdscr.getch()
        if key == curses.KEY_DOWN and selected_row < 6:
            selected_row += 1
        elif key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == 10:  # Enter key
            if selected_row == 6:
                sys.exit(0)
            elif selected_row == 0:
                get_top_european_leagues(stdscr)
            elif selected_row == 1:
                active_matches = matches.get_active_matches()
                matches.display_matches(stdscr, active_matches)
            elif selected_row == 2:
                get_selected_news(stdscr)
            elif selected_row == 3:
                print("Ciekawostki")
            elif selected_row == 4:
                select_quiz(stdscr)
            elif selected_row == 5:
                print("Ulubione drużyny")

if __name__ == '__main__':
    curses.wrapper(main)
