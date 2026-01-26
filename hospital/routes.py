from datetime import timedelta,date,datetime
from .forms import RegistrationForm,LoginForm,AddDoctorForm
from flask import render_template, url_for,flash,redirect,request,jsonify
from hospital import app,db,bcrypt
from hospital.models import *
from flask_login import login_user ,current_user,logout_user,login_required
from sqlalchemy import func
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
@login_required
def doc(): 
    doctor = Doctor.query.filter_by(user_id=current_user.id).first() 
    print(f"Doctor: {doctor.name}, ID: {doctor.id}, Appointments count: {len(doctor.appointments)}")
    return render_template('doc_dash.html',doctor=doctor)

@app.route("/patient")
def pat():  
    patient =Patient.query.filter_by(user_id=current_user.id).first()
    departments=Department.query.all()
    appointments=Appointment.query.filter_by(patient_id=patient.id).all()
    return render_template('pat_dash.html',patient=patient,departments=departments,appointments=appointments)

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

        doctor = Doctor(name=form.name.data,specialization=form.specialization.data,experience=form.experience.data,user_id=user.id,department_id=form.department_id.data,pph=form.pph.data)
        db.session.add(doctor)
        db.session.commit()

        flash(f'Doctor {form.name.data} added successfully!')
        return redirect(url_for('admin'))
    else:
        print(form.errors)
    return render_template('doc_reg.html',form=form)

@app.route("/departments/<int:dept_id>")
def departments(dept_id):
    dept = Department.query.get_or_404(dept_id)
    doctors = Doctor.query.filter_by(department_id=dept.id)
    return render_template('departments.html',departments=dept,doctors=doctors)

@app.route("/doctor_detail/<int:doc_id>")
def doctor_detail(doc_id):
    doctor= Doctor.query.get_or_404(doc_id)
    return render_template('doctor_detail.html',doctor=doctor)

std_slots = ["8.00 - 12.00 am" , "4.00 - 9.00 pm"]

@app.route("/availability/<int:doctor_id>")
@login_required
def availability(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)

    today = date.today()

    days_data = []

    for i in range(7):
        current_date = today + timedelta(days=i)

        daily_appointments = Appointment.query.filter_by(doctor_id=doctor_id,appointment_date=current_date).all()

        slots_status = []
        for slot in std_slots:

            count = sum(1 for appt in daily_appointments if appt. time_slot == slot)

            is_available = count < doctor.pph
            slots_status.append({ 
                'time': slot,
                'available': is_available,
                'remaining' : doctor.pph - count})
        days_data.append({
            'date': current_date.strftime("%Y-%m-%d"),
            'slots': slots_status,
            'display_date': current_date.strftime("%A, %d %B %Y")})
        
    return render_template('doctor_availability.html',doctor=doctor,days=days_data)

@app.route("/book_appointment",methods=['POST'])
@login_required
def book_appointment():
    doctor_id = request.form.get('doctor_id')
    if doctor_id:
        doctor_id = int(doctor_id)
    date_str = request.form.get('x') #it is of the format YYYY-MM-DD
    print(date_str)
    time_slot = request.form.get('time_slot')

    appt_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    doctor = Doctor.query.get(doctor_id)
    patient = Patient.query.filter_by(user_id=current_user.id).first()

    if not patient:
        flash("Patient profile not found . Please complete registration .","danger")
        return redirect(url_for('home'))
    
    current_count = Appointment.query.filter_by(
        doctor_id=doctor_id , appointment_date=appt_date ,time_slot=time_slot).count()

    if current_count >= doctor.pph:
        flash("Selected slot is no longer available. Please choose a different slot.","danger")
        return redirect(url_for('availability',doctor_id=doctor_id))


    new_appt = Appointment(dept_id=doctor.department_id,
                          doctor_id=doctor_id,
                          patient_id=patient.id,
                          date=datetime.now(),
                        status = "booked",
                          time_slot=time_slot,
                          appointment_date=appt_date)
    db.session.add(new_appt)
    db.session.commit()

    
    flash("Appointment booked successfully!","success")
    return redirect(url_for('pat'))


@app.route("/delete_appointment/<int:appt_id>",methods=['POST'])
@login_required
def delete_appointment(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    current_patient =  Patient.query .filter_by(user_id=current_user.id).first()

    if not current_patient or appt.patient_id != current_patient.id:
        flash("You are not authorized to cancel this appointment.","danger")
        return redirect(url_for('pat'))
    
    db.session.delete(appt)
    db.session.commit()

    flash("Appointment cancelled successfully.","success")
    return redirect(url_for('pat'))

@app.route("/edit_profile_pat",methods=['GET','POST'])
@login_required
def edit_profile_pat():
    patient=Patient.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        patient.name = request.form.get('name')
        patient.phone = request.form.get('phone')
        patient.address = request.form.get('address')
     
    
        try:
            db.session.commit()
            flash('Profile updated successfully','success')
            return redirect(url_for('pat'))
        except :
            db.session.rollback()
            flash('Error updating profile')
    return render_template('edit_profile_pat.html',patient=patient)

@app.route("/edit_password",methods = ['GET','POST'])
@login_required
def edit_password():
    user = User.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':
        user.username = request.form.get('username')
        new_password = request.form.get('password')
        user.password = bcrypt.generate_password_hash(new_password)
        
        try:
            db.session.commit()
            flash('updated successfully')
            return redirect(url_for('pat'))
        except :
            db.session.rollback()
            flash('Error updating profile')
    return render_template('edit_password.html',user=user)

@app.route("/patient_history")
@login_required
def patient_history():
    user = User.query.filter_by(id=current_user.id).first()
    return render_template('patient_history.html',user=user)


@app.route("/update_patient_history/<int:appointment_id>",methods=["GET","POST"])
@login_required
def update_patient_history(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if request.method == 'POST':
        treatment = appointment.treatment

        if not treatment:
            treatment = Treatment(appointment_id=appointment.id)
            db.session.add(treatment)
        
        treatment.diagnosis = request.form.get("diagnosis")
        treatment.prescription = request.form.get("prescription")
        treatment.notes = request.form.get("notes")

        try:
            db.session.commit()
            flash('Patient history updated successfully')
            return redirect(url_for('doc'))
        except:
            db.session.rollback()
            flash(f'Error updating profile')
    return render_template('update_patient_history.html',appointment=appointment)
