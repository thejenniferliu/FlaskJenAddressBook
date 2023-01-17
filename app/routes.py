from app import app

from flask import render_template, redirect, url_for, flash, request  
from app.forms import SignUpForm, LoginForm, AddressForm
from app.models import User, Address
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/address')
def address():
    address = Address.query.all()
    return render_template('address.html', address = address)
    
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

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username, password)
        user = User.query.filter_by(username = username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"{user.username} is now logged in", "warning")
            return redirect(url_for('index'))
        else:
            flash(f"Incorrect username and/or password", 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", 'warning')
    return redirect(url_for('index'))


@app.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
    form = AddressForm()
    if form.validate_on_submit():
        print('Form Validated!')
        #get data from form
        firstname = form.firstname.data
        lastname = form.lastname.data 
        address = form.address.data 
        phone_number = form.phone_number.data
        print(address, current_user)
        #final step is create post with userid. current_user is just a proxy to rremember who that is
        #Create new post instance
        new_address = Address(firstname = firstname, lastname = lastname, address = address, phone_number = phone_number, user_id = current_user.id)
        flash(f"Congratulations {new_address.firstname}, your address has been stored", 'success')
        return redirect(url_for('index'))

    return render_template('create.html', form = form)

@app.route('/addresses/<int:address_id>')
def get_address(address_id):
    address = Address.query.get(address_id)
    if not address:
        flash(f"A post with id {address_id} does not exist", 'danger')
        return redirect(url_for('address'))
    return render_template('addy.html', address = address)

@app.route('/addresses/<address_id>/edit', methods = ["GET", "POST"])
@login_required
def edit_address(address_id):

    addressp = Address.query.get_or_404(address_id)  
    if not addressp:
        flash(f"This post with id of {address_id} does not exist", 'danger')
        return redirect(url_for('address'))
    if addressp.author != current_user:
        flash("You do not have permission to edit this post", "danger")
        return redirect(url_for('address'))
    
    form = AddressForm()

    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data 
        address = form.address.data 
        phone_number = form.phone_number.data
        addressp.update(firstname = firstname, lastname = lastname, address = address, phone_number = phone_number)
        flash(f"{addressp.address} has been updated!", "success")
        return redirect(url_for('get_address', address_id = addressp.id))

    if request.method == 'GET':
        form.firstname.data = addressp.firstname
        form.lastname.data = addressp.lastname
        form.address.data = addressp.address
        form.phone_number.data = addressp.phone_number
    return render_template('edit.html', addressp = addressp, form = form)

@app.route('/addresses/<address_id>/delete')

@login_required
def delete_address(address_id):

    address = Address.query.get_or_404(address_id)  
    if not address:
        flash(f"This post with id of {address_id} does not exist", 'danger')
        return redirect(url_for('address'))
    if address.author != current_user:
        flash("You do not have permission to edit this post", "danger")
        return redirect(url_for('address'))
    address.delete()
    flash(f"{address.address} has been deleted", "info")
    return redirect(url_for('address'))