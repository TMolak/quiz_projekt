import streamlit as st
import random

def load_questions(file):
    questions = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                splittedLine = line.split('|')
                question = splittedLine[0]
                answers = splittedLine[1].split(';')
                correct = splittedLine[2]
                questions.append({
                    'pytanie': question,
                    'odpowiedzi': answers,
                    'poprawna': correct
                })
    return questions

# Wczytywanie pytań z plików
categories = {
    'Nauka': load_questions('pytania/nauka.txt'),
    'Historia': load_questions('pytania/historia.txt'),
    'Literatura': load_questions('pytania/literatura.txt')
}

# Funkcja do losowania pytania z odpowiedziami
def random_question(category):
    question = random.choice(categories[category])
    answers = question["odpowiedzi"].copy()
    random.shuffle(answers)
    return question, answers

# Inicjalizacja sesji
if 'page' not in st.session_state:
    st.session_state.page = 'start'
    st.session_state.points = 0
    st.session_state.category = None
    st.session_state.question = None
    st.session_state.answers = None
    st.session_state.correct_answer = None
    st.session_state.picked_answer = None
    st.session_state.checked = False

def start_game():
    st.session_state.page = 'select_mode'

def select_category(category):
    st.session_state.page = 'quiz'
    st.session_state.category = category
    st.session_state.question, st.session_state.answers = random_question(category)
    st.session_state.correct_answer = st.session_state.question["poprawna"]
    st.session_state.picked_answer = None
    st.session_state.checked = False

def reset_quiz():
    st.session_state.page = 'start'
    st.session_state.points = 0
    st.session_state.category = None
    st.session_state.question = None
    st.session_state.answers = None
    st.session_state.correct_answer = None
    st.session_state.picked_answer = None
    st.session_state.checked = False

def next_question():
    st.session_state.question, st.session_state.answers = random_question(st.session_state.category)
    st.session_state.correct_answer = st.session_state.question["poprawna"]
    st.session_state.picked_answer = None
    st.session_state.checked = False

# Strona startowa
if st.session_state.page == 'start':
    st.title("Quiz Wiedzy")
    st.write("Witamy w quizie wiedzy! Naciśnij 'Start gry', aby rozpocząć.")
    if st.button("Start gry"):
        start_game()
        st.experimental_rerun()

# Wybór trybu gry
elif st.session_state.page == 'select_mode':
    st.title("Wybierz kategorię")
    st.write("Wybierz kategorię, w której chcesz odpowiadać na pytania.")
    for categ in categories.keys():
        if st.button(categ):
            select_category(categ)
            st.experimental_rerun()

# Plansza z quizem
elif st.session_state.page == 'quiz':
    st.write("### Pytanie:")
    st.write(st.session_state.question["pytanie"])

    st.write("### Odpowiedzi:")
    st.session_state.picked_answer = st.radio("", st.session_state.answers, key="radio")

    if st.session_state.checked:
        if st.session_state.picked_answer == st.session_state.correct_answer:
            st.success("Poprawna odpowiedź!")
        else:
            st.error(f"Niepoprawna odpowiedź. Poprawna odpowiedź to: {st.session_state.correct_answer}")

    # Przycisk do sprawdzania odpowiedzi
    if not st.session_state.checked:
        if st.button("Sprawdź", key="sprawdz_button"):
            st.session_state.checked = True
            if st.session_state.picked_answer == st.session_state.correct_answer:
                st.success("Poprawna odpowiedź!")
                st.session_state.points += 1
            else:
                st.error(f"Niepoprawna odpowiedź. Poprawna odpowiedź to: {st.session_state.correct_answer}")
            st.experimental_rerun()

    # Przycisk do przechodzenia do następnego pytania
    if st.session_state.checked:
        if st.button("Następne pytanie", key="nastepne_pytanie_button"):
            next_question()
            st.experimental_rerun()

    st.write("Liczba punktów:", st.session_state.points)

    if st.button("Zakończ grę"):
        reset_quiz()
        st.experimental_rerun()
