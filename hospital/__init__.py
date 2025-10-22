from flask import Flask,render_template,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///hospital.db'
app.config['SECRET_KEY'] = '250f7f1559a72d593f94f8814fab426f6aca7ec16e1e437c8d2ed6380ec0df8e'
db=SQLAlchemy()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
db.init_app(app)


from . import routes
from . import models
from hospital.models import User

def create_admin():
    admin_username = 'admin'
    admin_password = 'admin123'
    admin_role = 'admin'

    existing = User.query.filter_by(username=admin_username).first()

    if not existing:
        hashed = bcrypt.generate_password_hash(admin_password).decode('utf-8')
        admin = User(username=admin_username,password_hash=hashed,role=admin_role)
        db.session.add(admin)
        db.session.commit()
        print("#admin user created")
    else:
        print("admin user already exists")

with app.app_context():
    db.create_all()
    create_admin()