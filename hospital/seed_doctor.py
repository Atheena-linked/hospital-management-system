from hospital import db, bcrypt, app
from hospital.models import User, Doctor, Department

def seed_doctors_and_depts():
    with app.app_context():
        # 1. Create Departments
        depts = [
            Department(name="Cardiology"),
            Department(name="Neurology"),
            Department(name="Pediatrics")
        ]
        db.session.add_all(depts)
        db.session.flush()  # To get dept IDs

        # 2. Doctor Data
        # Format: (Name, Dept_ID, Exp, Specialization, PPH, Username)
        doctors_info = [
            ("Dr. Gregory House", depts[1].id, 20, "Diagnostic Medicine", 2, "doc1"),
            ("Dr. Meredith Grey", depts[0].id, 12, "General Surgery", 4, "doc2"),
            ("Dr. Shaun Murphy", depts[1].id, 5, "Autistic Savant Surgery", 3, "doc3"),
            ("Dr. John Watson", depts[2].id, 15, "General Practice", 5, "doc4")
        ]

        hashed_pw = bcrypt.generate_password_hash('doctor123').decode('utf-8')

        for name, d_id, exp, spec, pph, uname in doctors_info:
            # Create User entry for login
            user = User(username=uname, password_hash=hashed_pw, role='doctor')
            db.session.add(user)
            db.session.flush()

            # Create Doctor entry
            doc = Doctor(
                name=name,
                department_id=d_id,
                experience=exp,
                specialization=spec,
                pph=pph,
                user_id=user.id,
                description=f"Specialist in {spec} with {exp} years of experience."
            )
            db.session.add(doc)

        db.session.commit()
        print("Departments and Doctors seeded successfully!")

if __name__ == "__main__":
    seed_doctors_and_depts()