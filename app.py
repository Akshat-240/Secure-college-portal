from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import view_users

app = Flask(__name__)
app.secret_key = "secret123"
DB_NAME = "college.db"

# ---------- DATABASE ----------
def get_db():
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    if not os.path.exists(DB_NAME):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                failed_attempts INTEGER DEFAULT 0,
                is_locked BOOLEAN DEFAULT 0
            )
        """)
        conn.commit()
        conn.close()
        print("Database initialized.")

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("home.html")

# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        # Validation
        if not username or not password or not role:
            return render_template("register.html", error="All fields are required")
        
        if len(username) < 3:
            return render_template("register.html", error="Username must be at least 3 characters")
        
        if len(password) < 8:
            return render_template("register.html", error="Password must be at least 8 characters")

        # Use Salted Hash (Werkzeug handles salt automatically)
        hashed_password = generate_password_hash(password)

        try:
            db = get_db()
            cur = db.cursor()
            
            # Check if username already exists
            cur.execute("SELECT username FROM users WHERE username=?", (username,))
            if cur.fetchone():
                db.close()
                return render_template("register.html", error="Username already exists. Choose a different one.")
            
            # Insert new user
            cur.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, hashed_password, role)
            )
            db.commit()
            db.close()
            
            # Update the view file automatically
            view_users.view_users()
            
            return render_template("register.html", success="Registration successful! Redirecting to login...")
        
        except sqlite3.Error as err:
            if db:
                db.close()
            return render_template("register.html", error=f"Database error: {err}")

    return render_template("register.html")

# ---------- LOGIN (WITH LOCK AFTER 3 FAILS) ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password_input = request.form["password"]

        db = get_db()
        cur = db.cursor()

        cur.execute(
            "SELECT password, role, failed_attempts, is_locked FROM users WHERE username=?",
            (username,)
        )
        user = cur.fetchone()

        if not user:
            db.close()
            return "Invalid credentials"

        db_password_hash, role, attempts, locked = user

        if locked:
            db.close()
            return "Account locked. Contact admin."

        # Verify password using secure check (handles salt)
        if check_password_hash(db_password_hash, password_input):
            # successful login
            cur.execute(
                "UPDATE users SET failed_attempts=0 WHERE username=?",
                (username,)
            )
            db.commit()
            db.close()
            
            # Update the view file automatically
            view_users.view_users()

            session["username"] = username
            session["role"] = role

            if role == "admin":
                return redirect("/admin")
            elif role == "faculty":
                return redirect("/faculty")
            else:
                return redirect("/student")

        else:
            attempts += 1

            if attempts >= 3:
                cur.execute(
                    "UPDATE users SET failed_attempts=?, is_locked=1 WHERE username=?",
                    (attempts, username)
                )
                db.commit()
                db.close()
                
                # Update the view file automatically
                view_users.view_users()
                
                return "Account locked after 3 failed attempts."

            else:
                cur.execute(
                    "UPDATE users SET failed_attempts=? WHERE username=?",
                    (attempts, username)
                )
                db.commit()
                db.close()
                
                # Update the view file automatically
                view_users.view_users()

                return f"Invalid credentials. Attempts left: {3 - attempts}"

    return render_template("login.html")

# ---------- STUDENT ----------
@app.route("/student")
def student():
    if session.get("role") != "student":
        return redirect("/login")
    return render_template("student.html")

# ---------- FACULTY ----------
@app.route("/faculty")
def faculty():
    if session.get("role") != "faculty":
        return redirect("/login")
    return render_template("faculty.html")

# ---------- ADMIN ----------
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect("/login")
    return render_template("admin.html")

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
