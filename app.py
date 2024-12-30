from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory




app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure random key

# MySQL database connection function
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',      # MySQL server
        user='root',           # MySQL username
        password='',  # MySQL password
        database='OU_Sphere'   # Your database name
    )
    return conn

# Route to render the login page
@app.route('/')
def login_page():
    return render_template('login.html')

# Route to handle login POST request
@app.route('/login', methods=['POST'])
def login():
    # Get form data
    username = request.form['username']
    password = request.form['password']

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query user
    cursor.execute('SELECT password, role FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    # Validate user
    if user and user[0] == password:  # Plain-text password comparison
        session['username'] = username
        session['role'] = user[1]
        return redirect(url_for('dashboard'))  # Redirect to dashboard
    else:
        return "Invalid credentials. Please try again."


@app.route('/')
def home():
    # Redirect to dashboard
    return redirect(url_for('dashboard'))


# Route for dashboard (after successful login)
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login_page'))  # Redirect if not logged in

    username = session['username']
    role = session['role']

    # Define role-specific activities
    role_activities = {
        'admin': [
            {'name': 'Manage Users', 'url': '/manage_users'},
           
            {'name': 'Monitor and Generate Reports', 'url': '/generate_reports'},
            {'name': 'Handle Support Queries', 'url': '/support_queries'},
        ],
        'lecturer': [
            {'name': 'Manage Courses', 'url': '/manage_courses'},
             {'name': 'Study Groups', 'url': '/study_groups'},
            {'name': 'Facilitate Discussions', 'url': '/discussions_forum'},
            {'name': 'Host Online Classes', 'url': '/host_classes'},
            {'name': 'Manage Assignments', 'url': '/manage_assignments'},
            {'name': 'Monitor Student Progress', 'url': '/monitor_progress'},
            {'name': 'Provide Feedback', 'url': '/provide_feedback'},
            

        ],
        'student': [
            {'name': 'View Courses', 'url': '/view_courses'},
            {'name': 'Study Groups', 'url': '/study_groups'},    
            {'name': 'Participate in Discussions', 'url': '/discussions_forum'},
            {'name': 'Track Academic Progress', 'url': '/track_progress'},
            {'name': 'Engage in Gamified Learning', 'url': '/gamified_learning'},
            {'name': 'Request Peer Mentoring', 'url': '/peer_mentoring'},
            {'name': 'Request Support', 'url': '/support_queries'},
        ]
    }

    # Render the dashboard template with role-specific activities
    return render_template(
        'dashboard.html',
        username=username,
        role=role.capitalize(),
        activities=role_activities.get(role, [])
    )

# Route: Manage Users Dashboard
@app.route('/manage_users')
def manage_users():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT username, role FROM users")
    users = cursor.fetchall()
    conn.close()

    return render_template('manage_users.html', users=users)

# Route: Add User
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                       (username, password, role))
        conn.commit()
        conn.close()

        return redirect(url_for('manage_users'))

    return render_template('add_user.html')


# Route: Edit User
@app.route('/edit_user/<string:username>', methods=['GET', 'POST'])
def edit_user(username):
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        new_role = request.form['role']
        cursor.execute("UPDATE users SET role = %s WHERE username = %s", (new_role, username))
        conn.commit()
        conn.close()

        return redirect(url_for('manage_users'))

    cursor.execute("SELECT username, role FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()

    return render_template('edit_user.html', user=user)


# Route: Delete User
@app.route('/delete_user/<string:username>', methods=['POST'])
def delete_user(username):
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    conn.commit()
    conn.close()

    return redirect(url_for('manage_users'))


@app.route('/manage_courses')
def manage_courses():
    if 'username' not in session or session['role'] != 'lecturer':
        return redirect(url_for('login_page'))

    lecturer_id = session['username']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses WHERE lecturer_id = %s", (lecturer_id,))
    courses = cursor.fetchall()
    conn.close()

    return render_template('manage_courses.html', courses=courses)



@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if 'username' not in session or session['role'] != 'lecturer':
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        course_id = request.form['course_id']
        title = request.form['title']
        description = request.form['description']
        lecturer_id = session['username']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO courses (course_id, title, description, lecturer_id) VALUES (%s, %s, %s, %s)",
            (course_id, title, description, lecturer_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('manage_courses'))

    return render_template('add_course.html')


@app.route('/edit_course/<string:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    if 'username' not in session or session['role'] != 'lecturer':
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        cursor.execute(
            "UPDATE courses SET title = %s, description = %s WHERE course_id = %s",
            (title, description, course_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('manage_courses'))

    cursor.execute("SELECT * FROM courses WHERE course_id = %s", (course_id,))
    course = cursor.fetchone()
    conn.close()

    return render_template('edit_course.html', course=course)


@app.route('/delete_course/<string:course_id>', methods=['POST'])
def delete_course(course_id):
    if 'username' not in session or session['role'] != 'lecturer':
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('manage_courses'))


@app.route('/assign_students/<string:course_id>', methods=['GET', 'POST'])
def assign_students(course_id):
    if 'username' not in session or session['role'] != 'lecturer':
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        student_ids = request.form.getlist('students')

        cursor.execute("DELETE FROM enrollments WHERE course_id = %s", (course_id,))
        for student_id in student_ids:
            cursor.execute("INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)", (student_id, course_id))

        conn.commit()
        conn.close()
        return redirect(url_for('manage_courses'))

    cursor.execute("SELECT username FROM users WHERE role = 'student'")
    students = cursor.fetchall()

    cursor.execute("SELECT student_id FROM enrollments WHERE course_id = %s", (course_id,))
    enrolled_students = [row['student_id'] for row in cursor.fetchall()]

    conn.close()

    return render_template('assign_students.html', students=students, enrolled_students=enrolled_students, course_id=course_id)


@app.route('/view_enrollments/<string:course_id>')
def view_enrollments(course_id):
    if 'username' not in session or session['role'] != 'lecturer':
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch enrolled students
    cursor.execute("""
        SELECT e.student_id, u.username, u.role
        FROM enrollments e
        JOIN users u ON e.student_id = u.username
        WHERE e.course_id = %s
    """, (course_id,))
    enrolled_students = cursor.fetchall()

    conn.close()

    return render_template('view_enrollments.html', enrolled_students=enrolled_students, course_id=course_id)




@app.route('/support_queries')
def support_queries():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM support_tickets")
    tickets = cursor.fetchall()
    conn.close()

    return render_template('support_queries.html', tickets=tickets)

@app.route('/respond_ticket/<int:ticket_id>', methods=['GET', 'POST'])
def respond_ticket(ticket_id):
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        response = request.form['response']
        status = request.form['status']

        cursor.execute(
            "UPDATE support_tickets SET response = %s, status = %s WHERE ticket_id = %s",
            (response, status, ticket_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('support_queries'))

    cursor.execute("SELECT * FROM support_tickets WHERE ticket_id = %s", (ticket_id,))
    ticket = cursor.fetchone()
    conn.close()

    return render_template('respond_ticket.html', ticket=ticket)

@app.route('/submit_ticket', methods=['GET', 'POST'])
def submit_ticket():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        query = request.form['query']
        user_id = session['username']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO support_tickets (user_id, query) VALUES (%s, %s)", (user_id, query))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

    return render_template('submit_ticket.html')


UPLOAD_FOLDER = 'static/uploads'
ASSIGNMENT_FOLDER = os.path.join(UPLOAD_FOLDER, 'assignments')
SUBMISSION_FOLDER = os.path.join(UPLOAD_FOLDER, 'submissions')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 1. Lecturer: Manage Assignments
@app.route('/create_assignment', methods=['GET', 'POST'])
def create_assignment():
    if 'username' not in session or session['role'] != 'lecturer':
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        course_id = request.form['course_id']
        title = request.form['title']
        description = request.form['description']
        deadline = request.form['deadline']
        file = request.files['file']

        # Handle file upload
        file_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(ASSIGNMENT_FOLDER, filename)
            file.save(file_path)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO assignments (course_id, title, description, deadline, file_path) VALUES (%s, %s, %s, %s, %s)",
            (course_id, title, description, deadline, file_path)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('manage_assignments'))

    # Fetch courses for the dropdown
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT course_id, title FROM courses")
    courses = cursor.fetchall()
    conn.close()

    return render_template('create_assignment.html', courses=courses)

@app.route('/manage_assignments', methods=['GET', 'POST'])
def manage_assignments():
    if 'username' not in session or session['role'] != 'lecturer':
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT a.assignment_id, a.title, a.description, a.deadline, c.title AS course_title 
        FROM assignments a 
        JOIN courses c ON a.course_id = c.course_id 
        WHERE c.lecturer_id = %s
    """, (session['username'],))
    assignments = cursor.fetchall()
    conn.close()

    return render_template('manage_assignments.html', assignments=assignments)

@app.route('/delete_assignment/<int:assignment_id>', methods=['POST'])
def delete_assignment(assignment_id):
    if 'username' not in session or session['role'] != 'lecturer':
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM submissions WHERE assignment_id = %s", (assignment_id,))
    cursor.execute("DELETE FROM assignments WHERE assignment_id = %s", (assignment_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('manage_assignments'))

@app.route('/review_submissions/<int:assignment_id>', methods=['GET'])
def review_submissions(assignment_id):
    if 'username' not in session or session['role'] != 'lecturer':
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT s.submission_id, s.student_id, s.submitted_at, s.grade, s.feedback, 
               u.username AS student_name, s.file_path 
        FROM submissions s 
        JOIN users u ON s.student_id = u.username 
        WHERE s.assignment_id = %s
    """, (assignment_id,))
    submissions = cursor.fetchall()
    conn.close()

    return render_template('review_submissions.html', submissions=submissions, assignment_id=assignment_id)

@app.route('/grade_submission/<int:submission_id>', methods=['GET', 'POST'])
def grade_submission(submission_id):
    if 'username' not in session or session['role'] != 'lecturer':
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        grade = request.form['grade']
        feedback = request.form['feedback']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE submissions SET grade = %s, feedback = %s WHERE submission_id = %s
        """, (grade, feedback, submission_id))
        conn.commit()
        conn.close()

        return redirect(url_for('manage_assignments'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.*, u.username AS student_name FROM submissions s 
        JOIN users u ON s.student_id = u.username WHERE s.submission_id = %s
    """, (submission_id,))
    submission = cursor.fetchone()
    conn.close()

    return render_template('grade_submission.html', submission=submission)

# 2. Student: View Courses and Assignments
@app.route('/view_courses', methods=['GET'])
def view_courses():
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    for course in courses:
        cursor.execute(
            "SELECT * FROM enrollments WHERE student_id = %s AND course_id = %s",
            (session['username'], course['course_id'])
        )
        course['enrolled'] = cursor.fetchone() is not None

    conn.close()
    return render_template('view_courses.html', courses=courses)

@app.route('/submit_assignment/<int:assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        file = request.files['file']
        student_id = session['username']

        # Define the directory and file path
        upload_dir = os.path.join('static/uploads/submissions')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)  # Create the directory if it doesn't exist

        file_path = os.path.join(upload_dir, secure_filename(file.filename))
        file.save(file_path)  # Save the uploaded file

        # Insert submission details into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO submissions (assignment_id, student_id, file_path)
            VALUES (%s, %s, %s)
        """, (assignment_id, student_id, file_path))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    # Fetch assignment details for the form
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM assignments WHERE assignment_id = %s", (assignment_id,))
    assignment = cursor.fetchone()
    conn.close()

    return render_template('submit_assignment.html', assignment=assignment)



@app.route('/course_details/<string:course_id>')
def course_details(course_id):
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('login_page'))

    student_id = session['username']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch course details
    cursor.execute("SELECT * FROM courses WHERE course_id = %s", (course_id,))
    course = cursor.fetchone()

    # Fetch course materials
    cursor.execute("SELECT * FROM course_materials WHERE course_id = %s", (course_id,))
    materials = cursor.fetchall()

    # Fetch assignments along with grades and feedback (if submitted by the student)
    cursor.execute("""
        SELECT 
            a.assignment_id, 
            a.title, 
            a.description, 
            a.deadline, 
            s.grade, 
            s.feedback, 
            s.file_path AS submission_file, 
            s.submitted_at
        FROM assignments a
        LEFT JOIN submissions s 
            ON a.assignment_id = s.assignment_id AND s.student_id = %s
        WHERE a.course_id = %s
    """, (student_id, course_id))
    assignments = cursor.fetchall()

    conn.close()

    return render_template(
        'course_details.html',
        course=course,
        materials=materials,
        assignments=assignments
    )

@app.route('/download_file/<path:file_path>')
def download_file(file_path):
    try:
        # Construct the directory path for file downloads
        directory = os.path.join(app.root_path, 'static/uploads')
        return send_from_directory(directory, file_path, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404





@app.route('/study_groups', methods=['GET'])
def study_groups():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch all study groups
    cursor.execute("""
        SELECT sg.group_id, sg.group_name, sg.description, sg.whiteboard_url, sg.document_url, 
               c.title AS course_name, u.username AS creator
        FROM study_groups sg
        JOIN courses c ON sg.course_id = c.course_id
        JOIN users u ON sg.creator_id = u.username
    """)
    study_groups = cursor.fetchall()

    # Fetch groups the user is a member of
    cursor.execute("""
        SELECT group_id, role FROM study_group_members WHERE user_id = %s
    """, (session['username'],))
    user_groups = {row['group_id']: row['role'] for row in cursor.fetchall()}

    conn.close()
    return render_template('study_groups.html', study_groups=study_groups, user_groups=user_groups)

@app.route('/create_study_group', methods=['GET', 'POST'])
def create_study_group():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        group_name = request.form['group_name']
        course_id = request.form['course_id']
        description = request.form['description']
        whiteboard_url = request.form.get('whiteboard_url', '')
        document_url = request.form.get('document_url', '')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO study_groups (group_name, course_id, description, creator_id, whiteboard_url, document_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (group_name, course_id, description, session['username'], whiteboard_url, document_url))
        conn.commit()

        # Automatically add creator as a member
        group_id = cursor.lastrowid
        cursor.execute("""
            INSERT INTO study_group_members (group_id, user_id, role)
            VALUES (%s, %s, %s)
        """, (group_id, session['username'], 'lecturer' if session['role'] == 'lecturer' else 'student'))

        conn.commit()
        conn.close()

        return redirect(url_for('study_groups'))

    # Fetch courses for dropdown
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT course_id, title FROM courses")
    courses = cursor.fetchall()
    conn.close()

    return render_template('create_study_group.html', courses=courses)

@app.route('/join_study_group/<int:group_id>', methods=['POST'])
def join_study_group(group_id):
    if 'username' not in session:
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO study_group_members (group_id, user_id, role)
        VALUES (%s, %s, %s)
    """, (group_id, session['username'], 'lecturer' if session['role'] == 'lecturer' else 'student'))
    conn.commit()
    conn.close()

    return redirect(url_for('study_groups'))



@app.route('/discussions_forum')
def discussions_forum():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch all discussions
    cursor.execute("""
        SELECT d.discussion_id, d.title, d.question, d.creator, d.created_at, u.role AS creator_role
        FROM discussions d
        JOIN users u ON d.creator = u.username
        ORDER BY d.created_at DESC
    """)
    discussions = cursor.fetchall()
    conn.close()

    return render_template('view_discussions.html', discussions=discussions)

@app.route('/create_discussion', methods=['GET', 'POST'])
def create_discussion():
    if 'username' not in session:
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        title = request.form['title']
        question = request.form['question']
        creator = session['username']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO discussions (title, question, creator)
            VALUES (%s, %s, %s)
        """, (title, question, creator))
        conn.commit()
        conn.close()

        return redirect(url_for('discussions_forum'))

    return render_template('create_discussion.html')


@app.route('/discussion/<int:discussion_id>', methods=['GET', 'POST'])
def discussion_details(discussion_id):
    if 'username' not in session:
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch discussion details
    cursor.execute("SELECT * FROM discussions WHERE discussion_id = %s", (discussion_id,))
    discussion = cursor.fetchone()

    # Fetch replies
    cursor.execute("""
        SELECT r.reply_id, r.reply_text, r.replied_at, r.replier
        FROM replies r
        WHERE r.discussion_id = %s
        ORDER BY r.replied_at ASC
    """, (discussion_id,))
    replies = cursor.fetchall()

    if request.method == 'POST':
        reply_text = request.form['reply']
        replier = session['username']

        # Insert new reply
        cursor.execute("""
            INSERT INTO replies (discussion_id, replier, reply_text)
            VALUES (%s, %s, %s)
        """, (discussion_id, replier, reply_text))
        conn.commit()

        return redirect(url_for('discussion_details', discussion_id=discussion_id))

    conn.close()
    return render_template('discussion_details.html', discussion=discussion, replies=replies)

@app.route('/edit_discussion/<int:discussion_id>', methods=['GET', 'POST'])
def edit_discussion(discussion_id):
    if 'username' not in session:
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        question = request.form['question']

        cursor.execute("""
            UPDATE discussions
            SET title = %s, question = %s
            WHERE discussion_id = %s AND creator = %s
        """, (title, question, discussion_id, session['username']))
        conn.commit()
        conn.close()

        return redirect(url_for('discussions_forum'))

    cursor.execute("SELECT * FROM discussions WHERE discussion_id = %s", (discussion_id,))
    discussion = cursor.fetchone()
    conn.close()

    return render_template('edit_discussion.html', discussion=discussion)

@app.route('/delete_discussion/<int:discussion_id>', methods=['POST'])
def delete_discussion(discussion_id):
    if 'username' not in session:
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete replies first
    cursor.execute("DELETE FROM replies WHERE discussion_id = %s", (discussion_id,))
    # Delete discussion
    cursor.execute("DELETE FROM discussions WHERE discussion_id = %s AND creator = %s",
                   (discussion_id, session['username']))
    conn.commit()
    conn.close()

    return redirect(url_for('discussions_forum'))







@app.route('/<path:path>')
def catch_all(path):
    return f"Path requested: {path}", 404


@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run(debug=True)
