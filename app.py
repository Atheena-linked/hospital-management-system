from flask import Flask , render_template
from flask_bcrypt import Bcrypt
from models import db
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SECRET_KEY'] = '250f7f1559a72d593f94f8814fab426f6aca7ec16e1e437c8d2ed6380ec0df8e'

db.init_app(app)
bcrypt = Bcrypt(app)

from models import *

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)