# ---------------- IMPORTS ----------------

import sqlite3  # module for SQLite database work
import json     # module for JSON import/export
from flask import Flask, request, jsonify, render_template  # Flask web framework
import random   # module for random selection of questions

# ---------------- FLASK APP ----------------

app = Flask(__name__)  # create Flask application instance

DB_NAME = "quiz.db"  # database file name

# ---------------- DATABASE INIT ----------------

def init_db():
    # connect to SQLite database (creates file if not exists)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # create table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            question TEXT,
            option_a TEXT,
            option_b TEXT,
            option_c TEXT,
            option_d TEXT,
            correct TEXT   
        )
    """)

    conn.commit()  # save changes to database
    conn.close()   # close connection


# ---------------- DATABASE CONNECTION ----------------

def get_db():
    # create and return database connection
    return sqlite3.connect(DB_NAME)


# ---------------- LOAD QUESTIONS ----------------

def load_questions():
    conn = get_db()        # connect to DB
    cursor = conn.cursor() # create cursor

    cursor.execute("SELECT * FROM questions")  # select all questions
    rows = cursor.fetchall()  # fetch all results

    conn.close()  # close connection

    questions = []  # list for formatted questions

    for row in rows:
        questions.append({
            "id": row[0],  # question ID
            "question": row[1],  # question text
            "options": [
                f"a) {row[2]}",  # option A
                f"b) {row[3]}",  # option B
                f"c) {row[4]}",  # option C
                f"d) {row[5]}"   # option D
            ],
            "answer": row[6]  # correct answer
        })

    return questions  # return list of questions


# ---------------- SAVE QUESTION ----------------

def save_question(q):
    conn = get_db()        # connect to DB
    cursor = conn.cursor() # create cursor

    cursor.execute("""
        INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        q["question"],      # question text
        q["options"][0],    # option A
        q["options"][1],    # option B
        q["options"][2],    # option C
        q["options"][3],    # option D
        q["answer"]         # correct answer
    ))

    conn.commit()  # save changes
    conn.close()   # close connection


# ---------------- DELETE QUESTION ----------------

def delete_question(q_id):
    conn = get_db()        # connect to DB
    cursor = conn.cursor() # create cursor

    cursor.execute("DELETE FROM questions WHERE id = ?", (q_id,))  # delete by id

    conn.commit()  # save changes
    conn.close()   # close connection


# ---------------- ROUTES ----------------

@app.route("/")  # main page route
def index():
    # render HTML page from templates folder
    return render_template("index.html")


@app.route("/questions", methods=["GET"])  # get all questions
def get_questions():
    # return JSON list of questions
    return jsonify(load_questions())


@app.route("/questions", methods=["POST"])  # add question
def add_question():
    # get JSON data from request
    data = request.json

    # save question to database
    save_question(data)

    # return success response
    return jsonify({"status": "ok"})


@app.route("/questions/<int:q_id>", methods=["DELETE"])  # delete question
def remove_question(q_id):
    # delete question by id
    delete_question(q_id)

    # return response
    return jsonify({"status": "deleted"})


# ---------------- RUN SERVER ----------------

if __name__ == "__main__":
    init_db()  # initialize database before starting server
    app.run(debug=True)  # start Flask server