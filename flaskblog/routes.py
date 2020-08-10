from flask import render_template, url_for, flash, redirect
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post

posts = [
    {
        'author': 'Kevin Soriano',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 1, 2020'
    },
    {
        'author': 'Thea Soriano',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 2, 2020'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title="About Page")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    print(form.errors)
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'kevin@gmail.com' and form.password.data == 'kevin':
            flash('You have been logged in!', 'success')
            print(form.data)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!', 'danger')
    return render_template('login.html', title="Login", form=form)
