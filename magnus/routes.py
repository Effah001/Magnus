from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import generate_password_hash
from magnus import app, db
from magnus.models import User
from magnus import bcrypt
from flask_login import login_required, current_user, logout_user


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/courses')
def courses():
    return render_template('courses.html')


@app.route('/quizzes')
def quizzes():
    return render_template('quizzes.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        # Check if the username or email already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email address already exists. Please use a different one.', 'error')
            return redirect(url_for('register'))

        # Hash the password using bcrypt before storing it in the database
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user instance
        new_user = User(username=username, password=hashed_password, email=email)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully. You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Retrieve the user from the database based on the username
        user = User.query.filter_by(username=username).first()

        if user:
            # Check if the password matches using bcrypt
            if bcrypt.check_password_hash(user.password, password):
                # Log in the user and create a session
                login_user(user)

                # Redirect to the profile page or any other protected page
                return redirect(url_for('profile'))

        # If login fails, display an error message
        flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')


@app.route('/profile/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        new_username = request.form.get('new_username')
        new_email = request.form.get('new_email')
        new_password = request.form.get('new_password')

        # Get the current user
        user = current_user

        print("Old Username:", user.username)

        # Update the user's information if new values are provided
        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email
        if new_password:
            # Hash the new password
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password = hashed_password
        
        print("New Username:", user.username)

        # Commit the changes to the database
        db.session.commit()

        # Redirect the user back to their profile page
        return redirect(url_for('profile'))

    # Render the update profile form
    return render_template('update.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))
