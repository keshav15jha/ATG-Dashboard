from flask import Flask, render_template, request, redirect, url_for, session
import os
import sqlite3
from werkzeug.utils import secure_filename
from database import create_users_table, add_user, get_user

app = Flask(__name__)
app.secret_key = 'your_secret_key' 
app.config['UPLOAD_FOLDER'] = 'static/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


create_users_table()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        address_line1 = request.form['address_line1']
        city = request.form['city']
        state = request.form['state']
        pincode = request.form['pincode']
        user_type = request.form['user_type']

        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')

        
        if 'profile_picture' not in request.files:
            return render_template('signup.html', error='No profile picture uploaded')

        profile_picture = request.files['profile_picture']

        
        if profile_picture and allowed_file(profile_picture.filename):
            filename = secure_filename(profile_picture.filename)

            profile_picture_path = os.path.join('uploads', filename).replace("\\", "/")

            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return render_template('signup.html', error='Invalid file format for profile picture')

        add_user(first_name, last_name, profile_picture_path, username, email, password, address_line1, city, state, pincode, user_type)

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username, password)

        if user:
            print(f"User found: {user}")

            session['user_id'] = user[0]  
            session['user_type'] = user[11]  

            print(f"Session user ID: {session['user_id']}")
            print(f"Session user type: {session['user_type']}")

            if session['user_type'] == 'Patient':
                return redirect(url_for('patient_dashboard'))
            elif session['user_type'] == 'Doctor':
                return redirect(url_for('doctor_dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/patient_dashboard')
def patient_dashboard():
    
    if 'user_id' in session and session['user_type'] == 'Patient':
        user = get_user_by_id(session['user_id'])
        print(f"User information for dashboard: {user}")
        return render_template('patient_dashboard.html', user=user)

    return redirect(url_for('login'))

@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'user_id' in session and session['user_type'] == 'Doctor':
        user = get_user_by_id(session['user_id'])
        print(f"User information for dashboard: {user}")
        return render_template('doctor_dashboard.html', user=user)

    return redirect(url_for('login'))

def get_user_by_id(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    print(f"Fetching user by ID: {user_id}")
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

if __name__ == '__main__':
    app.run(debug=True)
