import sqlite3
import bcrypt


def signup_user(name, email, password):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    try:

        cursor.execute(
            """
            INSERT INTO users
            (name, email, password)
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                hashed_password.decode()
            )
        )

        conn.commit()

        return True, "Signup successful."

    except sqlite3.IntegrityError:

        return False, "Email already exists."

    finally:

        conn.close()


def login_user(email, password):

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if not user:
        return False

    stored_hash = user[3]

    return bcrypt.checkpw(
        password.encode(),
        stored_hash.encode()
    )