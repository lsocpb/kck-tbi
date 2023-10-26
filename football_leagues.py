# Przykładowe informacje o 5 najlepszych ligach europejskich.
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

def display_league_info(league_info):
    for key, value in league_info.items():
        print(f"{key}: {value}")
    print("==============================")

def get_top_european_leagues():
    print("Dostępne ligi:")
    for index, league_info in enumerate(top_european_leagues_info, start=1):
        print(f"{index}. {league_info['Nazwa ligi']}")

    while True:
        try:
            wybor_ligi = int(input("Wybierz ligę (1-5): "))
            if 1 <= wybor_ligi <= 5:
                chosen_league = top_european_leagues_info[wybor_ligi - 1]
                display_league_info(chosen_league)
                break
            else:
                print("Niepoprawny wybór ligi. Wybierz liczbę od 1 do 5.")
        except ValueError:
            print("Niepoprawny wybór ligi. Wybierz liczbę od 1 do 5.")