import streamlit as st
import random

questions = {
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
        }
    ]
}

def random_question(category):
    question = random.choice(questions[category])
    answers = question["odpowiedzi"].copy()
    random.shuffle(answers)
    return question, answers


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

def select_category(category):
    st.session_state.page = 'quiz'
    st.session_state.kategoria = category
    st.session_state.pytanie, st.session_state.odpowiedzi = random_question(category)
    st.session_state.poprawna_odpowiedz = st.session_state.pytanie["poprawna"]
    st.session_state.zaznaczona_odpowiedz = None
    st.session_state.sprawdzone = False

def reset_quiz():
    st.session_state.page = 'start'
    st.session_state.punkty = 0

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
    kategorie = list(questions.keys())
    for kategoria in kategorie:
        if st.button(kategoria):
            select_category(kategoria)

# Plansza z quizem
elif st.session_state.page == 'quiz':
    st.write("### Pytanie:")
    st.write(st.session_state.pytanie["pytanie"])

    st.write("### Odpowiedzi:")
    st.session_state.zaznaczona_odpowiedz = st.radio("", st.session_state.odpowiedzi, index=0, key="odpowiedzi_radio")

    # Przycisk do sprawdzania odpowiedzi
    if st.button("Sprawdź"):
        st.session_state.sprawdzone = True
        if st.session_state.zaznaczona_odpowiedz == st.session_state.poprawna_odpowiedz:
            st.success("Poprawna odpowiedź!")
            st.session_state.punkty += 1
        else:
            st.error(f"Niepoprawna odpowiedź. Poprawna odpowiedź to: {st.session_state.poprawna_odpowiedz}")

    # Przycisk do przechodzenia do następnego pytania
    if st.session_state.sprawdzone and st.button("Następne pytanie"):
        st.session_state.pytanie, st.session_state.odpowiedzi = random_question(st.session_state.kategoria)
        st.session_state.poprawna_odpowiedz = st.session_state.pytanie["poprawna"]
        st.session_state.zaznaczona_odpowiedz = None
        st.session_state.sprawdzone = False

    st.write("Liczba punktów:", st.session_state.punkty)

    if st.button("Zakończ grę"):
        reset_quiz()
