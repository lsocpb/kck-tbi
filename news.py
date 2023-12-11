from logic import get_news_data, get_selected_news
import textwrap
import curses
from colors import display_ascii_art
from ascii import news_art

def display_news(stdscr, news_list, page):
    selected_row = 0
    rows_per_page = 5
    start_row = page * rows_per_page
    end_row = start_row + rows_per_page

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        display_ascii_art(stdscr, news_art, color_pair=3, vertical_offset=7)

        for index, news_info in enumerate(news_list[start_row:end_row], start=start_row + 1):
            x = w // 2 - len(news_info['Tytuł']) // 2
            y = h // 2 - rows_per_page // 2 + index - start_row - 1

            if index - 1 == start_row + selected_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, news_info['Tytuł'])
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, news_info['Tytuł'])

        stdscr.addstr(h - 2, 4, "Naciśnij 'Escape', aby powrócić do menu", curses.A_BOLD)
        stdscr.addstr(h - 1, w - 20, f"Strona: {page + 1}")
        stdscr.addstr(h - 1, 4, "Naciśnij <- lub -> aby przewijać strony", curses.A_BOLD)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_DOWN and selected_row < rows_per_page - 1 and start_row + selected_row < len(news_list) - 1:
            selected_row += 1
        elif key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == 10:
            chosen_news = get_selected_news(news_list, start_row + selected_row)
            return chosen_news
        elif key == 27:
            return None
        elif key == curses.KEY_RIGHT and end_row < len(news_list):
            page += 1
            selected_row = 0
            start_row = page * rows_per_page
            end_row = start_row + rows_per_page

        elif key == curses.KEY_LEFT and page > 0:
            page -= 1
            selected_row = 0
            start_row = page * rows_per_page
            end_row = start_row + rows_per_page

def display_news_info(stdscr, news_info):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    y = h // 2 - 5
    x = 2

    stdscr.addstr(h - 2, 4, "Naciśnij dowolny klawisz, aby wrócic", curses.A_BOLD)

    stdscr.addstr(y, x, "Treść:")
    y += 2

    wrapped_text = textwrap.wrap(news_info['Treść'], w - 4)
    for line in wrapped_text:
        stdscr.addstr(y, x, line)
        y += 1

    author_info = f"Autor: {news_info['Autor']}"
    stdscr.addstr(h - 1, w - len(author_info) - 2, author_info)

    stdscr.refresh()

def news_run_ui(stdscr):
    page = 0
    while True:
        news_list = get_news_data()
        selected_news = display_news(stdscr, news_list, page)
        if selected_news is not None:
            display_news_info(stdscr, selected_news)
            stdscr.getch()
        else:
            break
