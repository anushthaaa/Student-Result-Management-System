# app.py (renamed from run.py for better convention)
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login/student", methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']
        
        # validation
        if email and password:
            return redirect(url_for('home'))
        else:
            return render_template("student_login.html", error="Please fill all fields")
    
    return render_template("student_login.html")

@app.route("/register/student", methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        student_id = request.form['student_id']
        
        if name and email and password and student_id:
            # for now, redirecting to home page after registration
            return redirect(url_for('home'))
        else:
            return render_template("student_register.html", error="Please fill all fields")
    
    return render_template("student_register.html")

@app.route("/login/admin", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']
        
        if email and password:
            return redirect(url_for('home'))
        else:
            return render_template("admin_login.html", error="Please fill all fields")
    
    return render_template("admin_login.html")

if __name__ == "__main__":
    app.run(debug=True)