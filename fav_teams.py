import curses
import sqlite3

current_favorite_team = ""

def handle_favorite_teams(stdscr, user_id):
    global current_favorite_team
    selected_row_favorite_teams = 0

    def update_screen():
        global current_favorite_team
        current_favorite_team = get_current_favorite_team(user_id)

    update_screen()

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
                display_current_squad(stdscr, user_id)
            elif selected_row_favorite_teams == 3:
                break

def display_favorite_teams_menu(stdscr, selected_row, current_favorite_team, callback=None):
    curses.curs_set(0)
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(h // 2 - 4, w // 2 - len("TWOJA ULUBIONA DRUŻYNA: {}".format(current_favorite_team)) // 2,
                  "TWOJA ULUBIONA DRUŻYNA: {}".format(current_favorite_team))
    stdscr.attroff(curses.color_pair(1))

    menu = ["Wybierz ulubioną drużynę", "Sprawdź ostatnie wyniki", "Sprawdź aktualny skład", "Powrót"]

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
        callback()  # Wywołujemy funkcję zwrotną do aktualizacji ekranu


def select_favorite_team(stdscr, user_id):
    curses.curs_set(0)
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    available_teams = ["FC BARCELONA", "REAL MADRYT", "BAYERN MONACHIUM", "MANCHESTER UNITED", "MANCHESTER CITY", "CHELSEA FC", "BORUSSIA DORTMUND", 
                       "AC MILAN", "INTER MEDIOLAN", "JUVENTUS TURYN", "PARIS SAINT-GERMAIN", "LIVERPOOL FC", "ARSENAL FC", "TOTTENHAM HOTSPUR", "ATLETICO MADRYT", "WIECZYSTA KRAKOW"]

    selected_row_team = 0
    while True:
        for i, team in enumerate(available_teams):
            x = w // 2 - len(team) // 2
            y = h // 2 - len(available_teams) // 2 + i
            if i == selected_row_team:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, team)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, team)

        key = stdscr.getch()

        if key == curses.KEY_DOWN and selected_row_team < len(available_teams) - 1:
            selected_row_team += 1
        elif key == curses.KEY_UP and selected_row_team > 0:
            selected_row_team -= 1
        elif key == 10:
            save_favorite_team(user_id, available_teams[selected_row_team])
            break

    stdscr.refresh()

def save_favorite_team(user_id, selected_team):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE users SET favorite_team = ? WHERE id = ?", (selected_team, user_id))
        conn.commit()
    except sqlite3.Error as e:
        print("Błąd podczas zapisywania ulubionej drużyny:", e)
    finally:
        conn.close()

def get_current_favorite_team(user_id):
    global current_favorite_team

    # Sprawdź, czy wartość current_favorite_team została już ustawiona
    if not current_favorite_team:
        # Connect to the database
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:
            # Fetch the current favorite team for the user from the database
            cursor.execute("SELECT favorite_team FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            if result:
                current_favorite_team = result[0]
            else:
                current_favorite_team = "Brak ulubionej drużyny"  # Lub inny komunikat dla braku ulubionej drużyny
        except sqlite3.Error as e:
            current_favorite_team = "Błąd pobierania ulubionej drużyny"
        finally:
            # Close the database connection
            conn.close()

    return current_favorite_team


def display_last_results(stdscr, user_id):
    # Logic for displaying last results of the favorite team
    pass

def display_current_squad(stdscr, user_id):
    # Logic for displaying the current squad of the favorite team
    pass
