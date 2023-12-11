import curses
from logic import save_quiz_results_to_db, read_quiz_results_from_db, get_specialized_quiz_questions, get_general_quiz_questions
from ascii import quiz_art
from colors import display_ascii_art

def run_general_quiz(stdscr, user_id):
    quiz_name = "Quiz Ogólny"
    quiz_questions = get_general_quiz_questions()
    run_quiz(stdscr, quiz_name, quiz_questions, user_id)

def run_specialized_quiz(stdscr, user_id):
    quiz_name = "Quiz Specjalistyczny"
    quiz_questions = get_specialized_quiz_questions()
    run_quiz(stdscr, quiz_name, quiz_questions, user_id)

def run_quiz(stdscr, quiz_name, quiz_questions, user_id):
    selected_question = 0
    score = 0

    while selected_question < len(quiz_questions):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        question = quiz_questions[selected_question]
        stdscr.addstr(2, 2, f"Pytanie {selected_question + 1}/{len(quiz_questions)} ({quiz_name}):")
        stdscr.addstr(4, 2, question["Pytanie"])

        for i, answer in enumerate(question["Odpowiedzi"]):
            stdscr.addstr(6 + i, 4, answer)

        stdscr.addstr(h - 2, 2, "Wybierz odpowiedź (A, B, C lub D) spośród klawiszy na klawiaturze:")

        stdscr.refresh()
        key = stdscr.getch()
        if key == ord("A") or key == ord("a") or key == ord("B") or key == ord("b") or key == ord("C") or key == ord("c") or key == ord("D") or key == ord("d"):
            selected_answer = chr(key).upper()
            correct_answer = question["Poprawna odpowiedź"]
            if selected_answer == correct_answer:
                score += 1
            selected_question += 1

    save_quiz_results_to_db(user_id, quiz_name, score)

    stdscr.clear()
    stdscr.addstr(h // 2, w // 2 - 10, f"Twój wynik ({quiz_name}): {score}/{len(quiz_questions)}", curses.A_BOLD)
    stdscr.refresh()
    stdscr.getch()

def select_quiz(stdscr, user_id):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    current_row = 0
    menu = ["1. Quiz Ogólny", "2. Quiz Specjalistyczny", "3. Ostatnie Wyniki Quizów", "4. Powrót do menu głównego"]
    selected_quiz = None

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        display_ascii_art(stdscr, quiz_art, color_pair = 5, vertical_offset=7)
        
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
                run_general_quiz(stdscr, user_id)
            elif current_row == 1:
                run_specialized_quiz(stdscr, user_id)
            elif current_row == 2:
                display_quiz_results(stdscr, user_id)
            elif current_row == 3:
                break
        elif key == 27: 
            break

def display_quiz_results(stdscr, user_id):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(2, 2, "Ostatnie 5 wyników quizów:")

    quiz_results = read_quiz_results_from_db(user_id)

    start_index = max(0, len(quiz_results) - 5)
    recent_results = quiz_results[start_index:]

    for i, result in enumerate(recent_results):
        quiz_name, score = result
        stdscr.addstr(4 + i, 4, f"{quiz_name}: {score}/5")

    stdscr.addstr(h - 2, 2, "Naciśnij klawisz 'Enter' aby powrócić do menu głównego")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == 10:
            break


if __name__ == "__main__":
    id = None
    curses.wrapper(lambda stdscr: select_quiz(stdscr, id))