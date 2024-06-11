import streamlit as st
import random
import time

LEADERBOARD_FILES = {
    'Nauka': 'leaderboard_nauka.txt',
    'Historia': 'leaderboard_historia.txt',
    'Rozrywka': 'leaderboard_rozrywka.txt'
}

DIFFICULTY_LEVELS = {
    'Łatwy': {'czas': 30, 'pytania': 6},
    'Średni': {'czas': 20, 'pytania': 11},
    'Trudny': {'czas': 10, 'pytania': 16}
}


def load_questions(file):
    questions = []
    try:
        with open(file, 'r',encoding='utf-8' ) as f:
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
    'Rozrywka': load_questions('pytania/rozrywka.txt')
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
    st.session_state.time_left = 30
    st.session_state.score_saved = False
    st.session_state.difficulty = None
    st.session_state.num_questions = 0


if 'page' not in st.session_state:
    initialize_session_state()


def start_game():
    st.session_state.page = 'select_difficulty'


def select_difficulty(difficulty):
    st.session_state.difficulty = difficulty
    st.session_state.time_left = DIFFICULTY_LEVELS[difficulty]['czas']
    st.session_state.num_questions = DIFFICULTY_LEVELS[difficulty]['pytania']
    st.session_state.page = 'select_mode'


def select_category(category):
    st.session_state.page = 'quiz'
    st.session_state.category = category
    st.session_state.asked_questions = []
    st.session_state.results = []
    st.session_state.time_left = DIFFICULTY_LEVELS[st.session_state.difficulty]['czas']
    st.session_state.question, st.session_state.answers = random_question(category)
    st.session_state.correct_answer = st.session_state.question["poprawna"]
    st.session_state.picked_answer = None
    st.session_state.checked = False
    st.session_state.score_saved = False


def reset_quiz():
    initialize_session_state()


def next_question():
    st.session_state.time_left = DIFFICULTY_LEVELS[st.session_state.difficulty]['czas']
    st.session_state.question, st.session_state.answers = random_question(st.session_state.category)
    if len(st.session_state.asked_questions) >= st.session_state.num_questions:
        st.session_state.page = 'end'
    else:
        st.session_state.correct_answer = st.session_state.question["poprawna"]
        st.session_state.picked_answer = None
        st.session_state.checked = False


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
# Strona startowa
if st.session_state.page == 'start':
    st.title("Quiz Wiedzy")
    if st.button("Start gry"):
        start_game()
        st.rerun()
    st.write("### Leaderboards:")
    for category in LEADERBOARD_FILES.keys():
        st.write(f"**{category}**")
        display_leaderboard(category)

# Strona z wyborem poziomu trudnosci
elif st.session_state.page == 'select_difficulty':
    st.title("Wybierz poziom trudności")
    st.write("Im wyższy poziom trudności tym mniej czasu i więcej pytań")
    for level in DIFFICULTY_LEVELS.keys():
        if st.button(level):
            select_difficulty(level)
            st.rerun()
# Strona z wyborem kategorii
elif st.session_state.page == 'select_mode':
    st.title("Wybierz kategorię")
    st.write("Wybierz kategorię quizu.")
    for cat in categories.keys():
        if st.button(cat):
            select_category(cat)
            st.rerun()
# Strona z quizem
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
                st.rerun()
        with col2:
            st.write(f"Czas: {st.session_state.time_left}")
            progress = st.progress(
                100 - (st.session_state.time_left * 100 // DIFFICULTY_LEVELS[st.session_state.difficulty]['czas']))


        if st.session_state.time_left > 0:
            st.session_state.time_left -= 1
            time.sleep(1)
            st.rerun()
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
            st.rerun()

    if st.session_state.checked:
        if st.button("Następne pytanie", key="nastepne_pytanie_button"):
            next_question()
            st.rerun()

    st.write("Liczba punktów:", st.session_state.points)

    if st.button("Zakończ grę"):
        st.session_state.page = 'end'
        st.rerun()
# Strona z koncem gry
elif st.session_state.page == 'end':
    st.title("Koniec gry")

    correct_answers = st.session_state.points
    total_questions = len(st.session_state.results)
    score_percentage = (correct_answers / total_questions) * 100

    st.write(f"Liczba poprawnych odpowiedzi: {correct_answers} z {total_questions}")
    st.write(f"Procent poprawnych odpowiedzi: {score_percentage:.2f}%")
    st.write(f"Liczba punktów: {st.session_state.points}")

    name = st.text_input("Podaj swoje imię, aby zapisać wynik na tablicy wyników:")
    if name and not st.session_state.score_saved:
        update_leaderboard(name, st.session_state.points, st.session_state.category)
        st.session_state.score_saved = True
        st.success("Wynik zapisany na tablicy wyników!")

    st.write("### Podsumowanie:")
    for result in st.session_state.results:
        st.write(f"Pytanie: {result['question']}")
        st.write(f"Twoja odpowiedź: {result['picked']} (Poprawna odpowiedź: {result['correct']})")
        st.write("")

    if st.button("Zagraj ponownie"):
        reset_quiz()
        st.rerun()

    st.write("### Leaderboard:")
    display_leaderboard(st.session_state.category)