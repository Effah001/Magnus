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
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/courses')
def courses():
    return render_template('courses1.html')


@app.route('/quizzes')
def quizzes():
    return render_template('quizzes.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/math')
def math_topics():
    math_topics = [
        {"name": "Algebra", "description": "Explore the fundamental concepts of algebra, including equations, polynomials, and functions."},
        {"name": "Geometry", "description": "Discover the properties and relationships of shapes, angles, and spatial structures in geometry."},
        {"name": "Calculus", "description": "Delve into the study of rates of change and accumulation, fundamental to understanding motion and change in mathematics."},
        {"name": "Trigonometry", "description": "Study relationships between side lengths and angles of triangles."},
        {"name": "Statistics", "description": "Explore the collection, analysis, interpretation, and presentation of data."},
        {"name": "Number Theory", "description": "Investigate properties and relationships of numbers, especially integers."},
        {"name": "Linear Algebra", "description": "Examine vectors, vector spaces, linear transformations, and systems of linear equations."},
        {"name": "Differential Equations", "description": "Study equations that describe the rates of change of a function."},
        {"name": "Discrete Mathematics", "description": "Explore mathematical structures that are fundamentally discrete rather than continuous."},
        {"name": "Topology", "description": "Examine properties of space that are preserved under continuous deformations, such as stretching, crumpling, and bending, but not tearing or gluing."},
        {"name": "Probability Theory", "description": "Study the mathematical framework for modeling uncertain events."},
        {"name": "Mathematical Analysis", "description": "Examine the theory of functions of a real variable and includes, among other things, the concepts of continuity, limits, derivatives, and integrals."},
        {"name": "Graph Theory", "description": "Study the mathematical structures used to model pairwise relations between objects."},
        {"name": "Numerical Analysis", "description": "Explore the algorithms and numerical methods used to solve mathematical problems."},
        {"name": "Combinatorics", "description": "Investigate counting, arrangement, and combination of objects."},
        {"name": "Mathematical Logic", "description": "Study formal systems in mathematics that consist of formal languages for formalizing mathematical statements."},
        {"name": "Game Theory", "description": "Examine mathematical models of strategic interaction among rational decision-makers."},
        {"name": "Mathematical Physics", "description": "Explore mathematical methods for solving problems in physics."},
        {"name": "Complex Analysis", "description": "Study the analysis of functions of complex numbers, including complex derivatives and integrals."},
        {"name": "Set Theory", "description": "Examine the mathematical study of collections of objects, such as numbers or functions."}
    ]
    return render_template("math.html", math_topics=math_topics)


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

                # Redirect to the home page or any other protected page
                return redirect(url_for('home'))

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
    return render_template('update1.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    if request.method == 'POST':
        # Retrieve the current user
        user = current_user

        # Delete the user from the database
        db.session.delete(user)
        db.session.commit()

        # Log out the user (optional)
        logout_user()

        # Redirect the user to the login page
        return redirect(url_for('login'))

    # Handle GET request if necessary
    return redirect(url_for('profile'))  # Redirect to profile page if accessed via GET
