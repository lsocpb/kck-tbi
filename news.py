import curses
import textwrap

def get_selected_news(stdscr):
    news_list = [
        {
            "Tytuł": "Niesamowity mecz zakończony remisem",
            "Autor": "Jan Kowalski",
            "Data dodania": "2023-10-25",
            "Treść": "Wczorajszy mecz pomiędzy drużyną A i drużyną B zakończył się niesamowitym remisem z wynikiem 3-3. Kibice byli zachwyceni występem obu drużyn."
        },
        {
            "Tytuł": "Nowy transfer w drużynie X",
            "Autor": "Anna Nowak",
            "Data dodania": "2023-10-24",
            "Treść": "Drużyna X ogłosiła nowy transfer. Zespół pozyskał utalentowanego napastnika, który ma wzmocnić linię ataku."
        },
        {
            "Tytuł": "Klub Y zwycięzcą turnieju",
            "Autor": "Piotr Zawadzki",
            "Data dodania": "2023-10-23",
            "Treść": "Klub Y odniósł zwycięstwo w międzynarodowym turnieju piłkarskim. To już kolejny sukces drużyny w tym sezonie."
        },
    ]

    selected_row = 0
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        
        for index, news_info in enumerate(news_list, start=1):
            x = w // 2 - len(news_info['Tytuł']) // 2
            y = h // 2 - len(news_list) // 2 + index - 1
            if index - 1 == selected_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, news_info['Tytuł'])
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, news_info['Tytuł'])

        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_DOWN and selected_row < len(news_list) - 1:
            selected_row += 1
        elif key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == 10:  
            chosen_news = news_list[selected_row]
            display_news_info(stdscr, chosen_news)
            stdscr.getch()  
        elif key == 27:  
            break

def display_news_info(stdscr, news_info):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    y = h // 2 - 5 
    x = 2

    stdscr.addstr(y, x, "Treść:")
    y += 2

    wrapped_text = textwrap.wrap(news_info['Treść'], w - 4)
    for line in wrapped_text:
        stdscr.addstr(y, x, line)
        y += 1

    stdscr.refresh()

if __name__ == '__main__':
    curses.wrapper(get_selected_news)
