import streamlit as st
import random

# Definiujemy pytania i odpowiedzi
pytania = {
    "Nauka": [
        {
            "pytanie": "Jaka jest największa planeta w Układzie Słonecznym?",
            "odpowiedzi": ["Mars", "Jowisz", "Ziemia", "Saturn"],
            "poprawna": "Jowisz"
        },
        {
            "pytanie": "Który pierwiastek chemiczny ma symbol 'H'?",
            "odpowiedzi": ["Hel", "Wodór", "Węgiel", "Azot"],
            "poprawna": "Wodór"
        },
        {
            "pytanie": "Jak nazywa się proces, w którym rośliny przekształcają światło słoneczne w energię?",
            "odpowiedzi": ["Fotosynteza", "Respiracja", "Fermentacja", "Transpiracja"],
            "poprawna": "Fotosynteza"
        },
        {
            "pytanie": "Który gaz jest niezbędny do oddychania?",
            "odpowiedzi": ["Azot", "Tlen", "Dwutlenek węgla", "Hel"],
            "poprawna": "Tlen"
        },
        {
            "pytanie": "Jak nazywa się najtwardszy naturalnie występujący minerał?",
            "odpowiedzi": ["Granat", "Diament", "Kwarc", "Topaz"],
            "poprawna": "Diament"
        }
    ],
    "Historia": [
        {
            "pytanie": "Kto był pierwszym prezydentem Stanów Zjednoczonych?",
            "odpowiedzi": ["George Washington", "Abraham Lincoln", "Thomas Jefferson", "John Adams"],
            "poprawna": "George Washington"
        },
        {
            "pytanie": "W którym roku rozpoczęła się II wojna światowa?",
            "odpowiedzi": ["1914", "1939", "1945", "1941"],
            "poprawna": "1939"
        },
        {
            "pytanie": "Jak nazywał się król Francji, który został stracony podczas Rewolucji Francuskiej?",
            "odpowiedzi": ["Ludwik XIV", "Ludwik XVI", "Karol X", "Napoleon Bonaparte"],
            "poprawna": "Ludwik XVI"
        },
        {
            "pytanie": "Która cywilizacja zbudowała piramidy w Gizie?",
            "odpowiedzi": ["Majowie", "Aztekowie", "Egipcjanie", "Inkowie"],
            "poprawna": "Egipcjanie"
        },
        {
            "pytanie": "Jak nazywał się statek, którym Kolumb odkrył Amerykę?",
            "odpowiedzi": ["Mayflower", "Santa Maria", "Endeavour", "Discovery"],
            "poprawna": "Santa Maria"
        }
    ],
    "Literatura": [
        {
            "pytanie": "Kto jest autorem powieści 'Zdobywca'?",
            "odpowiedzi": ["Ernest Hemingway", "F. Scott Fitzgerald", "William Faulkner", "Thomas Wolfe"],
            "poprawna": "Thomas Wolfe"
        },
        {
            "pytanie": "Które z poniższych dzieł napisał William Shakespeare?",
            "odpowiedzi": ["Wojna i pokój", "Romeo i Julia", "Wielki Gatsby", "Zbrodnia i kara"],
            "poprawna": "Romeo i Julia"
        },
        {
            "pytanie": "Kto jest autorem powieści 'Wielki Gatsby'?",
            "odpowiedzi": ["F. Scott Fitzgerald", "Ernest Hemingway", "John Steinbeck", "William Faulkner"],
            "poprawna": "F. Scott Fitzgerald"
        },
        {
            "pytanie": "Która z tych książek została napisana przez George'a Orwella?",
            "odpowiedzi": ["1984", "Rok 1984", "Nowy wspaniały świat", "Mechaniczna pomarańcza"],
            "poprawna": "1984"
        },
        {
            "pytanie": "Jak nazywa się główny bohater powieści 'Moby Dick'?",
            "odpowiedzi": ["Ishmael", "Ahab", "Queequeg", "Starbuck"],
            "poprawna": "Ishmael"
        }
    ]
}

# Funkcja do losowania pytania z odpowiedziami
def losuj_pytanie(kategoria):
    pytanie = random.choice(pytania[kategoria])
    odpowiedzi = pytanie["odpowiedzi"].copy()
    random.shuffle(odpowiedzi)
    return pytanie, odpowiedzi

# Inicjalizacja sesji
if 'page' not in st.session_state:
    st.session_state.page = 'start'
    st.session_state.punkty = 0
    st.session_state.kategoria = None
    st.session_state.pytanie = None
    st.session_state.odpowiedzi = None
    st.session_state.poprawna_odpowiedz = None
    st.session_state.zaznaczona_odpowiedz = None
    st.session_state.sprawdzone = False

def start_game():
    st.session_state.page = 'select_mode'
    st.experimental_rerun()

def select_category(category):
    st.session_state.page = 'quiz'
    st.session_state.kategoria = category
    st.session_state.pytanie, st.session_state.odpowiedzi = losuj_pytanie(category)
    st.session_state.poprawna_odpowiedz = st.session_state.pytanie["poprawna"]
    st.session_state.zaznaczona_odpowiedz = None
    st.session_state.sprawdzone = False
    st.experimental_rerun()

def reset_quiz():
    st.session_state.page = 'start'
    st.session_state.punkty = 0
    st.experimental_rerun()

def next_question():
    st.session_state.pytanie, st.session_state.odpowiedzi = losuj_pytanie(st.session_state.kategoria)
    st.session_state.poprawna_odpowiedz = st.session_state.pytanie["poprawna"]
    st.session_state.zaznaczona_odpowiedz = None
    st.session_state.sprawdzone = False
    st.experimental_rerun()

# Strona startowa
if st.session_state.page == 'start':
    st.title("Quiz Wiedzy")
    st.write("Witamy w quizie wiedzy! Naciśnij 'Start gry', aby rozpocząć.")
    if st.button("Start gry"):
        start_game()

# Wybór trybu gry
elif st.session_state.page == 'select_mode':
    st.title("Wybierz kategorię")
    st.write("Wybierz kategorię, w której chcesz odpowiadać na pytania.")
    kategorie = list(pytania.keys())
    for kategoria in kategorie:
        if st.button(kategoria):
            select_category(kategoria)

# Plansza z quizem
elif st.session_state.page == 'quiz':
    st.write("### Pytanie:")
    st.write(st.session_state.pytanie["pytanie"])

    st.write("### Odpowiedzi:")
    st.session_state.zaznaczona_odpowiedz = st.radio("", st.session_state.odpowiedzi)

    # Przycisk do sprawdzania odpowiedzi
    if not st.session_state.sprawdzone:
        if st.button("Sprawdź", key="sprawdz_button"):
            st.session_state.sprawdzone = True
            if st.session_state.zaznaczona_odpowiedz == st.session_state.poprawna_odpowiedz:
                st.success("Poprawna odpowiedź!")
                st.session_state.punkty += 1
            else:
                st.error(f"Niepoprawna odpowiedź. Poprawna odpowiedź to: {st.session_state.poprawna_odpowiedz}")
            st.experimental_rerun()

    # Przycisk do przechodzenia do następnego pytania
    if st.session_state.sprawdzone:
        if st.button("Następne pytanie", key="nastepne_pytanie_button"):
            next_question()

    st.write("Liczba punktów:", st.session_state.punkty)

    if st.button("Zakończ grę"):
        reset_quiz()
