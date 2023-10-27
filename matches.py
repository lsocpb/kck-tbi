import requests
import curses

def get_active_matches():
    uri = 'https://api.football-data.org/v4/matches'
    headers = {'X-Auth-Token': '85fb8206e47442b38dfb484ba39522cf'}
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



def display_matches(stdscr, matches):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    if not matches:
        stdscr.addstr(h // 2, w // 2 - 15, "Brak aktywnych meczów.", curses.A_BOLD)
    else:
        y = h // 2 - len(matches) // 2

        for match in matches:
            x = w // 2 - len(match) // 2
            stdscr.addstr(y, x, match)
            y += 1

    stdscr.refresh()
    stdscr.getch()
