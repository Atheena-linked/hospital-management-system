from flask import Flask,render_template,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///hospital.db'
app.config['SECRET_KEY'] = '250f7f1559a72d593f94f8814fab426f6aca7ec16e1e437c8d2ed6380ec0df8e'
db=SQLAlchemy()
db.init_app(app)
from . import routes
from . import models