import curses
import json
import random
def load_quiz_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Piliki json z pytaniami i odpowiedziami do quizow
general_quiz_file = "data/general_quiz.json"
specialized_quiz_file = "data/specialized_quiz.json"

general_quiz_questions = load_quiz_from_file(general_quiz_file)
specialized_quiz_questions = load_quiz_from_file(specialized_quiz_file)

def run_general_quiz(stdscr):
    random_questions = random.sample(general_quiz_questions, 5)
    run_quiz(stdscr, "Quiz Ogólny", random_questions)

def run_specialized_quiz(stdscr):
    random_questions = random.sample(specialized_quiz_questions, 5)
    run_quiz(stdscr, "Quiz Specjalistyczny", random_questions)

# Funkcja ogólna do uruchamiania quizów
def run_quiz(stdscr, quiz_name, quiz_questions):
    selected_question = 0
    score = 0

    while selected_question < len(quiz_questions):
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Wyswietlamy pytanie
        question = quiz_questions[selected_question]
        stdscr.addstr(2, 2, f"Pytanie {selected_question + 1}/{len(quiz_questions)} ({quiz_name}):")
        stdscr.addstr(4, 2, question["Pytanie"])

        # Wyswietlamy odpowiedzi
        for i, answer in enumerate(question["Odpowiedzi"]):
            stdscr.addstr(6 + i, 4, answer)

        stdscr.refresh()
        # Pobieramy odpowiedz od użytkownika
        key = stdscr.getch()
        if key == ord("A") or key == ord("a") or key == ord("B") or key == ord("b") or key == ord("C") or key == ord("c") or key == ord("D") or key == ord("d"):
            selected_answer = chr(key).upper()
            correct_answer = question["Poprawna odpowiedź"]
            if selected_answer == correct_answer:
                score += 1
            selected_question += 1

    # Wyświetl wynik
    stdscr.clear()
    stdscr.addstr(h // 2, w // 2 - 10, f"Twój wynik ({quiz_name}): {score}/{len(quiz_questions)}", curses.A_BOLD)
    stdscr.refresh()
    stdscr.getch() 

# Funkcja wybierająca quiz
def select_quiz(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    current_row = 0
    menu = ["1. Quiz Ogólny", "2. Quiz Specjalistyczny", "3. Powrót do menu głównego"]
    selected_quiz = None

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        for idx, row in enumerate(menu):
            x = w // 2 - len(row) // 2
            y = h // 2 - len(menu) // 2 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == 10: 
            if current_row == 0:
                run_general_quiz(stdscr)
            elif current_row == 1:
                run_specialized_quiz(stdscr)
            elif current_row == 2:
                break
        elif key == 27: 
            break


if __name__ == "__main__":
    curses.wrapper(select_quiz)