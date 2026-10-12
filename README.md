# Student Management System

A beginner-friendly student record management web app built with Python, Flask, SQLite, HTML, and CSS.

## Features
- Add student records with ID, name, email, phone, department, and year.
- View all records and search by student ID, name, or department.
- Edit and delete student records.
- Dashboard statistics for total students, departments, and first-year students.
- SQLite persistence: records remain stored between app restarts.
- Responsive layout for phones, tablets, and desktops.
- Form validation and success/error messages.

## Requirements
- Python 3.10 or newer
- pip

## Run locally
1. Extract the ZIP file.
2. Open a terminal in the `student_management_system` folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the app:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5000` in your browser.

The `students.db` SQLite database is created automatically when the app starts.

## Project structure
```text
student_management_system/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   └── edit_student.html
└── static/
    └── style.css
```

## Notes
- This is an educational project prototype, not a production student information system.
- Before public deployment, change the Flask secret key, enable production settings, and add authentication/authorization.
