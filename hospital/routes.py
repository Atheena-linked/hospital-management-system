from .forms import RegistrationForm,LoginForm
from flask import render_template, url_for,flash,redirect
from hospital import app


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register",methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for{form.username.data}!')
        return redirect(url_for('home'))
    else:
        print(form.errors)

    return render_template('register.html',title='register',form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html',title='Login',form=form)
