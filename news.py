import curses

news_info = [
    {
        "Tytuł": "Lewandowski najlepszym piłkarzem świata w 2020 roku",
        "Autor": "Onet Sport",
        "Data": "2020-12-17",
    },
    {
        "Tytuł": "Onana najgorszym bramkarzem Ligi Mistrzów. Lewandowski na podium",
        "Autor": "Onet Sport",
        "Data": "2020-12-17",
    },
    {
        "Tytuł": "Ronaldo i Lewandowski w najlepszej jedenastce 2020 roku",
        "Autor": "Onet Sport",
        "Data": "2020-12-17",
    },
    {
        "Tytuł": "Messi i Ronaldo nie w najlepszej jedenastce 2020 roku",
        "Autor": "Onet Sport",
        "Data": "2020-12-17",
    },
]

def get_news(stdscr):
    selected_row = 0
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Wyświetl dostępne newsy
        for index, news in enumerate(news_info, start=1):
            x = w // 2 - len(news['Tytuł']) // 2
            y = h // 2 - len(news_info) // 2 + index - 1
            if index - 1 == selected_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, news['Tytuł'])
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, news['Tytuł'])
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_DOWN and selected_row < len(news_info) - 1:
            selected_row += 1
        elif key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == 10:  # Enter key
            chosen_news = news_info[selected_row]
            display_news(stdscr, chosen_news)
            stdscr.getch()
        elif key == 27:  # Escape key
            break

def display_news(stdscr, news):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    y = h // 2 - len(news) // 2
    x = w // 2 - max(len(key) for key in news) // 2

    for key, value in news.items():
        stdscr.addstr(y, x, f"{key}: {value}")
        y += 1

    stdscr.refresh()
    stdscr.getch()