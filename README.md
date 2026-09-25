# Student Management System

A small Flask and SQLite web application for managing student records. It supports adding, viewing, searching, editing, and deleting students, with validation for unique roll numbers, marks, and attendance.

## Features

- Add student details: name, roll number, course, marks, email, phone, department, and attendance.
- View all student records.
- Search by roll number.
- Edit or delete a student record.
- Validate required fields, unique roll numbers, and marks/attendance from 0 to 100.

## Technology

- Python 3
- Flask
- SQLite
- HTML and CSS

## Project files

- `app.py` — Flask routes, validation, and SQLite access.
- `templates/` — home, add, list, search, and update pages.
- `static/style.css` — shared page styling.
- `requirements.txt` — Python dependencies.

## Install and run (Windows PowerShell)

1. Install Python 3 and open PowerShell in this project folder.
2. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Start the app:

   ```powershell
   python app.py
   ```

5. Open `http://127.0.0.1:5000` in your browser. The SQLite database is created beside `app.py` on first run.

For a deployed environment, set a private `FLASK_SECRET_KEY` environment variable. Do not commit secrets, a database containing real personal information, or the report PDF with student identity details. The `.gitignore` file excludes local database, environment files, and PDFs. Submit the report PDF separately through the VITyarthi portal.

## Manual validation steps

1. Add a student with all fields and confirm the record appears in Student Records.
2. Try an existing roll number and confirm the duplicate is rejected.
3. Search with a known roll number and with an unknown one.
4. Edit a student's details and confirm the updated values appear.
5. Delete a test record and confirm it no longer appears.
6. Try marks or attendance outside 0–100 and confirm validation rejects the submission.

## Main workflow

Home → Add Student → Validate and save to SQLite → View/Search → Edit or Delete.
