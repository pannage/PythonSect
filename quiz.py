import random
import sys

# Список вопросов
questions = [
    {"question": "What is 2+2?", "options": ["a) 3", "b) 4", "c) 5", "d) 6"], "answer": "b"},
    {"question": "What is the capital of France?", "options": ["a) Berlin", "b) Madrid", "c) Paris", "d) Rome"], "answer": "c"},
    {"question": "What color is the sky?", "options": ["a) Blue", "b) Green", "c) Red", "d) Yellow"], "answer": "a"},
    {"question": "What is 5*3?", "options": ["a) 15", "b) 10", "c) 20", "d) 25"], "answer": "a"},
    {"question": "Which is a fruit?", "options": ["a) Carrot", "b) Apple", "c) Potato", "d) Onion"], "answer": "b"},
    {"question": "What is 10/2?", "options": ["a) 2", "b) 3", "c) 5", "d) 10"], "answer": "c"},
    {"question": "Which animal barks?", "options": ["a) Cat", "b) Dog", "c) Cow", "d) Fish"], "answer": "b"},
    {"question": "What is the color of grass?", "options": ["a) Blue", "b) Red", "c) Green", "d) Black"], "answer": "c"},
    {"question": "How many days in a week?", "options": ["a) 5", "b) 6", "c) 7", "d) 8"], "answer": "c"},
    {"question": "What is 9-3?", "options": ["a) 3", "b) 6", "c) 9", "d) 12"], "answer": "b"}
]

def start():
    # Main menu loop
    while True:
        print("Type 'Start' to begin, 'Admin' to add question, or 'Exit' to quit")
        user_input = input().lower()

        # Start the quiz
        if user_input == "start":
            game_logic()

        # Enter admin mode to add a question
        elif user_input == "admin":
            add_question()

        # Exit the program
        elif user_input == "exit":
            print("Goodbye!")
            sys.exit()

        # Handle unknown commands
        else:
            print("Unknown command")


def game_logic():
    # Initialize score
    score = 0

    # Get random questions (max 5 or less if not enough questions)
    selected_questions = get_random_questions(questions, min(5, len(questions)))

    # Loop through each question
    for q in selected_questions:
        show_question(q)

        # Get user input
        user_answer = get_user_answer()

        # Check if user wants to exit
        if user_answer == "exit":
            exit_program()

        # Check if user wants to add a question
        if user_answer == "admin":
            add_question()
            continue  # Skip current question

        # Check if answer is correct
        if check_answer(user_answer, q["answer"]):
            score += 1

    # Show final result
    show_results(score)


def get_random_questions(question_list, count):
    # Return 'count' random unique questions from the list
    return random.sample(question_list, count)


def show_question(q):
    # Display question text
    print("\n" + q["question"])

    # Display all answer options
    for option in q["options"]:
        print(option)


def get_user_answer():
    # Ask user for input and convert it to lowercase
    return input("Your answer (a/b/c/d) or 'Exit'/'Admin': ").lower()


def check_answer(user_answer, correct_answer):
    # Compare user answer with correct answer
    if user_answer == correct_answer:
        print("Correct!")
        return True
    else:
        print("Wrong!")
        return False


def show_results(score):
    # Display final results
    print("\nGame over")
    print(f"Your score: {score}/5")


def add_question():
    # Admin mode: add a new question
    print("\n--- ADD NEW QUESTION ---")

    # Get question text
    question_text = input("Enter question: ")

    # Get 4 answer options
    options = []
    for letter in ["a", "b", "c", "d"]:
        option = input(f"Option {letter}: ")
        options.append(f"{letter}) {option}")

    # Get correct answer
    correct = input("Correct answer (a/b/c/d): ").lower()

    # Create new question dictionary
    new_question = {
        "question": question_text,
        "options": options,
        "answer": correct
    }

    # Add new question to the list
    questions.append(new_question)

    print("Question added successfully!")


def exit_program():
    # Exit the program safely
    print("Exiting...")
    sys.exit()


# Start the program
start()