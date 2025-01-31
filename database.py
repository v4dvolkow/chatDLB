import sqlite3

# Функция для создания базы данных и таблиц
def init_db():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    # Создаем таблицу для вопросов, если она не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            question TEXT,
            answer TEXT DEFAULT NULL
        )
    ''')
    # Создаем таблицу для файлов (изображений и документов), если она не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            file_type TEXT,  -- 'photo' или 'document'
            file_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Функция для добавления вопроса в базу данных
def add_question(user_id, username, question):
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO questions (user_id, username, question)
        VALUES (?, ?, ?)
    ''', (user_id, username, question))
    conn.commit()
    conn.close()

# Функция для получения всех нерешенных вопросов
def get_unanswered_questions():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions WHERE answer IS NULL')
    questions = cursor.fetchall()
    conn.close()
    return questions

# Функция для обновления ответа на вопрос
def update_answer(question_id, answer):
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE questions
        SET answer = ?
        WHERE id = ?
    ''', (answer, question_id))
    conn.commit()
    conn.close()

# Функция для добавления файла в базу данных
def add_file(user_id, username, file_type, file_path):
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO files (user_id, username, file_type, file_path)
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, file_type, file_path))
    conn.commit()
    conn.close()

# Функция для получения всех файлов
def get_all_files():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM files')
    files = cursor.fetchall()
    conn.close()
    return files