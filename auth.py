import sqlite3
import bcrypt
import streamlit as st


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

    login_success = bcrypt.checkpw(
        password.encode(),
        stored_hash.encode()
    )

    if login_success:

        st.session_state["logged_in"] = True
        st.session_state["user_email"] = email
        st.session_state["user_name"] = user[1]

        return True

    return False


def logout_user():

    if "logged_in" in st.session_state:
        del st.session_state["logged_in"]

    if "user_email" in st.session_state:
        del st.session_state["user_email"]

    if "user_name" in st.session_state:
        del st.session_state["user_name"]