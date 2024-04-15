import sqlite3
import hashlib
import os

DATABASE_PATH = "C:\\Users\\Chris\\Desktop\\FacialRecognition\\pythonProject\\user_data.db"

def create_connection():
    """Create a database connection to the SQLite database specified by DATABASE_PATH."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def setup_database():
    """Setup the database and create the necessary users table if it doesn't already exist."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    image_path TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error setting up database: {e}")
        finally:
            conn.close()

def hash_password(password):
    """Generate a hash and salt for a given password."""
    salt = os.urandom(16)  # Generate a random 16-byte salt
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000), salt

def save_user(username, image_path, password):
    """Save a new user with their username, image path, and hashed password."""
    password_hash, salt = hash_password(password)
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, image_path, password_hash, salt)
                VALUES (?, ?, ?, ?)
            """, (username, image_path, password_hash, salt))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving user to database: {e}")
        finally:
            conn.close()

def check_user(username, password):
    """Verify a user's password against the hash stored in the database."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT password_hash, salt FROM users WHERE username = ?
            """, (username,))
            user = cursor.fetchone()
            if user:
                password_hash, salt = user
                new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
                return new_hash == password_hash
        finally:
            conn.close()
    return False

def get_all_users():
    """Fetch all usernames from the database."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users")
            users = [row[0] for row in cursor.fetchall()]
            return users
        finally:
            conn.close()

def get_image_path(username):
    """Retrieve the image path for a specific user."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT image_path FROM users WHERE username = ?
            """, (username,))
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            conn.close()

# Ensure the database is initialized
setup_database()

if __name__ == "__main__":
    setup_database()
