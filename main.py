import sys
import curses
from football_leagues import get_top_european_leagues
import matches
from news import get_selected_news
from quiz import select_quiz
import sqlite3
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
    init_database()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    selected_row = 0
    selected_row_login = 0
    
    while True:
        initial_screen(stdscr, selected_row_login)
        key = stdscr.getch()
        if key == curses.KEY_DOWN and selected_row_login < 2:
            selected_row_login += 1
        elif key == curses.KEY_UP and selected_row_login > 0:
            selected_row_login -= 1
        elif key == 10:  # Enter key
            if selected_row_login == 0:
                logged_user = login(stdscr)
                if logged_user is not None:
                    break
            elif selected_row_login == 1:
                register(stdscr)
            elif selected_row_login == 2:
                sys.exit(0)
    
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

def initial_screen(stdscr, selected_row):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    menu = ["Zaloguj się", "Zarejestruj się", "Wyjście"]

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

def login(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h // 2 - 1, w // 2 - 7, "Logowanie", curses.A_BOLD)
    stdscr.addstr(h // 2, w // 2 - 10, "Podaj nazwę użytkownika:", curses.A_BOLD)
    stdscr.refresh()
    username = stdscr.getstr(h // 2 + 1, w // 2 - 10, 20).decode("utf-8")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT username, password FROM users WHERE username = ?', (username,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data is not None:
        stored_username, stored_password = user_data
        stdscr.addstr(h // 2 + 2, w // 2 - 10, "Podaj hasło:", curses.A_BOLD)
        stdscr.refresh()
        password = stdscr.getstr(h // 2 + 3, w // 2 - 10, 20).decode("utf-8")

        if password == stored_password:
            return username

        else:
            stdscr.addstr(h // 2 + 2, w // 2 - 10, "Nieprawidłowe hasło.", curses.A_BOLD)
            stdscr.refresh()
            stdscr.getch()
    else:
        stdscr.addstr(h // 2 + 2, w // 2 - 10, "Użytkownik nie istnieje.", curses.A_BOLD)
        stdscr.refresh()
        stdscr.getch()
    return None

def register(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h // 2 - 1, w // 2 - 10, "Rejestracja", curses.A_BOLD)
    stdscr.addstr(h // 2, w // 2 - 13, "Podaj nazwę użytkownika:", curses.A_BOLD)
    stdscr.refresh()
    username = stdscr.getstr(h // 2 + 1, w // 2 - 13, 20).decode("utf-8")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()

    if existing_user is not None:
        stdscr.addstr(h // 2 + 2, w // 2 - 10, "Użytkownik już istnieje.", curses.A_BOLD)
        stdscr.refresh()
        stdscr.getch()
        conn.close()
        return

    stdscr.addstr(h // 2 + 2, w // 2 - 10, "Podaj hasło:", curses.A_BOLD)
    stdscr.refresh()
    password = stdscr.getstr(h // 2 + 3, w // 2 - 10, 20).decode("utf-8")

    # Dodaj nowego użytkownika do bazy danych
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

    stdscr.addstr(h // 2 + 4, w // 2 - 8, "Rejestracja zakończona sukcesem!", curses.A_BOLD)
    stdscr.refresh()
    stdscr.getch()

def init_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    c.execute('''
        INSERT OR IGNORE INTO users (username, password)
        VALUES (?, ?)
    ''', ("user1", "pass1"))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    curses.wrapper(main)
