import os
import os.path as op

from datetime import datetime as dt

import PIL
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
from PIL import Image
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy import select
import operator
from PIL import Image
size = 100, 100

admin = Admin()


#app = Flask(__name__)
app = Flask(__name__, static_folder='static')
#app = Flask(__name__, static_folder='static')

# set optional bootswatch theme
# see http://bootswatch.com/3/ for available swatches
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'this is a secret key '
#new line below
app.config['SQLALCHEMY_ECHO'] = True
#end of new line
db = SQLAlchemy(app)

# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'static')
try:
    os.mkdir(file_path)
except OSError:
    pass


admin.init_app(app)


class User(db.Model, UserMixin):
 id = db.Column(db.Integer, primary_key=True)
 username = db.Column(db.String(50))
 email = db.Column(db.String(120), unique=True, nullable=False)
 password = db.Column(db.String(100), nullable=False)
 #hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
 #password=hashed_password

def __repr__(self):
    return f'<User {self.username}>'


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)

def __str__(self):
    return self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Food(db.Model):
    __tablename__ = "food"
    food_id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.Unicode(64))
    food_price = db.Column(db.Numeric(10,2), nullable=False)
    food_type = db.Column(db.String(30), nullable=False)
    #new line
    path = db.Column(db.Unicode(128))
    # new line ends here

#def __repr__(self):
def __unicode__(self): #new line
    return f'<Food {self.food_name}>'


@login_manager.user_loader
def load_food(food_id):
    return Food.query.get(int(food_id))


class Order(db.Model):
    __tablename__ = "order"
    order_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.food_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    trans_option = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    food = relationship(Food, backref='foods')


def __repr__(self):
    return f'<Order {self.order_no}>'


@login_manager.user_loader
def load_order(order_no):
    return Order.query.get(int(order_no))


class Pay(db.Model):
    __tablename__ = "pay"
    pay_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_no = db.Column(db.Integer, db.ForeignKey('order.order_no'), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    cust_name = db.Column(db.String(30), nullable=False)
    cust_address = db.Column(db.String(30), nullable=False)
    cust_postcode = db.Column(db.String(30), nullable=False)
    cust_email = db.Column(db.String(30), nullable=False)
    cust_cardno = db.Column(db.String(30), nullable=False)
    card_expirydate = db.Column(db.String(30), nullable=False)
    card_cvv = db.Column(db.String(30), nullable=False)
    pay_datetime = db.Column(db.DateTime, default=dt.now)
    # pay_datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)


def __repr__(self):
    return f'<Pay {self.pay_no}>'
'''
#new funtion del_image
@listens_for(Image, 'after_delete')
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass
'''
#class FoodView(ModelView):
    #can_delete = False
   # form_columns = ["food_name", "food_price", "food_type"]
   # column_list = ["food_name", "food_price", "food_type"]


class FoodView(sqla.ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''
        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.path)))
    column_formatters = {
        'path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
                                      #thumbnail_size=((100,100),PIL.Image.Resampling.LANCZOS))
                                        #thumbnail_size = ((100, 100, True), PIL.Image.Resampling.LANCZOS))
                                                                          }



admin.add_view(ModelView(User, db.session))
admin.add_view(FoodView(Food, db.session))

@login_manager.user_loader
def load_order(pay_no):
    return Pay.query.get(int(pay_no))


@app.route('/')
@app.route('/home')
def option():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        customer = Customer.query.filter_by(username=username).first()
        if customer and bcrypt.check_password_hash(customer.password, password):
            login_user(customer)
            return redirect(url_for('welcome'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        new_customer = Customer(username=username, email=email, password=hashed_password)
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html')


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        food_id = int(request.form['food_id'])
        food_name = request.form['food_name']
        food_price = float(request.form['food_price'])
        # food_image = request.form['food_image']
        food_type = request.form['food_type']
        new_food = Food(food_id=food_id, food_name=food_name, food_price=food_price, food_type=food_type)
        db.session.add(new_food)
        db.session.commit()
        return redirect(url_for('welcome'))
    return render_template('create.html')


@app.route('/welcome')
def welcome():
    food = db.session.query(Food).all()
    # food = db.session.query(Food).first()
    return render_template('welcome.html', food=food)


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    food = db.session.query(Food).all()
    selected_menu = request.args.get('type')
    food = Food.query.filter(Food.food_name == selected_menu).first()

    test = food.food_price
    test_id = food.food_id
    return render_template("menu.html", title='Menu Details', food_name=selected_menu, food_price=test, food_id=test_id)


@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        # food_id = request.form.get("food_id")
        # food_id = request.form.get("food_id")
        food_id = request.form.get("food_id")
        food_name = request.form.get("food_name")
        food_price = float(request.form.get("food_price"))
        # food_price = request.args.get('food_price')

        quantity = request.form.get("name_of_slider")

        # quantity = 2
        # food_name = request.args.get("food_name") resulted in error
        trans_option = request.form.get("trans_option")
        total_price = float(food_price) * int(quantity)
        # total_price = int(food_price*quantity)

        new_order = Order(food_id=food_id, quantity=quantity, trans_option=trans_option, status='not collected')
        db.session.add(new_order)
        db.session.commit()
        recent = db.session.query(Order).order_by(Order.order_no.desc()).first()
        recent_order_no = recent.order_no
        # return redirect(url_for('checkout'))
        return render_template("checkout.html")


    else:
        return render_template('login.html')
        # return render_template('checkout.html')


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    print('ttt')
    if request.method == 'POST':
        print('aaa')
        recent = db.session.query(Order).order_by(Order.order_no.desc()).first()
        recent_order_no = recent.order_no
        food_id = recent.food_id

        food_name = db.session.query(Food.food_name). \
            join(Order, Order.food_id == Food.food_id). \
            filter(Order.order_no == recent_order_no). \
            first().food_name
        print(food_name)


        food_price = db.session.query(Food.food_price). \
            join(Order, Order.food_id == Food.food_id). \
            filter(Order.order_no == recent_order_no). \
            first().food_price
        print(food_price)


        #food_price = 2
        quantity = recent.quantity
        trans_option = recent.trans_option
        status = recent.status
        order_no = recent_order_no
        total_price = float(food_price) * int(quantity)
        #total_price = int(food_price * quantity)
        cust_name = request.form.get('cardname')
        cust_address = request.form.get('address')
        cust_postcode = request.form.get('postcode')
        cust_email = request.form.get('email')
        cust_cardno = request.form.get('cardnumber')
        card_expirydate = request.form.get('expdate')
        card_cvv = int(request.form.get('cvv'))

        new_pay = Pay(order_no=order_no, total_price=total_price, cust_name=cust_name, cust_address=cust_address,
                      cust_postcode=cust_postcode, cust_email=cust_email, cust_cardno=cust_cardno,
                      card_expirydate=card_expirydate, card_cvv=card_cvv)
        db.session.add(new_pay)
        db.session.commit()
        # print(new_pay.cust_name)

        pay = db.session.query(Pay).all()
        recentp = db.session.query(Pay).order_by(Pay.pay_no.desc()).first()
        recentpayno = recentp.pay_no
        return render_template("receipt.html", recentp=recentp, food_name=food_name, quantity=quantity,
                               food_price=food_price)

    elif request.method == 'GET':
        print('error')

    return render_template('menu.html')


@app.route('/orders')
def orders():
    order = db.session.query(Order).all()
    return render_template('orders.html', order=order)


@app.route('/receipt', methods=('GET', 'POST'))
def receipt():
    print('ttt')

    return render_template('login.html')


@app.route('/logout_page')
def logout_page():
    logout_user()
    return render_template('logout.html')


@app.route('/links', methods=['GET', 'POST'])
def links():
    menu = request.args.get('item')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('logout_page'))


if __name__ == "__main__":
    app_dir = op.realpath(os.path.dirname(__file__))
    #database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    with app.app_context():
        db.create_all()
    app.run(debug=True)


