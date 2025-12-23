from .forms import RegistrationForm,LoginForm,AddDoctorForm
from flask import render_template, url_for,flash,redirect
from hospital import app,db,bcrypt
from hospital.models import *
from flask_login import login_user ,current_user,logout_user,login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,password_hash=hashed_password,role='patient')
        db.session.add(user)
        db.session.commit()

        patient = Patient(name=form.name.data,age=form.age.data,address=form.address.data,contact_number=form.contact_number.data,gender=form.gender.data,user_id=user.id) 
        db.session.add(patient)
        db.session.commit()
        flash(f'Account created for {form.username.data}!You can now log in')
        return redirect(url_for('login'))
    else:
        print(form.errors)

    return render_template('register.html',title='register',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role=='admin':
            return redirect(url_for('admin'))
        elif current_user.role=='doctor':
            return redirect(url_for('doc'))
        else:
            return redirect(url_for('pat'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash,form.password.data):
            login_user(user)
            if user.role=='admin':
                return redirect(url_for('admin'))
            elif user.role=='doctor':
                return redirect(url_for('doc'))    
            else:
                return redirect(url_for('pat'))

        else:
            flash('Login Unsuccessful. Please check username and password')
        

    return render_template('login.html',title='Login',form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/admin")
def admin():
    d_count =  Doctor.query.count()
    p_count = Patient.query.count()
    return render_template('admin_dash.html',dcount = d_count,pcount=p_count)

@app.route("/doctor")
def doc():  
    return render_template('doc_dash.html')

@app.route("/patient")
def pat():  
    return render_template('pat_dash.html')

@app.route("/add_doc",methods=['GET','POST'])
@login_required

def add_doc():
    if current_user.role != 'admin':
        flash('you are not authorized to perform this action','danger')
        return redirect(url_for('home'))
    form = AddDoctorForm()
    # form.department_id.choices = [(d.id,d.name) for d in Department.query.all()]
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=form.username.data,password_hash=hashed_password,role='doctor')
        db.session.add(user)
        db.session.commit()

        doctor = Doctor(name=form.name.data,specialization=form.specialization.data,experience=form.experience.data,user_id=user.id,department_id=form.department_id.data)
        db.session.add(doctor)
        db.session.commit()

        flash(f'Doctor {form.name.data} added successfully!')
        return redirect(url_for('admin'))
    else:
        print(form.errors)
    return render_template('doc_reg.html',form=form)
