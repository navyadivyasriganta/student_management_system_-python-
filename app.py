from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "students.db"

def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                department TEXT NOT NULL,
                year TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    with get_db() as db:
        if query:
            students = db.execute("""
                SELECT * FROM students
                WHERE student_id LIKE ? OR name LIKE ? OR department LIKE ?
                ORDER BY id DESC
            """, (f"%{query}%", f"%{query}%", f"%{query}%")).fetchall()
        else:
            students = db.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
        total = db.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        departments = db.execute("SELECT COUNT(DISTINCT department) FROM students").fetchone()[0]
        first_year = db.execute("SELECT COUNT(*) FROM students WHERE year = '1st Year'").fetchone()[0]
    return render_template("index.html", students=students, query=query,
                           total=total, departments=departments, first_year=first_year)

@app.route("/add", methods=["POST"])
def add_student():
    data = {key: request.form.get(key, "").strip() for key in
            ("student_id", "name", "email", "phone", "department", "year")}
    if not all(data.values()):
        flash("Please fill in all fields.", "error")
        return redirect(url_for("index"))
    try:
        with get_db() as db:
            db.execute("""
                INSERT INTO students (student_id, name, email, phone, department, year)
                VALUES (?, ?, ?, ?, ?, ?)
            """, tuple(data.values()))
        flash("Student added successfully.", "success")
    except sqlite3.IntegrityError:
        flash("That student ID already exists. Please use a unique ID.", "error")
    return redirect(url_for("index"))

@app.route("/edit/<int:student_pk>", methods=["GET", "POST"])
def edit_student(student_pk):
    with get_db() as db:
        student = db.execute("SELECT * FROM students WHERE id = ?", (student_pk,)).fetchone()
        if student is None:
            flash("Student not found.", "error")
            return redirect(url_for("index"))
        if request.method == "POST":
            data = {key: request.form.get(key, "").strip() for key in
                    ("student_id", "name", "email", "phone", "department", "year")}
            if not all(data.values()):
                flash("Please fill in all fields.", "error")
                return render_template("edit_student.html", student=student)
            try:
                db.execute("""
                    UPDATE students SET student_id=?, name=?, email=?, phone=?,
                    department=?, year=? WHERE id=?
                """, (*data.values(), student_pk))
                flash("Student details updated successfully.", "success")
                return redirect(url_for("index"))
            except sqlite3.IntegrityError:
                flash("That student ID already exists. Please use a unique ID.", "error")
                student = dict(student)
                student.update(data)
                return render_template("edit_student.html", student=student)
    return render_template("edit_student.html", student=student)

@app.route("/delete/<int:student_pk>", methods=["POST"])
def delete_student(student_pk):
    with get_db() as db:
        db.execute("DELETE FROM students WHERE id = ?", (student_pk,))
    flash("Student record deleted.", "success")
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return {"status": "ok"}

init_db()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
