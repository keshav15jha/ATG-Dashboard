import sqlite3

def create_users_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            profile_picture TEXT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            address_line1 TEXT,
            city TEXT,
            state TEXT,
            pincode TEXT,
            user_type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user(first_name, last_name, profile_picture, username, email, password, address_line1, city, state, pincode, user_type):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (first_name, last_name, profile_picture, username, email, password, address_line1, city, state, pincode, user_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, profile_picture, username, email, password, address_line1, city, state, pincode, user_type))
    conn.commit()
    conn.close()

def get_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user
