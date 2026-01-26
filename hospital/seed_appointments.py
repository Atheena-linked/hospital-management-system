from hospital import db, app
from hospital.models import Appointment, Doctor, Patient, Department
from datetime import datetime, timedelta, date
import random

def seed_appointments():
    with app.app_context():
        print("Seeding Appointments...")

        # 1. Fetch existing Doctors and Patients from DB to get their real IDs
        doctors = Doctor.query.all()
        patients = Patient.query.all()

        if not doctors or not patients:
            print("Error: No doctors or patients found. Please run seed_doctors.py and seed_patients.py first.")
            return

        # 2. Define Sample Data
        # We will create a mix of Past (Completed) and Future (Booked) appointments
        
        # Helper to get a doctor by name (optional, or just pick random)
        doc_house = Doctor.query.filter_by(name="Dr. Gregory House").first()
        doc_grey = Doctor.query.filter_by(name="Dr. Meredith Grey").first()
        doc_watson = Doctor.query.filter_by(name="Dr. John Watson").first()
        
        # List of appointments to create
        appointments_data = [
            {
                "patient": patients[0], # Alice
                "doctor": doc_house,
                "days_offset": -5,      # 5 days ago (Past)
                "time": "09:00 - 10:00 AM",
                "status": "Completed"
            },
            {
                "patient": patients[1], # Bob
                "doctor": doc_grey,
                "days_offset": 2,       # 2 days in future
                "time": "10:00 - 11:00 AM",
                "status": "Booked"
            },
            {
                "patient": patients[2], # Charlie
                "doctor": doc_watson,
                "days_offset": -10,     # 10 days ago (Past)
                "time": "02:00 - 03:00 PM",
                "status": "Completed"
            },
            {
                "patient": patients[3], # Diana
                "doctor": doc_house,
                "days_offset": 1,       # Tomorrow
                "time": "11:00 - 12:00 PM",
                "status": "Booked"
            },
            {
                "patient": patients[0], # Alice (Again)
                "doctor": doc_watson,
                "days_offset": 5,       # 5 days in future
                "time": "04:00 - 05:00 PM",
                "status": "Booked"
            }
        ]

        # 3. Create and Add Objects
        for data in appointments_data:
            # Calculate dates based on offset
            appt_date_obj = date.today() + timedelta(days=data['days_offset'])
            appt_datetime = datetime.combine(appt_date_obj, datetime.min.time())

            # Ensure the doctor exists (in case seed data changed)
            if data['doctor']:
                new_appt = Appointment(
                    dept_id=data['doctor'].department_id, # Auto-fill dept from doctor
                    doctor_id=data['doctor'].id,
                    patient_id=data['patient'].id,
                    appointment_date=appt_datetime, # DateTime column
                    date=appt_date_obj,             # Date column
                    time_slot=data['time'],
                    status=data['status']
                )
                db.session.add(new_appt)

        # 4. Commit
        db.session.commit()
        print(f"Successfully added {len(appointments_data)} appointments!")

if __name__ == "__main__":
    seed_appointments()