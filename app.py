import random
import string

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "exam_cell_secret_key"


# ================= DATABASE =================

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll TEXT,
        name TEXT,
        branch TEXT,
        semester TEXT,
        subject TEXT,
        marks INTEGER
    )
    """)

    conn.commit()
    conn.close()


create_table()
# ================= CAPTCHA =================

def generate_captcha():

    captcha = ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=5
        )
    )

    return captcha


# ================= LOGIN =================

USERNAME = "admin"
PASSWORD = "admin123"

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        user_captcha = request.form["captcha"]


        # CAPTCHA CHECK

        if user_captcha != session.get("captcha"):

            captcha = generate_captcha()
            session["captcha"] = captcha

            return render_template(
                "login.html",
                error="Invalid CAPTCHA",
                captcha=captcha
            )



        # USERNAME PASSWORD CHECK

        if username == USERNAME and password == PASSWORD:

            session["admin"] = username

            return redirect(url_for("dashboard"))


        else:

            captcha = generate_captcha()
            session["captcha"] = captcha

            return render_template(
                "login.html",
                error="Invalid Username or Password",
                captcha=captcha
            )



    # FIRST TIME LOGIN PAGE OPEN

    captcha = generate_captcha()
    session["captcha"] = captcha


    return render_template(
        "login.html",
        captcha=captcha
    )


# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    total_students = len(students)

    passed = len([i for i in students if i["marks"] >= 33])

    failed = len([i for i in students if i["marks"] < 33])

    conn.close()

    return render_template(
        "dashboard.html",
        students=students,
        total_students=total_students,
        passed=passed,
        failed=failed
    )
# ================= ADD STUDENT =================

@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        roll = request.form["roll"]
        name = request.form["name"]
        branch = request.form["branch"]
        semester = request.form["semester"]
        subject = request.form["subject"]
        marks = request.form["marks"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students
            (roll, name, branch, semester, subject, marks)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (roll, name, branch, semester, subject, marks))

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template(
        "add_student.html"
    )


# ================= EDIT STUDENT =================

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":

        roll = request.form["roll"]
        name = request.form["name"]
        branch = request.form["branch"]
        semester = request.form["semester"]
        subject = request.form["subject"]
        marks = request.form["marks"]

        cursor.execute("""
            UPDATE students
            SET roll=?,
                name=?,
                branch=?,
                semester=?,
                subject=?,
                marks=?
            WHERE id=?
        """, (roll, name, branch, semester, subject, marks, id))

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()

    conn.close()

    return render_template(
        "edit_student.html",
        student=student
    )


# ================= DELETE STUDENT =================

@app.route("/delete/<int:id>")
def delete_student(id):

    if "admin" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


# ================= SEARCH =================

@app.route("/search", methods=["POST"])
def search():

    if "admin" not in session:
        return redirect(url_for("login"))

    keyword = request.form["keyword"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM students
        WHERE name LIKE ?
        OR roll LIKE ?
    """, ("%" + keyword + "%", "%" + keyword + "%"))

    students = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        page="dashboard",
        students=students,
        total_students=len(students),
        passed=len([x for x in students if x["marks"] >= 33]),
        failed=len([x for x in students if x["marks"] < 33])
    )


# ================= LOGOUT =================

@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect(url_for("login"))


# ================= MAIN =================

if __name__ == "__main__":
    app.run(debug=True)