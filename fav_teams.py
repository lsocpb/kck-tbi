import curses

def handle_favorite_teams(stdscr, user_id):
    selected_row_favorite_teams = 0

    while True:
        display_favorite_teams_menu(stdscr, selected_row_favorite_teams)
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
                display_current_squad(stdscr, user_id)
            elif selected_row_favorite_teams == 3:
                break

def display_favorite_teams_menu(stdscr, selected_row):
    curses.curs_set(0)
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    menu = ["Wybierz ulubioną drużynę", "Sprawdź ostatnie wyniki", "Sprawdź aktualny skład", "Powrót"]

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

def select_favorite_team(stdscr, user_id):
    # Logic for selecting a favorite team
    pass

def display_last_results(stdscr, user_id):
    # Logic for displaying last results of the favorite team
    pass

def display_current_squad(stdscr, user_id):
    # Logic for displaying the current squad of the favorite team
    pass
