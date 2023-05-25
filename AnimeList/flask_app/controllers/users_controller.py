from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
from flask_app.models.friendship_model import Friendship

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route("/users/register", methods=["POST"])
def register():
    if not User.validate_data(request.form):
        return redirect('/')
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password' : hashed_pass,
        'confirm_password' : hashed_pass
    }
    logged_user_id = User.create(data)
    session['user_id'] = logged_user_id
    return redirect('/dashboard')

@app.route('/users/login', methods=['POST'])
def loging_user():
    potential_user = User.get_by_email({'email': request.form['email']})
    if not potential_user:
        flash ('Invalid credentials', 'login')
        print('User Not Found')
        return redirect ('/')
    if not bcrypt.check_password_hash(potential_user.password, request.form['password']):
        flash ('Invalid credentials', 'login')
        print ('Invalid Password')
        return redirect ('/')
    session['user_id'] = potential_user.id
    return redirect ('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    logged_user = User.get_by_id({'id': session['user_id']})
    friends = Friendship.get_all_friends({'id': session['user_id']})
    return render_template('dashboard.html', logged_user = logged_user, friends = friends)

@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/')

