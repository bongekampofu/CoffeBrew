from decimal import Decimal
import os
import os.path as op
from datetime import datetime as dt
from sqlalchemy import Column, Integer, DateTime
from flask import Flask, render_template, url_for, redirect, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.event import listens_for
from markupsafe import Markup
from flask_admin import Admin, form
from flask_admin.form import rules
from flask_admin.contrib import sqla, rediscli
from flask import session as login_session
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy import select
from sqlalchemy import select
import operator
from werkzeug.utils import secure_filename
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from sqlalchemy import update
from wtforms import PasswordField
#new imports
from sqlalchemy.ext.hybrid import hybrid_property

from flask import Flask, request, redirect, url_for, render_template
import os
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'path/to/upload/folder'  # Set your upload folder path
DATABASE = 'yourdatabase.db'  # Update with your database name

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows us to return rows as dictionaries
    return conn

@app.route('/addfood', methods=['GET', 'POST'])
def addfood():
    if request.method == 'POST':
        food_name = request.form['food_name']
        food_price = float(request.form['food_price'])
        food_type = request.form['food_type']

        if 'file1' not in request.files:
            return 'There is no file1 in form!', 400  # Return a 400 Bad Request

        file1 = request.files['file1']
        if file1.filename == '':
            return 'No selected file!', 400  # Return if no file is selected

        # Save the file
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)

        # Insert the new food record into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO food (food_name, food_price, food_type, file_image) VALUES (?, ?, ?, ?)',
                       (food_name, food_price, food_type, path))
        conn.commit()
        conn.close()

        return redirect(url_for('welcome'))

    return render_template('createfood.html')

@app.route('/welcome')
def welcome():
    return 'Food added successfully!'  # Replace with your welcome view logic


if __name__ == "__main__":
    app_dir = op.realpath(os.path.dirname(__file__))
    with app.app_context():
        db.create_all()
    app.run(debug=True)
