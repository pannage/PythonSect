import random  # import module for random selection
import sys     # import module to exit the program
import json    # import module to work with JSON files
import sqlite3 # import module to work DB

# ---------------- DATABASE SETUP ----------------

def init_db():  # function to initialize database
    conn = sqlite3.connect("quiz.db")  # connect to database (creates file if not exists)
    cursor = conn.cursor()  # create cursor to execute SQL commands

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (  -- create table if it doesn't exist
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- unique ID for each question
            question TEXT,                         -- question text
            option_a TEXT,                         -- option A
            option_b TEXT,                         -- option B
            option_c TEXT,                         -- option C
            option_d TEXT,                         -- option D
            correct TEXT                           -- correct answer (a/b/c/d)
        )
    """)

    conn.commit()  # save changes
    conn.close()   # close connection


# ---------------- LOAD QUESTIONS ----------------

def load_questions():  # function to load questions from database
    conn = sqlite3.connect("quiz.db")  # connect to database
    cursor = conn.cursor()  # create cursor

    cursor.execute("SELECT * FROM questions")  # get all questions
    rows = cursor.fetchall()  # fetch all rows

    conn.close()  # close connection

    questions = []  # create empty list

    for row in rows:  # iterate through database rows
        questions.append({  # convert each row to dictionary
            "question": row[1],  # question text
            "options": [  # list of options
                f"a) {row[2]}",  # option A
                f"b) {row[3]}",  # option B
                f"c) {row[4]}",  # option C
                f"d) {row[5]}"   # option D
            ],
            "answer": row[6]  # correct answer
        })

    return questions  # return list of questions

# ---------------- SAVE QUESTION ----------------

def save_question_to_db(q):  # function to save one question to database
    conn = sqlite3.connect("quiz.db")  # connect to database
    cursor = conn.cursor()  # create cursor

    cursor.execute("""
        INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct)
        VALUES (?, ?, ?, ?, ?, ?)  -- insert new question
    """, (
        q["question"],        # question text
        q["options"][0][3:],  # remove 'a) ' from option A
        q["options"][1][3:],  # remove 'b) '
        q["options"][2][3:],  # remove 'c) '
        q["options"][3][3:],  # remove 'd) '
        q["answer"]           # correct answer
    ))

    conn.commit()  # save changes
    conn.close()   # close connection


# initialize database
init_db()  # ensure DB and table exist

# load questions into variable
questions = load_questions()  # load all questions from DB

# ---------------- MAIN MENU ----------------
def start():  # main menu function
    while True:  # infinite loop
        print("\nType 'Start' to begin, 'Admin' to add question, or 'Exit' to quit, 'Import'/'Export'")  # show menu
        user_input = input().lower()  # get input and convert to lowercase

        if user_input == "start":  # if user wants to start quiz
            if not questions:  # check if list is empty
                print("No questions yet! Add some in Admin mode.")  # warning message
            else:
                game_logic()  # start quiz

        elif user_input == "admin":  # if user enters admin mode
            add_question()  # call function to add question

        elif user_input == "exit":  # if user wants to exit
            print("Goodbye!")  # farewell message
            sys.exit()  # terminate program

        elif user_input == "export":
            export_to_json()

        elif user_input == "import":
            import_from_json()

        else:  # if command is unknown
            print("Unknown command")  # error message

def game_logic():  # main quiz logic
    score = 0  # initialize score

    # select random questions (max 5 or less if not enough)
    selected_questions = random.sample(questions, min(5, len(questions)))

    for q in selected_questions:  # loop through selected questions
        show_question(q)  # display question

        user_answer = get_user_answer()  # get answer from user

        if check_answer(user_answer, q["answer"]):  # check if correct
            score += 1  # increase score

    show_results(score, len(selected_questions))  # display final score


# ---------------- DISPLAY QUESTION ----------------

def show_question(q):  # function to display a question
    print("\n" + q["question"])  # print question text

    for option in q["options"]:  # loop through options
        print(option)  # print each option


# ---------------- USER INPUT ----------------

def get_user_answer():  # function to get user input
    return input("Your answer (a/b/c/d): ").lower()  # return lowercase input


# ---------------- CHECK ANSWER ----------------

def check_answer(user_answer, correct_answer):  # function to check answer
    if user_answer == correct_answer:  # compare answers
        print("Correct!")  # correct message
        return True  # return True
    else:
        print("Wrong!")  # wrong message
        return False  # return False


# ---------------- RESULTS ----------------

def show_results(score, questions_count):  # function to show results
    print("\nGame over")  # end message
    print(f"Your score: {score}/{questions_count}")  # print score


# ---------------- ADD QUESTION ----------------

def add_question():  # function to add new question
    global questions  # use global variable

    print("\n--- ADD NEW QUESTION ---")  # header

    question_text = input("Enter question: ")  # get question text

    options = []  # create empty list for options

    for letter in ["a", "b", "c", "d"]:  # loop through option labels
        option = input(f"Option {letter}: ")  # get option text
        options.append(f"{letter}) {option}")  # format and add to list

    correct = input("Correct answer (a/b/c/d): ").lower()  # get correct answer

    new_question = {  # create dictionary for new question
        "question": question_text,
        "options": options,
        "answer": correct
    }

    save_question_to_db(new_question)  # save question to database

    questions = load_questions()  # reload questions from DB

    print("Question saved!")  # confirmation message

# new function for export logic
def export_to_json():
    # user input filename
    filename = input("Enter file name (without .json): ")

    # add .json
    filename = filename + ".json"

    # connect DB
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    # get all questions
    cursor.execute("SELECT * FROM questions")
    rows = cursor.fetchall()

    conn.close()

    data = []

    # transform the data into a JSON 
    for row in rows:
        question_dict = {
            "question": row[1],
            "options": [
                f"a) {row[2]}",
                f"b) {row[3]}",
                f"c) {row[4]}",
                f"d) {row[5]}"
            ],
            "answer": row[6]
        }

        data.append(question_dict)

    # save to file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Exported {len(data)} questions to {filename}")


# new function for import logic
def import_from_json():
    global questions

    filename = input("Enter file name (with .json): ")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        for q in data:
            save_question_to_db(q)

        questions = load_questions()

        print(f"Imported {len(data)} questions from {filename}")

    except FileNotFoundError:
        print("File not found!")

    except json.JSONDecodeError:
        print("Invalid JSON file!")

# ---------------- START PROGRAM ----------------

start()  # start the program