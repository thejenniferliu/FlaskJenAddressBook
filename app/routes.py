from app import app


from flask import render_template, redirect, url_for, flash  
from app.forms import SignUpForm

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
        print(firstname, lastname, email, username, password)

        if username == 'jenniferl':
            flash('That user arleady exists', 'danger')
            return redirect(url_for('signup'))
        flash(f"Welcome {firstname} {lastname}, you're signed up!", 'success')
        return redirect(url_for('index'))

    return render_template('signup.html', form = form)

@app.route('/login')
def login():
    return render_template('login.html')