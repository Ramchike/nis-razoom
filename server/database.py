import psycopg2

DB_CONFIG = {
    'dbname': 'yourdatabase',
    'user': 'yourusername',
    'password': 'yourpassword',
    'host': 'localhost',
    'port': '5432'
}


def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn


# Функция для инициализации базы данных (создание таблиц)
def initialize_db():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS States (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            type VARCHAR(50),
            harm_allowance FLOAT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Ranks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            salary FLOAT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS unstand_allowance (
            id SERIAL PRIMARY KEY,
            percent FLOAT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Employees (
            id SERIAL PRIMARY KEY,
            state_id INTEGER REFERENCES States(id) ON DELETE SET NULL,
            rank_id INTEGER REFERENCES Ranks(id) ON DELETE SET NULL,
            unstand_allowance_id INTEGER REFERENCES unstand_allowance(id) ON DELETE SET NULL
        );
        """
    ]

    conn = get_db_connection()
    cursor = conn.cursor()

    for command in commands:
        cursor.execute(command)

    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized successfully.")
