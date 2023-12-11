import sys
import curses
import matches
from football_leagues import run_ui
from news import news_run_ui
from quiz import select_quiz
from fav_teams import handle_favorite_teams, get_current_favorite_team
from logic import login, register, init_database
from colors import display_ascii_art
from ascii import app_art

def display_menu(stdscr, menu_options, selected_row):
    curses.curs_set(0)
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    display_ascii_art(stdscr, app_art, color_pair = 7 ,vertical_offset=7)

    for i, option in enumerate(menu_options):
        x = w // 2 - len(option) // 2
        y = h // 2 - len(menu_options) // 2 + i
        if i == selected_row:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, option)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, option)

    stdscr.refresh()

def register_interface(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    display_ascii_art(stdscr, app_art, color_pair = 7 ,vertical_offset=7)
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h // 2 - 1, w // 2 - 10, "Rejestracja", curses.A_BOLD)
    stdscr.addstr(h // 2, w // 2 - 13, "Podaj nazwę użytkownika:", curses.A_BOLD)
    stdscr.addstr(h - 2, 4, "Naciśnij Escape, aby powrócić do menu", curses.A_BOLD)
    stdscr.refresh()
    username = ""
    curses.curs_set(1)
    

    while True:
        key = stdscr.getch()
        if key == 10:
            break
        elif key == 27:
            return None, None
        elif key == curses.KEY_BACKSPACE or key == 127:
            username = username[:-1]
            stdscr.addstr(h // 2 + 1, w // 2 - 10 + len(username), ' ')
        else:
            username += chr(key)
            stdscr.addstr(h // 2 + 1, w // 2 - 10, username)
        stdscr.refresh()

    stdscr.addstr(h // 2 + 2, w // 2 - 10, "Podaj hasło:", curses.A_BOLD)
    stdscr.refresh()

    password = ""
    while True:
        key = stdscr.getch()
        if key == 10:
            break
        elif key == curses.KEY_BACKSPACE or key == 127:
            password = password[:-1]
            stdscr.addstr(h // 2 + 3, w // 2 - 10 + len(password), ' ')
        else:
            password += chr(key)
            stdscr.addstr(h // 2 + 3, w // 2 - 10, "*" * len(password))
        stdscr.refresh()
    
    if not password:
        display_error_message(stdscr, "Hasło nie może być puste!")
    else:
        display_error_message(stdscr, "Zarejestrowano pomyślnie!")

    return username, password


def login_interface(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    display_ascii_art(stdscr, app_art, color_pair = 7 ,vertical_offset=7)
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h // 2 - 1, w // 2 - 7, "Logowanie", curses.A_BOLD)
    stdscr.addstr(h // 2, w // 2 - 10, "Podaj nazwę użytkownika:", curses.A_BOLD)
    stdscr.addstr(h - 2, 4, "Naciśnij Escape, aby powrócić do menu", curses.A_BOLD)
    stdscr.refresh()
    username = ""
    password = ""
    active_field = "username"
    curses.curs_set(1)

    while True:
        key = stdscr.getch()
        if key == 10:
            if active_field == "username":
                active_field = "password"
                stdscr.addstr(h // 2 + 2, w // 2 - 10, "Podaj hasło:", curses.A_BOLD)
                stdscr.refresh()
                continue
            else:
                break
        elif key == 27:
            return None, None
        elif key == curses.KEY_BACKSPACE or key == 127:
            if active_field == "username":
                username = username[:-1]
                stdscr.addstr(h // 2 + 1, w // 2 - 10 + len(username), ' ')
            elif active_field == "password":
                password = password[:-1]
                stdscr.addstr(h // 2 + 3, w // 2 - 10 + len(password), ' ') 
        elif key == 9:
            active_field = "username"
            curses.curs_set(1)         
        else:
            if active_field == "username":
                username += chr(key)
                stdscr.addstr(h // 2 + 1, w // 2 - 10, username)
            elif active_field == "password":
                password += chr(key)
                stdscr.addstr(h // 2 + 3, w // 2 - 10, "*" * len(password))
        stdscr.refresh()
    curses.curs_set(0)

    return username, password

def main(stdscr):
    init_database()
    user_id = None
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    selected_row = 0
    selected_row_login = 0
    menu_options_login = ["Zaloguj się", "Zarejestruj się", "Wyjście"]
    menu_options_main = ["Informacje o ligach", "Mecze", "Aktualności", "Quizy piłkarskie", "Ulubione drużyny", "Wyjście"]

    while True:
        display_menu(stdscr, menu_options_login, selected_row_login)
        key = stdscr.getch()
        if key == curses.KEY_DOWN and selected_row_login < 2:
            selected_row_login += 1
        elif key == curses.KEY_UP and selected_row_login > 0:
            selected_row_login -= 1
        elif key == 10:
            if selected_row_login == 0:
                username, password = login_interface(stdscr)
                user_id = login(username, password)
                if user_id is not None:
                    break
                else:
                    display_error_message(stdscr, "Nieprawidłowa nazwa użytkownika lub hasło!")
            elif selected_row_login == 1:
                username, password = register_interface(stdscr)
                register(username, password)
            elif selected_row_login == 2:
                sys.exit(0)

    current_favorite_team = get_current_favorite_team(user_id)
    
    while True:
        display_menu(stdscr, menu_options_main, selected_row)
        key = stdscr.getch()
        if key == curses.KEY_DOWN and selected_row < 6:
            selected_row += 1
        elif key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == 10: 
            if selected_row == 5:
                sys.exit(0)
            elif selected_row == 0:
                run_ui(stdscr)
            elif selected_row == 1:
                matches.display_matches(stdscr)
            elif selected_row == 2:
                news_run_ui(stdscr)
            elif selected_row == 3:
                select_quiz(stdscr, user_id)
            elif selected_row == 4:
                handle_favorite_teams(stdscr, user_id, current_favorite_team)

def display_error_message(stdscr, message):
    h, w = stdscr.getmaxyx()
    error_win = curses.newwin(5, len(message) + 4, h // 2 - 2, w // 2 - len(message) // 2 - 2)
    error_win.border()
    error_win.addstr(2, 2, message, curses.A_BOLD)
    error_win.refresh()
    stdscr.getch()            


if __name__ == '__main__':
    curses.wrapper(main)


