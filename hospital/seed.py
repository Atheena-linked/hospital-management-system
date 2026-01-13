from hospital import db, bcrypt, app
from hospital.models import User, Patient

def seed_patients():
    with app.app_context():
        # Clear existing data if you want a fresh start (Optional)
        # Patient.query.delete()
        # User.query.filter_by(role='patient').delete()

        patients_data = [
            {"name": "Alice Johnson", "age": 28, "gender": "Female", "address": "123 Maple St", "contact": "9876543210"},
            {"name": "Bob Smith", "age": 45, "gender": "Male", "address": "456 Oak Ave", "contact": "8765432109"},
            {"name": "Charlie Brown", "age": 12, "gender": "Male", "address": "789 Pine Rd", "contact": "7654321098"},
            {"name": "Diana Prince", "age": 34, "gender": "Female", "address": "321 Birch Ln", "contact": "6543210987"},
            {"name": "Edward Norton", "age": 50, "gender": "Male", "address": "654 Cedar Ct", "contact": "5432109876"}
        ]

        hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')

        for i, data in enumerate(patients_data, 1):
            username = f"pat{i}"
            
            # 1. Create the User record first
            user = User(
                username=username,
                password_hash=hashed_pw,
                role='patient'
            )
            db.session.add(user)
            db.session.flush() # This generates the user.id without committing yet

            # 2. Create the Patient record linked to that User
            patient = Patient(
                name=data['name'],
                age=data['age'],
                gender=data['gender'],
                address=data['address'],
                contact_number=data['contact'],
                user_id=user.id
            )
            db.session.add(patient)

        db.session.commit()
        print("Database seeded with 5 patients (pat1 through pat5)!")

if __name__ == "__main__":
    seed_patients()