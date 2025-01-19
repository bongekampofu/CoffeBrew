from decimal import Decimal
import os
import os.path as op
from datetime import datetime as dt
from sqlalchemy import Column, Integer, DateTime
from flask import Flask, render_template, send_from_directory, url_for, redirect, request
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

from jinja2 import TemplateNotFound  # Import TemplateNotFound exception
import logging

#for xml files
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from datetime import datetime as dt


admin = Admin()
app = Flask(__name__, static_folder='static')

#log errors
app_dir = op.realpath(os.path.dirname(__file__))
logger = logging.getLogger('app_logger')
logger.setLevel(logging.DEBUG)  # Set the logger level to DEBUG or higher

# Create a file handler and set the level to DEBUG
log_file_path = op.join(app_dir, 'app.log')
handler = logging.FileHandler(log_file_path)

# Create a formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)


@app.errorhandler(404)
def page_not_found(e):
    logger.error('Page not found: %s', e)
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error('Page not found: %s', e)
    db.session.rollback()
    return render_template('500.html'), 500

# see http://bootswatch.com/3/ for available swatches
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\Bongeka.Mpofu\\DB Browser for SQLite\\site.db'

app.config['SECRET_KEY'] = 'this is a secret key '
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
login_manager.init_app(app)
admin.init_app(app)

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


def __repr__(self):
    return f'<User {self.username}>'

class Customer(db.Model, UserMixin):
    __tablename__ = "customer"
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
    file_image = db.Column(db.String(30), nullable=False)
    cartitems = relationship("CartItem", back_populates="food")

def __unicode__(self):
    return f'<Food {self.food_name}>'

@login_manager.user_loader
def load_food(food_id):
    return Food.query.get(int(food_id))

class CartItem(db.Model):
    __tablename__='cartitem'
    cart_id = db.Column(db.Integer,primary_key=True)
    cart_name = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    # adding the foreign key
    food_id = db.Column(db.Integer, db.ForeignKey('food.food_id'), nullable=False)
    food = relationship("Food", back_populates="cartitems") #2nd backpopulates method

    # def __repr__(self):
def __unicode__(self):  # new line
        return f'<CartI'
        f'tem {self.cart_name}>'


class Order(db.Model):
    __tablename__ = "order"
    order_no = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique primary key
    food_id = db.Column(db.Integer, nullable=False)  # Correcting syntax for food_id
    quantity = db.Column(db.Integer, nullable=False)
    pay_order_no = db.Column(db.Integer, db.ForeignKey('pay.order_no'), nullable=True)  # Foreign key to Pay table

    pay_reference = db.relationship("Pay", back_populates="orders")  # Define relationship back to Pay

    def __repr__(self):
        return f'<Order {self.order_no}>'

class Pay(db.Model):
    __tablename__ = "pay"
    pay_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_no = db.Column(db.Integer, unique=True)  # Foreign key target column in Pay

    total_price = db.Column(db.Numeric(10, 2))
    cust_name = db.Column(db.String(30), nullable=False)
    cust_address = db.Column(db.String(30), nullable=False)
    cust_postcode = db.Column(db.String(30), nullable=False)
    cust_email = db.Column(db.String(30), nullable=False)
    cust_cardno = db.Column(db.String(30), nullable=False)
    card_expirydate = db.Column(db.String(30), nullable=False)
    card_cvv = db.Column(db.String(30), nullable=False)
    trans_option = db.Column(db.String(30))
    pay_datetime = db.Column(db.DateTime, default=dt.now)

    orders = db.relationship("Order", back_populates="pay_reference")  # Relationship to Order



class Rest(db.Model):
    __tablename__ = 'rest'
    rest_id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    rest_name = db.Column(db.String(80))
    address = db.Column(db.String(70))
    stars = db.Column(db.Integer())
    image = db.Column(db.String(500))

    # One-to-many relationship with Table
    #tables = db.relationship('Table', back_populates='restaurant', cascade="all, delete-orphan")
    resttables = db.relationship("Table", back_populates="rest")

class Table(db.Model):
    __tablename__ = 'table'
    table_id = db.Column(db.String(20), primary_key=True)
    rest_id = db.Column(db.Integer, db.ForeignKey('rest.rest_id'))
    table_type = db.Column(db.String(20))
    reserve_fee = db.Column(db.Numeric(10, 2))
    max_occupants = db.Column(db.Integer())
    available = db.Column(db.Boolean)

    # Back reference to Rest
    #restaurant = db.relationship('Rest', back_populates='tables')
    #rest_id = db.Column(db.ForeignKey("restaurant.id"), nullable=False)
    rest = db.relationship("Rest", back_populates="resttables")
    bookings = db.relationship("Bookings", back_populates="table")  # Relationship to Bookings

class Bookings(db.Model):
    __tablename__ = 'bookings'
    book_no = db.Column(db.Integer, autoincrement=True, primary_key=True)
    table_id = db.Column(db.String(20), db.ForeignKey('table.table_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_date_time = db.Column(db.String(20))
    total_price = db.Column(db.Numeric(10,2))
    table = db.relationship("Table", back_populates="bookings")  # relationship

class RestView(ModelView):
    can_delete = False
    form_columns = ["rest_name", "address", "stars", "image"]
    column_list = ["rest_name", "address", "stars", "image"]

class TableView(ModelView):
    can_delete = False
    form_columns = ["table_id", "rest_id", "table_type", "reserve_fee", "max_occupants", "available"]
    column_list = ["table_id", "rest_id", "table_type", "reserve_fee", "max_occupants", "available"]


admin.add_view(ModelView(User, db.session))
admin.add_view(RestView(Rest, db.session))
admin.add_view(TableView(Table, db.session))


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        customer = Customer.query.filter_by(username=username).first()
        if customer and bcrypt.check_password_hash(customer.password, password):
            #db.session["username"] = username
            login_session['username'] = username
            login_user(customer)
            return redirect(url_for('welcome'))
        else:
            #if "username" in db.session:
            if "username" in login_session:
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

        checkemail = Customer.query.filter(Customer.email == email).first()
        checkuser = Customer.query.filter(Customer.username == username).first()

        if checkemail != None:
            flash("Please register using a different email.")

            return render_template("register.html")
        elif checkuser is not None:
            flash("Username already exists !")

            return render_template("register.html")

        else:
            new_customer = Customer(username=username, email=email, password=hashed_password)
            db.session.add(new_customer)
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/welcome')
def welcome():
    if "username" in login_session:
        username = login_session['username']
        food = db.session.query(Food).all()
        #path=food.file_image
        return render_template('welcome.html', food=food)
    else:
        return redirect(url_for('login'))

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    food = db.session.query(Food).all()
    selected_menu = request.args.get('type')
    food = Food.query.filter(Food.food_name == selected_menu).first()
    price = food.food_price
    fid = food.food_id
    return render_template("menu.html", title='Menu Details', food_name=selected_menu, food_price=price, food_id=fid)


@app.route('/addfood', methods=['GET', 'POST'])
def addfood():
    if request.method == 'POST':
        food_name = request.form['food_name']
        food_price = float(request.form['food_price'])
        food_type = request.form['food_type']
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        #comment the following 2 lines
        #return path
        #return 'ok'
        new_food = Food(food_name=food_name, food_price=food_price, food_type=food_type, file_image=path)
        db.session.add(new_food)
        db.session.commit()
        return redirect(url_for('welcome'))
    return render_template('createfood.html')

@app.route('/delete_food/<int:food_id>', methods=['POST'])
def delete_food(food_id):
    # First, delete all related cart items
    CartItem.query.filter_by(food_id=food_id).delete()

    # Query the food item by ID
    food_item = Food.query.get_or_404(food_id)

    # Remove the food item from the database
    db.session.delete(food_item)
    db.session.commit()

@app.route('/addtocart', methods=['GET', 'POST'])
def addtocart():
    if request.method == 'POST':
        if "username" in login_session:
            food_id = request.form.get("food_id")
            print(food_id)
            food_name = request.form.get("food_name")
            food_price = float(request.form.get("food_price"))
            quantity = request.form.get("name_of_slider")
            print(quantity)
            total_price = float(food_price) * int(quantity)
            cart_name = "cart" + food_id
            new_cartitem = CartItem(cart_name=cart_name,quantity=quantity,food_id=food_id)
            db.session.add(new_cartitem)
            db.session.commit()
            return redirect(url_for('welcome'))


@app.route('/checkout')
def checkout():
    # Query to join CartItem with Food and retrieve necessary fields
    cartitems = db.session.query(
        CartItem.quantity,
        Food.food_name,
        Food.food_price
    ).join(Food, CartItem.food_id == Food.food_id).all()

    return render_template('checkout.html', cartitems=cartitems)


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        if "username" in login_session:
            usern = login_session['username']
            # Retrieve the latest order_no from the Pay table
            last_pay = db.session.query(Pay).order_by(Pay.order_no.desc()).first()
            new_order_no = last_pay.order_no + 1 if last_pay else 1

            orderno = new_order_no

            total_price = Decimal('0.0')
            cartitems = db.session.query(CartItem).all()
            for cartitem in cartitems:
                food_id = cartitem.food_id
                quantity = cartitem.quantity
                total_price += Decimal(cartitem.food.food_price * cartitem.quantity)

            new_order = Order(food_id=food_id, quantity=quantity, order_no=orderno, pay_order_no=orderno)
            db.session.add(new_order)
            db.session.commit()

            trans_option = request.form.get("trans_option")
            cust_name = request.form.get('cardname')
            cust_address = request.form.get('address')
            cust_postcode = request.form.get('postcode')
            cust_email = request.form.get('email')
            cust_cardno = request.form.get('cardnumber')
            card_expirydate = request.form.get('expdate')
            card_cvv = int(request.form.get('cvv'))

            new_pay = Pay(
                order_no=orderno,
                total_price=Decimal(total_price),
                cust_name=cust_name,
                cust_address=cust_address,
                cust_postcode=cust_postcode,
                cust_email=cust_email,
                cust_cardno=cust_cardno,
                card_expirydate=card_expirydate,
                card_cvv=card_cvv,
                trans_option=trans_option
            )
            db.session.add(new_pay)
            db.session.commit()

            db.session.query(CartItem).delete()
            db.session.commit()

            recentp = db.session.query(Pay).order_by(Pay.pay_no.desc()).first()
            return render_template("receipt.html", recentp=recentp)

    # For GET requests, render the payment form
    return render_template("checkout.html")  # Replace with actual payment form template

# Route to render the table booking form
@app.route('/table_booking', methods=['GET'])
def table_booking():
    return render_template('table_booking.html')

# Route to process the form submission
@app.route('/book_table', methods=['POST'])
def book_table():
    if request.method == 'POST':
        table_id = "m12"
        user_id = login_session.get('user_id')
        people = request.form.get('people')
        date = request.form.get('date')
        time = request.form.get('time')
        datetime_str = f"{date} {time}"

        table = db.session.query(Table).filter_by(table_id=table_id).first()
        #if not table:
        #    flash("Selected table does not exist.")
        #    return redirect(url_for('table_booking'))

        total_price = table.reserve_fee * Decimal(people)

        new_booking = Bookings(
            table_id=table_id,
            user_id=user_id,
            book_date_time=datetime_str,
            total_price=total_price
        )
        db.session.add(new_booking)
        db.session.commit()

        last_pay = db.session.query(Pay).order_by(Pay.order_no.desc()).first()
        # Ensure last_pay.order_no defaults to 0 if it's None
        order_no = (last_pay.order_no or 0) + 1 if last_pay else 1
        #order_no = new_order_no

        print("Redirecting to payment_table with:", total_price, order_no)

        print(type(total_price))
        print(type(order_no))

        print(total_price)
        print(order_no)
        order_no = 7
        print(order_no)

    return redirect(url_for('payment_table', total_price=total_price, order_no=order_no))



@app.route('/payment_table/<float:total_price>/<int:order_no>', methods=['GET', 'POST'])
def payment_table(total_price, order_no):
    if request.method == 'POST':
        #if "username" in login_session:

        print("this code now!!!:", order_no, total_price)
        print(type(order_no))
        print(type(total_price))

        cust_name = request.form.get('cardname')
        cust_address = request.form.get('address')
        cust_postcode = request.form.get('postcode')
        cust_email = request.form.get('email')
        cust_cardno = request.form.get('cardnumber')
        card_expirydate = request.form.get('expdate')
        card_cvv = int(request.form.get('cvv'))
        trans_option = request.form.get("trans_option")

        new_pay = Pay(
            order_no=order_no,
            total_price=total_price,
            cust_name=cust_name,
            cust_address=cust_address,
            cust_postcode=cust_postcode,
            cust_email=cust_email,
            cust_cardno=cust_cardno,
            card_expirydate=card_expirydate,
            card_cvv=card_cvv,
            trans_option=trans_option
        )

        db.session.add(new_pay)
        db.session.commit()

        recentp = db.session.query(Pay).order_by(Pay.pay_no.desc()).first()
        return render_template("receipt.html", recentp=recentp)
        print("im here")

    #total_price = request.args.get('total_price', '0.0')
    #order_no = request.args.get('order_no')
    return render_template("checkout_table.html", total_price=total_price, order_no=order_no)


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        if "username" in login_session:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            db.session.query(Customer). \
                filter(Customer.username == username). \
                update({'password': password})
            db.session.commit()
            return redirect(url_for('welcome'))
        return render_template('update.html')

@app.route('/view-orders')
def view_orders():
    file_name = "orders.xml"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

    # Ensure the file exists before attempting to serve it
    if os.path.exists(file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], file_name)
    else:
        return "No orders.xml file found.", 404

@app.route('/download-orders')
def download_orders():
    file_name = "orders.xml"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

    # Ensure the file exists before attempting to download
    if os.path.exists(file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], file_name, as_attachment=True)
    else:
        return "No orders.xml file found.", 404



@app.route('/logout')
def logout():
    #db.session.pop("username", None)
    db.session.query(CartItem).delete()
    db.session.commit()

    del login_session['username']
    logout_user()
    return redirect(url_for('login'))

#create xml files
def export_to_xml(file_name="orders.xml"):
    # Ensure the static directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

    # Query data from the database
    orders = Order.query.all()

    # Create or append to the XML file
    if os.path.exists(file_path):
        tree = ElementTree()
        tree.parse(file_path)
        root = tree.getroot()
    else:
        root = Element("Orders")

    for order in orders:
        # Add Order details
        order_elem = SubElement(root, "Order")
        SubElement(order_elem, "OrderNo").text = str(order.order_no)
        SubElement(order_elem, "FoodID").text = str(order.food_id)
        SubElement(order_elem, "Quantity").text = str(order.quantity)

        # Add Payment details if available
        if order.pay_reference:
            pay_elem = SubElement(order_elem, "Payment")
            SubElement(pay_elem, "PayNo").text = str(order.pay_reference.pay_no)
            SubElement(pay_elem, "TotalPrice").text = str(order.pay_reference.total_price)
            SubElement(pay_elem, "CustomerName").text = order.pay_reference.cust_name
            SubElement(pay_elem, "CustomerAddress").text = order.pay_reference.cust_address
            SubElement(pay_elem, "CustomerPostcode").text = order.pay_reference.cust_postcode
            SubElement(pay_elem, "CustomerEmail").text = order.pay_reference.cust_email
            SubElement(pay_elem, "TransactionOption").text = order.pay_reference.trans_option or "N/A"
            SubElement(pay_elem, "PaymentDateTime").text = order.pay_reference.pay_datetime.strftime("%Y-%m-%d %H:%M:%S")

    # Write the XML file to the static directory
    tree = ElementTree(root)
    with open(file_path, "wb") as file:
        tree.write(file, encoding="utf-8", xml_declaration=True)

    print(f"Data exported successfully to {file_path}")

#end of xml code


if __name__ == "__main__":
    app_dir = op.realpath(os.path.dirname(__file__))
    with app.app_context():
        db.create_all()
        export_to_xml()
    app.run(debug=True)
