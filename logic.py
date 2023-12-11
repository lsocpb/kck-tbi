import sqlite3
import json
import requests
import bcrypt
import random
import os
# LOGIC FOR JSON LOADING INTO APP

def load_info(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    except Exception as e:
        print(f"Error loading data from {path}: {e}")
        return None


# LOGIC FOR FAVORITE TEAMS

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
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT favorite_team FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return "Brak ulubionej drużyny"
    except sqlite3.Error as e:
        return "Błąd pobierania ulubionej drużyny"
    finally:
        conn.close()

def get_last_results(user_id):
    current_favorite_team = get_current_favorite_team(user_id)

    if current_favorite_team == "Brak ulubionej drużyny":
        return "Nie wybrano ulubionej drużyny."
    else:
        try:
            with open("data/last_results.json", "r") as file:
                match_results = json.load(file)
                if "teams" in match_results and current_favorite_team in match_results["teams"]:
                    team_results = match_results["teams"][current_favorite_team]["results"]
                    last_results = []
                    for i, result in enumerate(team_results[-5:][::-1], start=1):
                        outcome_color = "RED" if result["outcome"] == "LOSER" else "GREEN"
                        if result["outcome"] == "DRAW":
                            outcome_color = "YELLOW"
                        last_results.append({
                            "opponent": result["opponent"],
                            "score": result["score"],
                            "outcome": result["outcome"],
                            "color": outcome_color
                        })
                    return {
                        "team_name": current_favorite_team,
                        "results": last_results
                    }
                else:
                    return f"Brak wyników dla {current_favorite_team}."
        except FileNotFoundError:
            return "Brak pliku z wynikami."
        
# LOGIC FOR FOOTBALL LEAGUES

path = "data/top_european_leagues_info.json"
top_european_leagues_info = load_info(path)

def get_selected_league_info(selected_row, top_european_leagues_info):
    if 0 <= selected_row < len(top_european_leagues_info):
        return top_european_leagues_info[selected_row]
    else:
        return None
    
# LOGIC FOR ACTIVE MATCHES DISPLAY:

def get_active_matches():
    api_key = os.environ.get('FOOTBALL_API_KEY')
    uri = 'https://api.football-data.org/v4/matches'
    headers = {'X-Auth-Token': api_key}
    response = requests.get(uri, headers=headers)
    data = response.json()

    if 'matches' in data:
        matches = data['matches']
        active_matches = []

        for match in matches:
            if 'status' in match and match['status'] == 'IN_PLAY' and 'competition' in match and 'name' in match['competition'] and match['competition']['name'] in ['Bundesliga', 'Ligue 1', 'Primera Division', 'Premier League', 'Serie A']:
                home_team_name = match['homeTeam']['name'] if 'homeTeam' in match else 'Nieznany gospodarz'
                away_team_name = match['awayTeam']['name'] if 'awayTeam' in match else 'Nieznany gość'
                home_team_score = match['score']['fullTime']['home'] if 'score' in match and 'fullTime' in match['score'] and 'home' in match['score']['fullTime'] else '?'
                away_team_score = match['score']['fullTime']['away'] if 'score' in match and 'fullTime' in match['score'] and 'away' in match['score']['fullTime'] else '?'
                competition_name = match['competition']['name']
                formatted_match = f"{home_team_name} {home_team_score} - {away_team_score} {away_team_name} ({competition_name})"
                active_matches.append(formatted_match)

        return active_matches
    return []

# LOGIC FOR NEWS DISPLAY:

def get_selected_news(news_list, selected_row):
    if 0 <= selected_row < len(news_list):
        return news_list[selected_row]
    else:
        return None
    
def get_news_data():
    path = "data/news.json"
    return load_info(path)


# LOGIC FOR QUIZ:

def save_quiz_results_to_db(user_id, quiz_name, score):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    if user is not None:
        cursor.execute('INSERT INTO quiz_results (user_id, quiz_name, score) VALUES (?, ?, ?)', (user_id, quiz_name, score))
        conn.commit()
    conn.close()

def read_quiz_results_from_db(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT quiz_name, score FROM quiz_results WHERE user_id = ?', (user_id,))
    quiz_results = cursor.fetchall()
    conn.close()
    return quiz_results

general_quiz_path = "data/general_quiz.json"
specialized_quiz_path = "data/specialized_quiz.json"

general_quiz_questions = load_info(general_quiz_path)
specialized_quiz_questions = load_info(specialized_quiz_path)

def get_general_quiz_questions():
    random_questions = random.sample(general_quiz_questions, 5)
    return random_questions

def get_specialized_quiz_questions():
    random_questions = random.sample(specialized_quiz_questions, 5)
    return random_questions

# LOGIC FOR USER REGISTRATION AND LOGIN:

def login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT username, password, id FROM users WHERE username = ?', (username,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data is not None:
        stored_username, stored_password, id = user_data
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return id
    return None

def register(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()

    if existing_user is not None:
        conn.close()
        return False

    salt = bcrypt.gensalt(rounds=15)
    if password is None:
        return False
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()

    return username

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
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            quiz_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    c.execute('''
        INSERT OR IGNORE INTO users (username, password)
        VALUES (?, ?)
    ''', ("user1", "pass1"))

    conn.commit()
    conn.close()

