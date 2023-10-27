import curses

top_european_leagues_info = [
    {
        "Nazwa ligi": "English Premier League",
        "Kraj": "Anglia",
        "Rok założenia": 1992,
        "Liczba drużyn": 20,
        "Najpopularniejszy klub": "Manchester United",
    },
    {
        "Nazwa ligi": "La Liga",
        "Kraj": "Hiszpania",
        "Rok założenia": 1929,
        "Liczba drużyn": 20,
        "Najpopularniejszy klub": "Real Madrid",
    },
    {
        "Nazwa ligi": "Serie A",
        "Kraj": "Włochy",
        "Rok założenia": 1898,
        "Liczba drużyn": 20,
        "Najpopularniejszy klub": "Juventus",
    },
    {
        "Nazwa ligi": "Bundesliga",
        "Kraj": "Niemcy",
        "Rok założenia": 1963,
        "Liczba drużyn": 18,
        "Najpopularniejszy klub": "Bayern Monachium",
    },
    {
        "Nazwa ligi": "Ligue 1",
        "Kraj": "Francja",
        "Rok założenia": 1932,
        "Liczba drużyn": 20,
        "Najpopularniejszy klub": "Paris Saint-Germain",
    },
]


def get_top_european_leagues(stdscr):
    selected_row = 0
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        # Wyświetl dostępne ligi
        for index, league_info in enumerate(top_european_leagues_info, start=1):
            x = w // 2 - len(league_info['Nazwa ligi']) // 2
            y = h // 2 - len(top_european_leagues_info) // 2 + index - 1
            if index - 1 == selected_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, league_info['Nazwa ligi'])
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, league_info['Nazwa ligi'])
        
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == curses.KEY_DOWN and selected_row < len(top_european_leagues_info) - 1:
            selected_row += 1
        elif key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == 10:  # Enter key
            chosen_league = top_european_leagues_info[selected_row]
            display_league_info(stdscr, chosen_league)
            stdscr.getch()  # Oczekiwanie na naciśnięcie klawisza przed powrotem do menu
        elif key == 27:  # Escape key
            break

def display_league_info(stdscr, league_info):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    y = h // 2 - len(league_info) // 2
    x = w // 2 - max(len(key) for key in league_info) // 2

    for key, value in league_info.items():
        stdscr.addstr(y, x, f"{key}: {value}")
        y += 1
    
    stdscr.refresh()
    stdscr.getch()