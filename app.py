from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(32)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "students.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the students table if it does not already exist."""
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL UNIQUE,
            course TEXT NOT NULL,
            marks INTEGER NOT NULL CHECK(marks >= 0 AND marks <= 100),
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            department TEXT NOT NULL,
            attendance INTEGER NOT NULL CHECK(attendance >= 0 AND attendance <= 100)
        )
    """)
    conn.commit()
    conn.close()


def validate_student_form(form):
    """Validate all student fields and return (data, error)."""
    name = form.get("name", "").strip()
    roll_no = form.get("roll_no", "").strip()
    course = form.get("course", "").strip()
    marks_text = form.get("marks", "").strip()
    email = form.get("email", "").strip()
    phone = form.get("phone", "").strip()
    department = form.get("department", "").strip()
    attendance_text = form.get("attendance", "").strip()

    if not name:
        return None, "Name cannot be empty."
    if not roll_no:
        return None, "Roll number cannot be empty."
    if not course:
        return None, "Course cannot be empty."
    if not email:
        return None, "Email cannot be empty."
    if not phone:
        return None, "Phone cannot be empty."
    if not department:
        return None, "Department cannot be empty."

    try:
        marks = int(marks_text)
    except ValueError:
        return None, "Marks must be a number."

    if not 0 <= marks <= 100:
        return None, "Marks must be between 0 and 100."

    try:
        attendance = int(attendance_text)
    except ValueError:
        return None, "Attendance must be a number."

    if not 0 <= attendance <= 100:
        return None, "Attendance must be between 0 and 100."

    return {
        "name": name,
        "roll_no": roll_no,
        "course": course,
        "marks": marks,
        "email": email,
        "phone": phone,
        "department": department,
        "attendance": attendance,
    }, None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/students")
def students():
    conn = get_db_connection()
    students_list = conn.execute(
        "SELECT * FROM students ORDER BY id"
    ).fetchall()
    conn.close()
    return render_template("students.html", students=students_list)


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        data, error = validate_student_form(request.form)

        if error:
            flash(error, "error")
            return redirect(url_for("add_student"))

        conn = get_db_connection()

        # Give a friendly error instead of exposing a SQLite traceback.
        existing = conn.execute(
            "SELECT id FROM students WHERE roll_no = ?",
            (data["roll_no"],)
        ).fetchone()

        if existing:
            conn.close()
            flash("Roll number already exists. Roll numbers must be unique.", "error")
            return redirect(url_for("add_student"))

        conn.execute("""
            INSERT INTO students
            (name, roll_no, course, marks, email, phone, department, attendance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["name"],
            data["roll_no"],
            data["course"],
            data["marks"],
            data["email"],
            data["phone"],
            data["department"],
            data["attendance"],
        ))
        conn.commit()
        conn.close()

        flash("Student added successfully.", "success")
        return redirect(url_for("students"))

    return render_template("add_student.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    searched = False
    roll_no = ""

    if request.method in ("GET", "POST"):
        roll_no = request.values.get("roll_no", "").strip()
        searched = True

        if roll_no:
            conn = get_db_connection()
            results = conn.execute(
                "SELECT * FROM students WHERE roll_no = ?",
                (roll_no,)
            ).fetchall()
            conn.close()

    return render_template(
        "search.html",
        students=results,
        searched=searched,
        roll_no=roll_no
    )


@app.route("/update/<int:student_id>", methods=["GET", "POST"])
def update_student(student_id):
    conn = get_db_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    if student is None:
        conn.close()
        flash("Student not found.", "error")
        return redirect(url_for("students"))

    if request.method == "POST":
        data, error = validate_student_form(request.form)

        if error:
            conn.close()
            flash(error, "error")
            return redirect(url_for("update_student", student_id=student_id))

        # Make sure another student does not already use the new roll number.
        duplicate = conn.execute(
            "SELECT id FROM students WHERE roll_no = ? AND id != ?",
            (data["roll_no"], student_id)
        ).fetchone()

        if duplicate:
            conn.close()
            flash("Roll number already belongs to another student.", "error")
            return redirect(url_for("update_student", student_id=student_id))

        conn.execute("""
            UPDATE students
            SET name = ?,
                roll_no = ?,
                course = ?,
                marks = ?,
                email = ?,
                phone = ?,
                department = ?,
                attendance = ?
            WHERE id = ?
        """, (
            data["name"],
            data["roll_no"],
            data["course"],
            data["marks"],
            data["email"],
            data["phone"],
            data["department"],
            data["attendance"],
            student_id,
        ))
        conn.commit()
        conn.close()

        flash("Student updated successfully.", "success")
        return redirect(url_for("students"))

    conn.close()
    return render_template("update.html", student=student)


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )
    conn.commit()
    conn.close()

    flash("Student deleted successfully.", "success")
    return redirect(url_for("students"))


init_db()

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
