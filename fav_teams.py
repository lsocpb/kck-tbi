import curses
from colors import addstr_colorized, setup_colors, setup_bw_colors, display_ascii_art
from logic import save_favorite_team, get_current_favorite_team, get_last_results
from ascii import fav_teams_art, results_art

def handle_favorite_teams(stdscr, user_id, current_favorite_team):
    curses.curs_set(0)
    selected_row_favorite_teams = 0

    def update_screen():
        nonlocal current_favorite_team
        current_favorite_team = get_current_favorite_team(user_id)

    while True:
        display_favorite_teams_menu(stdscr, selected_row_favorite_teams, current_favorite_team, update_screen)
        key = stdscr.getch()
        if key == curses.KEY_DOWN and selected_row_favorite_teams < 3:
            selected_row_favorite_teams += 1
        elif key == curses.KEY_UP and selected_row_favorite_teams > 0:
            selected_row_favorite_teams -= 1
        elif key == 10:
            if selected_row_favorite_teams == 0:
                select_favorite_team(stdscr, user_id)
            elif selected_row_favorite_teams == 1:
                display_last_results(stdscr, user_id)
            elif selected_row_favorite_teams == 2:
                break

def display_favorite_teams_menu(stdscr, selected_row, current_favorite_team, callback=None):
    curses.curs_set(0)
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(h // 2 - 4, w // 2 - len("TWOJA ULUBIONA DRUŻYNA: {}".format(current_favorite_team)) // 2,
                  "TWOJA ULUBIONA DRUŻYNA: {}".format(current_favorite_team))
    stdscr.attroff(curses.color_pair(1))

    menu = ["Wybierz ulubioną drużynę", "Sprawdź ostatnie wyniki", "Powrót"]


    display_ascii_art(stdscr, fav_teams_art, color_pair = 7 ,vertical_offset=9)
    for i, option in enumerate(menu):
        x = w // 2 - len(option) // 2
        y = h // 2 - len(menu) // 2 + i + 1
        if i == selected_row:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, option)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, option)

    stdscr.refresh()

    if callback is not None:
        callback() 


def select_favorite_team(stdscr, user_id):
    curses.curs_set(0)
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    available_teams = ["FC BARCELONA", "REAL MADRYT", "BAYERN MONACHIUM", "MANCHESTER UNITED", "MANCHESTER CITY", "CHELSEA FC", "BORUSSIA DORTMUND", 
                       "AC MILAN", "INTER MEDIOLAN", "JUVENTUS TURYN", "PARIS SAINT-GERMAIN", "LIVERPOOL FC", "ARSENAL FC", "TOTTENHAM HOTSPUR", "ATLETICO MADRYT", "WIECZYSTA KRAKOW"]

    selected_row_team = 0
    rows_per_page = 5
    page = 0

    while True:
        start_row = page * rows_per_page
        end_row = start_row + rows_per_page
        stdscr.clear()

        for i, team in enumerate(available_teams[start_row:end_row]):
            x = w // 2 - len(team) // 2
            y = h // 2 - len(available_teams) // 2 + i
            if i == selected_row_team:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, team)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, team)

        stdscr.addstr(h - 2, 4, "Naciśnij 'Escape', aby powrócić do menu", curses.A_BOLD)
        stdscr.addstr(h - 1, w - 20, f"Strona: {page + 1}")
        stdscr.addstr(h - 1, 4, "Naciśnij <- lub -> aby przewijać strony", curses.A_BOLD)
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_DOWN and selected_row_team < len(available_teams) - 1:
            selected_row_team += 1
        elif key == curses.KEY_UP and selected_row_team > 0:
            selected_row_team -= 1
        elif key == 10:
            save_favorite_team(user_id, available_teams[selected_row_team])
            break
        elif key == 27:
            return None
        elif key == curses.KEY_RIGHT and end_row < len(available_teams):
            page += 1
            selected_row_team = 0
        elif key == curses.KEY_LEFT and page > 0:
            page -= 1
            selected_row_team = 0

    stdscr.refresh()

def display_last_results(stdscr, user_id):
    curses.curs_set(0)
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    results_data = get_last_results(user_id)
    display_ascii_art(stdscr, results_art, color_pair = 5, vertical_offset=9)
    
    if isinstance(results_data, str):
        stdscr.addstr(h // 2, w // 2 - len(results_data) // 2, results_data)
    else:
        setup_colors()
        team_name = results_data["team_name"]
        stdscr.addstr(h // 2 - 5, w // 2 - len(f"Ostatnie wyniki dla {team_name}:") // 2, f"Ostatnie wyniki dla {team_name}:")
        for i, result in enumerate(results_data["results"], start=1):
            outcome_color = curses.COLOR_GREEN if result["color"] == "RED" else curses.COLOR_RED
            if result["color"] == "YELLOW":
                outcome_color = curses.COLOR_YELLOW
            addstr_colorized(stdscr, h // 2 - 3 + i, w // 2 - len(result["opponent"]) // 2 - 7, f"{result['opponent']}: {result['score']} ({result['outcome']})", outcome_color)

    stdscr.refresh()
    stdscr.getch()
    setup_bw_colors()

