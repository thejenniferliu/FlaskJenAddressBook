from app import app
from flask import render_template, redirect, url_for, flash  
from app.forms import SignUpForm
from app.models import User

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/signup', methods = ["GET", "POST"])
def signup():
    form = SignUpForm()
    print("FORM DATA:", form.data)
    if form.validate_on_submit():
        print("Form submitted and validated!")
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(firstname, lastname, email)

        check_user = User.query.filter( (User.username == username) | (User.email == email) ).all()

        if check_user: 
            flash('A user with that email and/or username already exists.', 'danger')
            return redirect(url_for('signup'))
        new_user = User(firstname = firstname, lastname = lastname, email=email, username=username, password=password)
    
        flash(f'Thank you {new_user.username} for signing up!', 'success')

        return redirect(url_for('index'))

    return render_template('signup.html', form = form)

@app.route('/login')
def login():
    return render_template('login.html')