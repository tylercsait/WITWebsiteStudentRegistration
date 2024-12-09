from flask import Flask, request, jsonify, render_template, redirect, url_for
import db_utils

app = Flask(__name__)

# Route for the register students page
@app.route('/register')
def register():
    return render_template('register.html')

# Default route for the directory page (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route for viewing all registered students
@app.route('/view-students')
def view_students():
    students = []
    try:
        with db_utils.mysql_connection() as cursor:
            cursor.execute("SELECT student_id, student_name FROM students")
            students = cursor.fetchall()
            students = [dict(student_id=row[0], student_name=row[1]) for row in students]
    except Exception as e:
        print(f"Error fetching students: {e}")
    return render_template('view_students.html', students=students)

# Route to handle student registration form submission
@app.route('/register-student', methods=['POST'])
def register_student():
    student_id = request.form['student_id']
    student_name = request.form['student_name']

    with db_utils.mysql_connection() as cursor:
        if not db_utils.__get_column_value(cursor, "students", "student_id", student_id):
            cursor.execute("INSERT INTO students (student_id, student_name) VALUES (%s, %s)", (student_id, student_name))
            print("Student information submitted successfully!")
        else:
            print("Student already exists")

    return redirect(url_for('view_students'))

# Route to handle student deletion
@app.route('/delete-student/<student_id>', methods=['POST'])
def delete_student(student_id):
    with db_utils.mysql_connection() as cursor:
        db_utils.delete_student_by_id(cursor, student_id)
    return redirect(url_for('view_students'))

# API endpoint for adding student information
@app.route('/api/students', methods=['POST'])
def api_students():
    data = request.json
    student_id = data['student_id']
    student_name = data['student_name']

    with db_utils.mysql_connection() as cursor:
        if not db_utils.__get_column_value(cursor, "students", "student_id", student_id):
            cursor.execute("INSERT INTO students (student_id, student_name) VALUES (%s, %s)", (student_id, student_name))
            print("Student information submitted successfully!")
        else:
            print("Student already exists")

    return jsonify({"message": "Student information submitted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
