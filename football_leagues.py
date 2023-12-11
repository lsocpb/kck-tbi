import curses
from logic import get_selected_league_info, top_european_leagues_info
from ascii import pl_art, seriea_art, bundesliga_art, laliga_art, french_art, leagues_art
from colors import display_ascii_art
    
def display_league_menu(stdscr, selected_row):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    display_ascii_art(stdscr, leagues_art, color_pair = 2 ,vertical_offset=7)
    for index, league_info in enumerate(top_european_leagues_info, start=1):
        x = w // 2 - len(league_info['Nazwa ligi']) // 2
        y = h // 2 - len(top_european_leagues_info) // 2 + index - 1
        if index - 1 == selected_row:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, league_info['Nazwa ligi'])
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, league_info['Nazwa ligi'])
    stdscr.addstr(h - 2, 4, "Naciśnij 'Escape', aby powrócić do menu", curses.A_BOLD)
    stdscr.refresh()

def display_league_info(stdscr, league_info):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    y = h // 2 - len(league_info) // 2
    x = w // 2 - max(len(key) for key in league_info) // 2

    for key, value in league_info.items():
        if key == 'Nazwa ligi' and value == 'English Premier League':
            display_ascii_art(stdscr, pl_art, color_pair = 4 ,vertical_offset=7)
        elif key == 'Nazwa ligi' and value == 'Serie A':
            display_ascii_art(stdscr, seriea_art, color_pair = 4 ,vertical_offset=7)
        elif key == 'Nazwa ligi' and value == 'Bundesliga':
            display_ascii_art(stdscr, bundesliga_art, color_pair = 4 ,vertical_offset=7)
        elif key == 'Nazwa ligi' and value == 'La Liga':
            display_ascii_art(stdscr, laliga_art, color_pair = 4 ,vertical_offset=7)
        elif key == 'Nazwa ligi' and value == 'Ligue 1':
            display_ascii_art(stdscr, french_art, color_pair = 4 ,vertical_offset=7)
        elif key == 'Nazwa ligi' and value == 'La Liga':
            display_ascii_art(stdscr, laliga_art, color_pair = 4 ,vertical_offset=7)
        stdscr.addstr(y, x, f"{key}: {value}")
        y += 1
    

    stdscr.addstr(h - 2, 4, "Naciśnij dowolny klawisz, aby wrócic do wyboru lig", curses.A_BOLD)
    stdscr.refresh()
    stdscr.getch()

def run_ui(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    selected_row = 0

    while True:
        display_league_menu(stdscr, selected_row)
        key = stdscr.getch()

        if key == curses.KEY_DOWN and selected_row < len(top_european_leagues_info) - 1:
            selected_row += 1
        elif key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == 10:
            selected_league_info = get_selected_league_info(selected_row, top_european_leagues_info)
            if selected_league_info:
                display_league_info(stdscr, selected_league_info)
                stdscr.getch()
        elif key == 27:
            break
