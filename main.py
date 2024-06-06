import streamlit as st
import random
import time

LEADERBOARD_FILES = {
    'Nauka': 'leaderboard_nauka.txt',
    'Historia': 'leaderboard_historia.txt',
    'Literatura': 'leaderboard_literatura.txt'
}

def load_questions(file):
    questions = []
    try:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    splitted_line = line.split('|')
                    question = splitted_line[0]
                    answers = splitted_line[1].split(';')
                    correct = splitted_line[2]
                    questions.append({
                        'pytanie': question,
                        'odpowiedzi': answers,
                        'poprawna': correct
                    })
    except FileNotFoundError:
        st.error(f"File {file} not found.")
    return questions

categories = {
    'Nauka': load_questions('pytania/nauka.txt'),
    'Historia': load_questions('pytania/historia.txt'),
    'Literatura': load_questions('pytania/literatura.txt')
}

def random_question(category):
    available_indices = list(set(range(len(categories[category]))) - set(st.session_state.asked_questions))
    if not available_indices:
        return None, None
    index = random.choice(available_indices)
    st.session_state.asked_questions.append(index)
    question = categories[category][index]
    answers = question["odpowiedzi"].copy()
    random.shuffle(answers)
    return question, answers

def initialize_session_state():
    st.session_state.page = 'start'
    st.session_state.points = 0
    st.session_state.category = None
    st.session_state.question = None
    st.session_state.answers = None
    st.session_state.correct_answer = None
    st.session_state.picked_answer = None
    st.session_state.checked = False
    st.session_state.asked_questions = []
    st.session_state.results = []
    st.session_state.time_left = 30  # Timer for each question (in seconds)
    st.session_state.score_saved = False  # Ensure score is saved only once

if 'page' not in st.session_state:
    initialize_session_state()

def start_game():
    st.session_state.page = 'select_mode'

def select_category(category):
    st.session_state.page = 'quiz'
    st.session_state.category = category
    st.session_state.asked_questions = []
    st.session_state.results = []
    st.session_state.time_left = 30
    st.session_state.question, st.session_state.answers = random_question(category)
    st.session_state.correct_answer = st.session_state.question["poprawna"]
    st.session_state.picked_answer = None
    st.session_state.checked = False
    st.session_state.score_saved = False

def reset_quiz():
    initialize_session_state()

def next_question():
    st.session_state.time_left = 30
    st.session_state.question, st.session_state.answers = random_question(st.session_state.category)
    if st.session_state.question is None:
        st.session_state.page = 'end'
    else:
        st.session_state.correct_answer = st.session_state.question["poprawna"]
        st.session_state.picked_answer = None
        st.session_state.checked = False

def save_results():
    summary = "Quiz Results\n\n"
    for idx, result in enumerate(st.session_state.results):
        summary += f"Q{idx + 1}: {result['question']}\n"
        summary += f"Your answer: {result['picked']} (Correct: {result['correct']})\n\n"
    return summary

def load_leaderboard(category):
    leaderboard = []
    try:
        with open(LEADERBOARD_FILES[category], 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    name, score = line.split(':')
                    leaderboard.append({'name': name, 'score': int(score)})
    except FileNotFoundError:
        pass
    return leaderboard

def save_leaderboard(category, leaderboard):
    with open(LEADERBOARD_FILES[category], 'w', encoding='utf-8') as f:
        for entry in leaderboard:
            f.write(f"{entry['name']}:{entry['score']}\n")

def update_leaderboard(name, score, category):
    leaderboard = load_leaderboard(category)
    leaderboard.append({'name': name, 'score': score})
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
    save_leaderboard(category, leaderboard)

def display_leaderboard(category):
    st.title(f"Leaderboard - {category}")
    leaderboard = load_leaderboard(category)
    for idx, entry in enumerate(leaderboard):
        st.write(f"{idx + 1}. {entry['name']} - {entry['score']} points")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

if st.session_state.page == 'start':
    st.title("Quiz Wiedzy")
    st.write("Witamy w quizie wiedzy! Naciśnij 'Start gry', aby rozpocząć.")
    if st.button("Start gry"):
        start_game()
        st.experimental_rerun()
    st.write("### Leaderboards:")
    for category in LEADERBOARD_FILES.keys():
        st.write(f"**{category}**")
        display_leaderboard(category)

elif st.session_state.page == 'select_mode':
    st.title("Wybierz kategorię")
    st.write("Wybierz kategorię, w której chcesz odpowiadać na pytania.")
    for categ in categories.keys():
        if st.button(categ):
            select_category(categ)
            st.experimental_rerun()

elif st.session_state.page == 'quiz':
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.write("### Pytanie:")
    st.write(st.session_state.question["pytanie"])

    st.write("### Odpowiedzi:")
    st.session_state.picked_answer = st.radio("", st.session_state.answers, key="radio")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.checked:
        if st.session_state.picked_answer == st.session_state.correct_answer:
            st.success("Poprawna odpowiedź!")
        else:
            st.error(f"Niepoprawna odpowiedź. Poprawna odpowiedź to: {st.session_state.correct_answer}")

    if not st.session_state.checked:
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("Sprawdź", key="sprawdz_button"):
                st.session_state.checked = True
                result = {
                    'question': st.session_state.question["pytanie"],
                    'picked': st.session_state.picked_answer,
                    'correct': st.session_state.correct_answer
                }
                st.session_state.results.append(result)
                if st.session_state.picked_answer == st.session_state.correct_answer:
                    st.success("Poprawna odpowiedź!")
                    st.session_state.points += 1
                else:
                    st.error(f"Niepoprawna odpowiedź. Poprawna odpowiedź to: {st.session_state.correct_answer}")
                st.experimental_rerun()
        with col2:
            st.write(f"Czas: {st.session_state.time_left}")
            progress = st.progress(100 - (st.session_state.time_left * 100 // 30))

        # Countdown timer
        if st.session_state.time_left > 0:
            st.session_state.time_left -= 1
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.session_state.checked = True
            result = {
                'question': st.session_state.question["pytanie"],
                'picked': st.session_state.picked_answer,
                'correct': st.session_state.correct_answer
            }
            st.session_state.results.append(result)
            if st.session_state.picked_answer == st.session_state.correct_answer:
                st.success("Poprawna odpowiedź!")
                st.session_state.points += 1
            else:
                st.error(f"Niepoprawna odpowiedź. Poprawna odpowiedź to: {st.session_state.correct_answer}")
            st.experimental_rerun()

    if st.session_state.checked:
        if st.button("Następne pytanie", key="nastepne_pytanie_button"):
            next_question()
            st.experimental_rerun()

    st.write("Liczba punktów:", st.session_state.points)

    if st.button("Zakończ grę"):
        st.session_state.page = 'end'
        st.experimental_rerun()

elif st.session_state.page == 'end':
    st.title("Koniec gry")
    st.write("Gratulacje, odpowiedziałeś na wszystkie pytania w tej kategorii!")
    st.write(f"Liczba punktów: {st.session_state.points}")

    name = st.text_input("Podaj swoje imię, aby zapisać wynik na tablicy liderów:")
    if name and not st.session_state.score_saved:
        update_leaderboard(name, st.session_state.points, st.session_state.category)
        st.session_state.score_saved = True
        st.success("Wynik zapisany na tablicy liderów!")

    st.write("### Podsumowanie:")
    for result in st.session_state.results:
        st.write(f"Pytanie: {result['question']}")
        st.write(f"Twoja odpowiedź: {result['picked']} (Poprawna odpowiedź: {result['correct']})")
        st.write("")

    summary = save_results()
    st.download_button(label="Pobierz wyniki", data=summary, file_name='quiz_results.txt', mime='text/plain')

    if st.button("Zagraj ponownie"):
        reset_quiz()
        st.experimental_rerun()

    st.write("### Leaderboard:")
    display_leaderboard(st.session_state.category)
