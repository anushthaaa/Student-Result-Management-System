import os
from flask import Flask, render_template, request, redirect, url_for, session
import re
from models import Student
from dotenv import load_dotenv
import psycopg2

# load .env variables
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") # required for session

# connect to PostgreSQL using env variables
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD")
    )
    return conn



app = Flask(__name__)
app.secret_key = "supersecretkey123"  # for session

@app.route("/")
def home():
    return render_template("index.html")

def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.(com)$', email)

def is_valid_student_id(student_id):
    return re.match(r'^(ST|S)[0-9]{3,}$', student_id)

def is_valid_name(name):
    return re.match(r'^[A-Za-z]+(?: [A-Za-z]+)*$', name)

def is_valid_password(password):
    return re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$', password)



@app.route("/login/student", methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']
        
        # VALIDATION
        if not is_valid_email(email):
            return render_template("student_login.html", error="Invalid email.")
        if not is_valid_password(password):
            return render_template("student_login.html", error="Password must be at least 6 characters and should include numbers and letters.")
        
        # Connect to DB and verify student
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE email = %s AND password = %s", (email, password))
        student = cur.fetchone()
        cur.close()
        conn.close()

        if student:
            session["student_email"] = email
            return redirect(url_for('student_dashboard'))
        else:
            return render_template("student_login.html", error="Incorrect email or password.")
    
    return render_template("student_login.html")



@app.route("/register/student", methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        student_id = request.form['student_id']

        # VALIDATION
        if not is_valid_name(name):
            return render_template("student_register.html", error="Invalid name")
        if not is_valid_email(email):
            return render_template("student_register.html", error="Invalid email")
        if not is_valid_student_id(student_id):
            return render_template("student_register.html", error="Invalid student ID")
        if not is_valid_password(password):
            return render_template("student_register.html", error="Password must be at least 6 characters and include numbers and letters.")

        new_student = Student(name, email, password, student_id)
        print("Name:", new_student.name)
        print("Email:", new_student.email)
        print("ID:", new_student.student_id)
        print("Info:", new_student.display_info())

        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO students (name, email, password, student_id)
                VALUES (%s, %s, %s, %s)
            """, (name, email, password, student_id))

            conn.commit()
            cur.close()
            conn.close()

            return redirect(url_for('home')) 

        except Exception as e:
            conn.rollback()
            cur.close()
            conn.close()
            return f"❌ Error while inserting: {e}"

    return render_template("student_register.html")



@app.route("/dashboard/student")
def student_dashboard():

    email = session.get("student_email")  # get logged-in students email
    if not email:
        return redirect(url_for('student_login'))  # not logged in

    conn = get_db_connection()
    cur = conn.cursor()
    # gets student info
    cur.execute("SELECT * FROM students WHERE email = %s", (email,))
    row = cur.fetchone()

    if row:
        student = {
            "name": row[1],
            "email": row[2],
            "password": row[3],
            "student_id": row[4],
        }

        cur.close()
        conn.close()

        return render_template("student_dashboard.html", student=student)
    else:
        cur.close()
        conn.close()
        return "Student not found"



@app.route("/login/admin", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']

        if email == "admin@gmail.com" and password == "admin123":
            session['admin_email'] = email
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("admin_login.html", error="Invalid login")
        
        # # VALIDATION
        # if not is_valid_email(email):
        #     return render_template("admin_login.html", error="Invalid email.")
        # if not is_valid_password(password):
        #     return render_template("admin_login.html", error=" Password must be at least 6 characters and include numbers and letters")
        
        # if email and password:
        #     return redirect(url_for('admin_dashboard'))
        # else:
        #     return render_template("admin_login.html", error="Please fill all fields")
    
    return render_template("admin_login.html")



@app.route("/dashboard/admin")
def admin_dashboard():

    return render_template("admin_dashboard.html")


@app.route("/upload_results", methods=['GET', 'POST'])
def upload_results():
    if not session.get("admin_email"):
        return redirect(url_for('admin_login'))
    
    return render_template("upload_result.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("student_email", None)  # Remove student email from session
    session.pop("admin_email", None) # same for admin
    return redirect(url_for('home'))  # Go back to home page

if __name__ == "__main__":
    app.run(debug=True)
