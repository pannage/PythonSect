import random  # import module for random selection
import sys     # import module to exit the program
import json    # import module to work with JSON files


def load_questions():  # function to load questions from JSON file
    try:  # try to open file
        with open("questions.json", "r") as file:  # open file in read mode
            return json.load(file)  # load JSON data and return it
    except FileNotFoundError:  # if file does not exist
        return []  # return empty list


def save_questions(questions):  # function to save questions to JSON file
    with open("questions.json", "w") as file:  # open file in write mode
        json.dump(questions, file, indent=4)  # write data 

questions = load_questions()  # load questions into variable


def start():  # main menu function
    while True:  # infinite loop
        print("\nType 'Start' to begin, 'Admin' to add question, or 'Exit' to quit")  # show menu
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

    show_results(score)  # display final score


def show_question(q):  # function to display a question
    print("\n" + q["question"])  # print question text

    for option in q["options"]:  # loop through options
        print(option)  # print each option


def get_user_answer():  # function to get user input
    return input("Your answer (a/b/c/d): ").lower()  # return lowercase input


def check_answer(user_answer, correct_answer):  # function to check answer
    if user_answer == correct_answer:  # compare answers
        print("Correct!")  # correct message
        return True  # return True
    else:
        print("Wrong!")  # wrong message
        return False  # return False


def show_results(score):  # function to show results
    print("\nGame over")  # end message
    print(f"Your score: {score}/5")  # print score


def add_question():  # function to add new question
    print("\n--- ADD NEW QUESTION ---")  # header

    question_text = input("Enter question: ")  # get question text

    options = []  # create empty list for options

    for letter in ["a", "b", "c", "d"]:  # loop through option labels
        option = input(f"Option {letter}: ")  # get option text
        options.append(f"{letter}) {option}")  # add formatted option to list

    correct = input("Correct answer (a/b/c/d): ").lower()  # get correct answer

    new_question = {  # create dictionary for new question
        "question": question_text,
        "options": options,
        "answer": correct
    }

    questions.append(new_question)  # add new question to list

    save_questions(questions)  # save updated list to JSON file

    print("Question saved!")  # confirmation message


start()  # start the program