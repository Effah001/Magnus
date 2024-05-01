from flask import render_template
from magnus import app


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

