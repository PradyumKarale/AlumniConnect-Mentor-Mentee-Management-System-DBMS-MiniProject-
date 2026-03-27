from flask import Flask, render_template, request, redirect, session, flash
from flask import session
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = "secret123"
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root1",
    database="alumni_connect"
)

cursor = db.cursor()

# HOME
@app.route('/')
def home():
    return redirect('/login')

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        role = request.form['role']
        skills_input = request.form['skills']

        # insert user
        query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
        try:
         cursor.execute(query, (name, email, hashed_password, role))
         db.commit()
        except Exception as e:
         return "Email already exists! Try logging in."

        user_id = cursor.lastrowid

        # handle skills
        skills_list = skills_input.split(',')

        for skill in skills_list:
            skill = skill.strip()

            # check if skill exists
            cursor.execute("SELECT skill_id FROM skills WHERE skill_name=%s", (skill,))
            result = cursor.fetchone()

            if result:
                skill_id = result[0]
            else:
                cursor.execute("INSERT INTO skills (skill_name) VALUES (%s)", (skill,))
                db.commit()
                skill_id = cursor.lastrowid

            # insert into user_skills
            cursor.execute("INSERT INTO user_skills (user_id, skill_id) VALUES (%s, %s)", (user_id, skill_id))
            db.commit()

        flash("Registered successfully! Please login.", "success")
        return redirect('/login')

    return render_template('register.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        query = "SELECT * FROM users WHERE email=%s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
          session['user_id'] = user[0]
          session['role'] = user[4]
          if user[4] == 'student':
            return redirect('/student_dashboard')
          else:
            return redirect('/alumni_dashboard')
        else:
          flash("Invalid credentials!", "danger")
          return redirect('/login')

    return render_template('login.html')

# STUDENT DASHBOARD
@app.route('/student_dashboard')
def student_dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    if session.get('role') != 'student':
        return "Access denied!"

    skill = request.args.get('skill')

    if skill:
        query = """
        SELECT u.user_id, u.name, u.email, GROUP_CONCAT(s.skill_name)
        FROM users u
        JOIN user_skills us ON u.user_id = us.user_id
        JOIN skills s ON us.skill_id = s.skill_id
        WHERE u.role = 'alumni' AND s.skill_name LIKE %s
        GROUP BY u.user_id
        """
        cursor.execute(query, ('%' + skill + '%',))
    else:
        query = """
        SELECT u.user_id, u.name, u.email, GROUP_CONCAT(s.skill_name)
        FROM users u
        LEFT JOIN user_skills us ON u.user_id = us.user_id
        LEFT JOIN skills s ON us.skill_id = s.skill_id
        WHERE u.role = 'alumni'
        GROUP BY u.user_id
        """
        cursor.execute(query)

    alumni_list = cursor.fetchall()

    return render_template('student_dashboard.html',
                       alumni_list=alumni_list,
                       page_title="Student Dashboard")
#Send Request

@app.route('/send_request', methods=['POST'])
def send_request():
    alumni_id = request.form['alumni_id']

    
    student_id = session['user_id']

    query = "INSERT INTO requests (student_id, alumni_id, status) VALUES (%s, %s, 'pending')"
    cursor.execute(query, (student_id, alumni_id))
    db.commit()

    flash("Request Sent Successfully!", "success")
    return redirect('/student_dashboard')

# alumni dashbord

@app.route('/alumni_dashboard')
def alumni_dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    if session.get('role') != 'alumni':
        return "Access denied!"

    alumni_id = session['user_id']

    query = "SELECT * FROM requests WHERE alumni_id=%s"
    cursor.execute(query, (alumni_id,))
    requests_data = cursor.fetchall()

    return render_template('alumni_dashboard.html',
                       requests=requests_data,
                       page_title="Alumni Dashboard")

#update request status

@app.route('/update_request', methods=['POST'])
def update_request():
    if 'user_id' not in session:
        return redirect('/login')

    request_id = request.form['request_id']
    action = request.form['action']

    try:
        # 1. CHECK CURRENT STATUS FIRST
        cursor.execute("SELECT status FROM requests WHERE request_id=%s", (request_id,))
        result = cursor.fetchone()

        if not result:
            flash("Request not found!", "danger")
            return redirect('/alumni_dashboard')

        current_status = result[0]

        # 2. PREVENT DUPLICATE ACTION
        if current_status != 'pending':
            flash("Action already completed!", "warning")
            return redirect('/alumni_dashboard')

        # 3. UPDATE STATUS
        cursor.execute(
            "UPDATE requests SET status=%s WHERE request_id=%s",
            (action, request_id)
        )

        # 4. CREATE SESSION ONLY IF APPROVED
        if action == "approved":
            cursor.execute(
                "INSERT INTO sessions (request_id, date, time, status) VALUES (%s, CURDATE(), CURTIME(), 'scheduled')",
                (request_id,)
            )

        # 5. COMMIT
        db.commit()

        flash("Request processed successfully!", "success")

    except Exception as e:
        db.rollback()
        flash(str(e), "danger")

    return redirect('/alumni_dashboard')
    
# View Sessions

@app.route('/sessions')
def view_sessions():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    role = session['role']

    if role == 'student':
        query = """
         SELECT s.session_id, u.name, s.date, s.time, f.rating, f.comment
         FROM sessions s
         JOIN requests r ON s.request_id = r.request_id
         JOIN users u ON r.alumni_id = u.user_id
         LEFT JOIN feedback f ON s.session_id = f.session_id
         WHERE r.student_id = %s
         """
    else:
        query = """
         SELECT s.session_id, u.name, s.date, s.time, f.rating, f.comment
         FROM sessions s
         JOIN requests r ON s.request_id = r.request_id
         JOIN users u ON r.student_id = u.user_id
         LEFT JOIN feedback f ON s.session_id = f.session_id
         WHERE r.alumni_id = %s
         """

    cursor.execute(query, (user_id,))
    sessions = cursor.fetchall()

    return render_template('sessions.html',
                       sessions=sessions,
                       role=role,
                       page_title="Your Sessions")

#feedback

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    session_id = request.form['session_id']
    rating = request.form['rating']
    comment = request.form['comment']

    query = "INSERT INTO feedback (session_id, rating, comment) VALUES (%s, %s, %s)"
    cursor.execute(query, (session_id, rating, comment))
    db.commit()

    flash("Feedback submitted successfully!", "success")
    return redirect('/sessions')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)