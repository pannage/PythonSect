import random

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
    print("Type 'Start' to begin the quiz")
    user_input = input()
    if user_input.lower() == "start":
        game_logic()
    else:
        print("You need to type 'Start' to begin.")

def game_logic():
    score = 0
    selected_questions = random.sample(questions, 5)

    for q in selected_questions:
        print("\n" + q["question"])
        for option in q["options"]:
            print(option)

        answer = input("Your answer (a/b/c/d): ").lower()

        if answer == q["answer"]:
            print("Correct!")
            score += 1
        else:
            print("Wrong!")

    results(score)

def results(score):
    print("\nGame over")
    print(f"Your score: {score}/5")

start()