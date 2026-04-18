# импорт модуля os — используется для работы с файловой системой (проверка существования файла, удаление файла и т.д.)
import os

# импорт модуля json — нужен для работы с JSON (чтение и запись данных в файл)
import json

# импорт sqlite3 — стандартная библиотека для работы с SQLite базой данных
import sqlite3

# импорт pytest — фреймворк для написания и запуска тестов
import pytest


# импортируем функции, которые будем тестировать, из твоего файла
# ВАЖНО: your_file_name нужно заменить на реальное имя файла без .py
from your_file_name import (
    init_db,              # функция для инициализации базы данных (создания таблиц)
    load_questions,       # функция для загрузки вопросов из БД
    save_question_to_db,  # функция для сохранения вопроса в БД
    check_answer,         # функция для проверки правильности ответа
    export_to_json,       # функция для экспорта данных из БД в JSON файл
    import_from_json      # функция для импорта данных из JSON файла в БД
)


# имя тестовой базы данных, которая будет использоваться только во время тестов
TEST_DB = "test_quiz.db"


# ---------- FIXTURE (подготовка тестовой БД) ----------
# фикстура pytest — это функция, которая выполняется перед тестами
@pytest.fixture
def setup_db(monkeypatch):
    # monkeypatch — встроенный инструмент pytest для подмены функций/поведения

    # здесь мы подменяем sqlite3.connect внутри твоего файла
    # вместо подключения к "боевой" базе — всегда будет использоваться TEST_DB
    monkeypatch.setattr(
        "your_file_name.sqlite3.connect",
        lambda _: sqlite3.connect(TEST_DB)  # игнорируем переданный аргумент и подключаемся к тестовой БД
    )

    # вызываем функцию инициализации БД (создание таблицы questions)
    init_db()

    # yield — точка, где управление передается тесту
    # код ДО yield выполняется ДО теста
    yield

    # код ПОСЛЕ yield выполняется ПОСЛЕ теста

    # если файл тестовой базы существует — удаляем его
    # это нужно, чтобы каждый тест начинался с чистого состояния
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


# ---------- TEST: init_db ----------
def test_init_db_creates_table(setup_db):
    # подключаемся к тестовой базе данных
    conn = sqlite3.connect(TEST_DB)

    # создаем курсор — объект для выполнения SQL-запросов
    cursor = conn.cursor()

    # SQL-запрос:
    # проверяем, существует ли таблица с именем 'questions'
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='questions'"
    )

    # получаем одну строку результата (или None, если таблицы нет)
    table = cursor.fetchone()

    # закрываем соединение с базой данных
    conn.close()

    # проверяем, что таблица существует (не None)
    assert table is not None


# ---------- TEST: save_question_to_db ----------
def test_save_question(setup_db):
    # создаем тестовый вопрос в виде словаря
    question = {
        "question": "2+2?",  # текст вопроса
        "options": ["a) 3", "b) 4", "c) 5", "d) 6"],  # варианты ответа
        "answer": "b"  # правильный ответ
    }

    # сохраняем вопрос в базу данных
    save_question_to_db(question)

    # подключаемся к тестовой базе
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()

    # получаем все строки из таблицы questions
    cursor.execute("SELECT * FROM questions")
    rows = cursor.fetchall()  # список всех записей

    # закрываем соединение
    conn.close()

    # проверяем, что добавилась ровно одна запись
    assert len(rows) == 1

    # проверяем, что текст вопроса совпадает
    # rows[0][1] — это поле question (зависит от структуры таблицы)
    assert rows[0][1] == "2+2?"


# ---------- TEST: load_questions ----------
def test_load_questions(setup_db):
    # создаем тестовый вопрос
    question = {
        "question": "Capital of France?",
        "options": ["a) Berlin", "b) Paris", "c) Rome", "d) Madrid"],
        "answer": "b"
    }

    # сохраняем его в БД
    save_question_to_db(question)

    # вызываем функцию загрузки вопросов
    questions = load_questions()

    # проверяем, что вернулся список из одного элемента
    assert len(questions) == 1

    # проверяем текст вопроса
    assert questions[0]["question"] == "Capital of France?"

    # проверяем правильный ответ
    assert questions[0]["answer"] == "b"


# ---------- TEST: check_answer ----------
def test_check_answer_correct():
    # проверяем, что функция возвращает True при совпадении ответов
    assert check_answer("a", "a") is True


def test_check_answer_wrong():
    # проверяем, что функция возвращает False при несовпадении
    assert check_answer("a", "b") is False


# ---------- TEST: export_to_json ----------
def test_export_to_json(setup_db, monkeypatch):
    # создаем тестовый вопрос
    question = {
        "question": "1+1?",
        "options": ["a) 1", "b) 2", "c) 3", "d) 4"],
        "answer": "b"
    }

    # сохраняем его в БД
    save_question_to_db(question)

    # подменяем input() — вместо ввода пользователя всегда возвращаем "test_export"
    # это значит, что файл будет называться test_export.json
    monkeypatch.setattr("builtins.input", lambda _: "test_export")

    # вызываем функцию экспорта
    export_to_json()

    # проверяем, что файл был создан
    assert os.path.exists("test_export.json")

    # открываем файл и читаем JSON
    with open("test_export.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # проверяем, что в файле 1 вопрос
    assert len(data) == 1

    # проверяем текст вопроса
    assert data[0]["question"] == "1+1?"

    # удаляем файл после теста
    os.remove("test_export.json")


# ---------- TEST: import_from_json ----------
def test_import_from_json(setup_db, monkeypatch):
    # создаем тестовые данные (список с одним вопросом)
    data = [
        {
            "question": "3+3?",
            "options": ["a) 5", "b) 6", "c) 7", "d) 8"],
            "answer": "b"
        }
    ]

    # записываем эти данные в файл test_import.json
    with open("test_import.json", "w", encoding="utf-8") as f:
        json.dump(data, f)

    # подменяем input — теперь функция import_from_json получит имя файла автоматически
    monkeypatch.setattr("builtins.input", lambda _: "test_import.json")

    # вызываем импорт
    import_from_json()

    # подключаемся к базе
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()

    # получаем все записи
    cursor.execute("SELECT * FROM questions")
    rows = cursor.fetchall()

    # закрываем соединение
    conn.close()

    # проверяем, что импортировалась 1 запись
    assert len(rows) == 1

    # проверяем текст вопроса
    assert rows[0][1] == "3+3?"

    # удаляем файл после теста
    os.remove("test_import.json")