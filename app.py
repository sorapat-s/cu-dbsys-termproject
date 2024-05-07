from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,Image
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import HexColor
from reportlab.platypus import PageTemplate, BaseDocTemplate
from io import BytesIO
from flask import send_file


from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:Ton23102546@localhost/postgres'
db = SQLAlchemy(app)

customer_attrb = ["customer_id", "firstname", "lastname", "national_id",
                  "passport", "date_of_birth", "gender", "email", "password"]


class Data(db.Model):
    __tablename__ = 'test'
    test_id = db.Column(db.Integer, primary_key=True)
    inp1 = db.Column(db.String(120))
    inp2 = db.Column(db.Integer())

    def __init__(self, inp1, inp2):
        self.inp1 = inp1
        self.inp2 = inp2


class User(db.Model):
    __tablename__ = 'test_basic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    age = db.Column(db.Integer, index=True)
    address = db.Column(db.String(256))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'address': self.address,
            'phone': self.phone,
            'email': self.email
        }


class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    firstname = db.Column(db.String(50), index=True)
    lastname = db.Column(db.String(50), index=True)
    national_id = db.Column(db.String(13))
    passport = db.Column(db.String(50))
    date_of_birth = db.Column(db.DateTime())
    gender = db.Column(db.String(1))
    email = db.Column(db.String(50))
    password = db.Column(db.String(20))

    def __init__(self, customer_id, firstname, lastname, national_id, passport, date_of_birth, gender, email, password):
        self.customer_id = customer_id
        self.firstname = firstname
        self.lastname = lastname
        self.national_id = national_id
        self.passport = passport
        self.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d')
        self.gender = gender
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'national_id': self.national_id,
            'passport': self.passport,
            'date_of_birth': self.date_of_birth.strftime("%d %b %Y"),
            'gender': self.gender,
            'email': self.email,
            'password': self.password
        }
    
class Trip(db.Model):
    __tablename__ = 'trip'
    trip_id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    tour_program_id = db.Column(db.Integer, foreign_key = True)
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    number_of_customer = db.Column(db.Integer)
    reservation_start = db.Column(db.DateTime())
    reservation_end = db.Column(db.DateTime())
    price = db.Column(db.Integer)

    def __init__(self, trip_id, tour_program_id, start_date, end_date, number_of_customer, reservation_start, reservation_end, price):
        self.trip_id = trip_id
        self.tour_program_id = tour_program_id
        self.start_date = datetime.strftime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strftime(end_date, '%Y-%m-%d')
        self.number_of_customer = number_of_customer
        self.reservation_start = datetime.strftime(reservation_start, '%Y-%m-%d')
        self.reservation_end = datetime.strptime(reservation_end, '%Y-%m-%d')
        self.price = price

    def to_dict(self):
        return {
            'trip_id' : self.trip_id,
            'tour_program_id' : self.tour_program_id,
            'start_date' : self.start_date.strftime('%Y-%m-%d'),
            'end_date' : self.end_date.strftime('%Y-%m-%d'),
            'number_of_customer' : self.number_of_customer,
            'reservation_start' : self.reservation_start.strftime('%Y-%m-%d'),
            'reservation_end' : self.reservation_end.strftime('%Y-%m-%d'),
            'price' : self.price
        }    

class CustomerPaymentMethod(db.Model):
    __tablename__ = 'customer_payment_method'
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    card_number = db.Column(db.String(30), primary_key=True)
    security_code = db.Column(db.String(3), nullable=False)
    expiry_date = db.Column(db.String(5), nullable=False)

    def __init__(self, customer_id, card_number, security_code, expiry_date):
        self.customer_id = customer_id
        self.card_number = card_number
        self.security_code = security_code
        self.expiry_date = expiry_date

    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'card_number': self.card_number,
            'security_code': self.security_code,
            'expiry_date': self.expiry_date
        }

class MembershipTier(db.Model):
    __tablename__ = 'membership_tier'
    tier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tier_discount = db.Column(db.Integer, nullable=False)
    tier_fee = db.Column(db.Integer, nullable=False)
    tier_benefit = db.Column(db.Text, nullable=False)

    def __init__(self, tier_discount, tier_fee, tier_benefit):
        self.tier_discount = tier_discount
        self.tier_fee = tier_fee
        self.tier_benefit = tier_benefit

    def to_dict(self):
        return {
            'tier_id': self.tier_id,
            'tier_discount': self.tier_discount,
            'tier_fee': self.tier_fee,
            'tier_benefit': self.tier_benefit
        }

class Promotion(db.Model):
    __tablename__ = 'promotion'
    promotion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    promotion_name = db.Column(db.String(50), nullable=False)
    promotion_banner = db.Column(db.Text, nullable=False)
    applicable_trip = db.Column(db.ARRAY(db.Integer), nullable=False)
    promotion_status = db.Column(db.Boolean, nullable=False)

    def __init__(self, promotion_name, promotion_banner, applicable_trip, promotion_status):
        self.promotion_name = promotion_name
        self.promotion_banner = promotion_banner
        self.applicable_trip = applicable_trip
        self.promotion_status = promotion_status

    def to_dict(self):
        return {
            'promotion_id': self.promotion_id,
            'promotion_name': self.promotion_name,
            'promotion_banner': self.promotion_banner,
            'applicable_trip': self.applicable_trip,
            'promotion_status': self.promotion_status
        }
class CustomerTrip(db.Model):
    __tablename__ = 'customer_trip'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.trip_id'), primary_key=True)
    payment_status = db.Column(db.Boolean, nullable=False)
    payment_due = db.Column(db.DateTime, nullable=False)

    def __init__(self, customer_id, trip_id, payment_status, payment_due):
        self.customer_id = customer_id
        self.trip_id = trip_id
        self.payment_status = payment_status
        self.payment_due = payment_due

    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'trip_id': self.trip_id,
            'payment_status': self.payment_status,
            'payment_due': self.payment_due.strftime('%Y-%m-%d %H:%M:%S')
        }

class TourProgram(db.Model):
    __tablename__ = 'tour_program'
    tour_program_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tour_program_name = db.Column(db.String(50), nullable=False)
    max_number_of_customer = db.Column(db.Integer, nullable=False)
    destination_city = db.Column(db.String(50), nullable=False)
    destination_country = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    min_price = db.Column(db.Integer, nullable=False)
    max_price = db.Column(db.Integer, nullable=False)
    tour_detail = db.Column(db.Text, nullable=False)
    airline = db.Column(db.String(50), nullable=False)

    def __init__(self, tour_program_name, max_number_of_customer, destination_city, destination_country, duration, min_price, max_price, tour_detail, airline):
        self.tour_program_name = tour_program_name
        self.max_number_of_customer = max_number_of_customer
        self.destination_city = destination_city
        self.destination_country = destination_country
        self.duration = duration
        self.min_price = min_price
        self.max_price = max_price
        self.tour_detail = tour_detail
        self.airline = airline

    def to_dict(self):
        return {
            'tour_program_id': self.tour_program_id,
            'tour_program_name': self.tour_program_name,
            'max_number_of_customer': self.max_number_of_customer,
            'destination_city': self.destination_city,
            'destination_country': self.destination_country,
            'duration': self.duration,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'tour_detail': self.tour_detail,
            'airline': self.airline
        }
    
class Trip(db.Model):
    __tablename__ = 'trip'
    trip_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tour_program_id = db.Column(db.Integer, db.ForeignKey('tour_program.tour_program_id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    number_of_customer = db.Column(db.Integer, nullable=False)
    reservation_start = db.Column(db.DateTime, nullable=False)
    reservation_end = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, tour_program_id, start_date, end_date, number_of_customer, reservation_start, reservation_end, price):
        self.tour_program_id = tour_program_id
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_customer = number_of_customer
        self.reservation_start = reservation_start
        self.reservation_end = reservation_end
        self.price = price

    def to_dict(self):
        return {
            'trip_id': self.trip_id,
            'tour_program_id': self.tour_program_id,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d'),
            'number_of_customer': self.number_of_customer,
            'reservation_start': self.reservation_start.strftime('%Y-%m-%d'),
            'reservation_end': self.reservation_end.strftime('%Y-%m-%d'),
            'price': self.price
        }


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        inp1 = request.form['inp1']
        inp2 = request.form['inp2']
        print(inp1, inp2)
        entry = Data(inp1, inp2)
        db.session.add(entry)
        db.session.commit()
        return render_template('success.html')


@app.route('/edit')
def edit():
    return render_template('edit_table.html')


@app.route('/customer')
def cust():
    return render_template('customer.html')


@app.route('/api/data')
def data():
    query = User.query.order_by(User.id)

    # search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            User.name.like(f'%{search}%'),
            User.email.like(f'%{search}%')
        ))
    total = query.count()

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            if name not in ['name', 'age', 'email', 'id']:
                name = 'name'
            col = getattr(User, name)
            if direction == '-':
                col = col.desc()
            order.append(col)
        if order:
            query = User.query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    # response
    return {
        'data': [user.to_dict() for user in query],
        'total': total,
    }


@app.route('/api/data', methods=['POST'])
def update():
    data = request.get_json()
    print(data)
    if 'id' not in data:
        abort(400)
    user = User.query.get(data['id'])
    if (data['type'] == "edit"):
        for field in ['name', 'age', 'address', 'phone', 'email']:
            if field in data:
                setattr(user, field, data[field])
    if (data['type'] == "delete"):
        print("deleted", data["id"])
        User.query.filter(User.id == data["id"]).delete()
    db.session.commit()
    return '', 204


@app.route('/api/data/customer')
def cust_data():
    query = Customer.query.order_by(Customer.customer_id)

    # search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            Customer.customer_id.cast(db.String).like(f'%{search}%'),
            Customer.firstname.like(f'%{search}%'),
            Customer.lastname.like(f'%{search}%'),
            Customer.national_id.like(f'%{search}%'),
            Customer.passport.like(f'%{search}%'),
            Customer.date_of_birth.cast(db.String).like(f'%{search}%'),
            Customer.gender.like(f'%{search}%'),
            Customer.email.like(f'%{search}%'),
            Customer.password.like(f'%{search}%')
        ))
    total = query.count()

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            if name not in customer_attrb:
                name = 'id'
            col = getattr(Customer, name)
            if direction == '-':
                col = col.desc()
            order.append(col)
        if order:
            query = Customer.query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    # response
    return {
        'data': [Customer.to_dict() for Customer in query],
        'total': total,
    }


@app.route('/api/data/customer', methods=['POST'])
def cust_update():
    data = request.get_json()
    print(data)
    if 'id' not in data:
        abort(400)
    customer = Customer.query.get(data['id'])
    total = Customer.query.count()
    if (data['type'] == "add"):
        data.pop('type')
        data.pop('id')
        data['customer_id'] = total + 1
        print("attempted to add", data)
        entry = Customer(**data)
        print("customer id askflaflsdhfjhdsjf", entry.customer_id)
        db.session.add(entry)
        db.session.commit()
    elif (data['type'] == "edit"):
        for field in customer_attrb:
            if field in data:
                setattr(customer, field, data[field])
    elif (data['type'] == "delete"):
        print("deleted", data["id"])
        Customer.query.filter(Customer.customer_id == data["id"]).delete()
    db.session.commit()
    return {
        'data': [Customer.to_dict() for Customer in Customer.query],
        'total': total,
    }, 200

@app.route('/cus_report')
def report_user_all():
    # Query data from the database
    customers = Customer.query.all()
    # Create a BytesIO buffer to store the PDF
    buffer = BytesIO()

    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    title = Paragraph("Customer Report", getSampleStyleSheet()['Title'])
    
    elements.append(title)


    # Add data to the PDF
    data = [
        ["Customer ID", "Firstname", "Lastname", "National ID", "Passport", "Date of Birth", "Gender", "Email", "Password"]
    ]
    for customer in customers:
        data.append([
            customer.customer_id,
            customer.firstname,
            customer.lastname,
            customer.national_id,
            customer.passport,
            customer.date_of_birth.strftime("%d %b %Y"),
            customer.gender,
            customer.email,
            customer.password
        ])

   # Calculate column widths to fit the A4 page
    num_cols = len(data[0])
    col_widths = [A4[0] / num_cols] * num_cols
    
    # Create a table and style
    table = Table(data, repeatRows=1)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 0), (-1, -1), 5.5)])  # กำหนดขนาดตัวอักษรเป็น auto'
    
    
    table.setStyle(style)
    
    col_widths = [1.5 * cm, 2 * cm, 2 * cm, 2 * cm, 1 * cm, 2 * cm, 0.9 * cm, 5 * cm, 2 * cm]  # ปรับขนาดความกว้างของแต่ละคอลัมน์
    table._argW = col_widths
    table.allow_auto_fit = True

    # Add table to the PDF
    elements.append(table)


    # Build the PDF
    doc.build(elements)

    # Reset buffer position
    buffer.seek(0)

    # Return PDF file to download
    return send_file(buffer, as_attachment=True,download_name="custumerreport")

@app.route("/cus_rep/<int:customer_id>")
def cus_rep(customer_id):
    customer = Customer.query.get(customer_id)
    
    if customer:
        buffer = BytesIO()

        # Create a PDF document
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        # Create a footer
        def footer(canvas, doc):
            date_text = "Generated on: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            canvas.drawRightString(A4[0] - 20, 20, date_text)

        # Add footer template to the document
        doc.build([], onLaterPages=footer)

        elements = []

        # Add customer details to the PDF
        title = Paragraph("Customer Report", getSampleStyleSheet()['Title'])
        elements.append(title)

        # Add customer information
        elements.append(Spacer(1, 20))  # Add space

        # Customer data
        data = [
            ["Name:", f"{customer.firstname} {customer.lastname}"],
            ["Date of Birth:", customer.date_of_birth.strftime('%d %b %Y')],
            ["National ID:", customer.national_id],
            ["Passport:", customer.passport],
            ["Gender:", customer.gender],
            ["Email:", customer.email]
        ]

        # Create a table for customer data
        table = Table(data, colWidths=[120, '*'])

        # Style the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 12)
        ])
        table.setStyle(style)

        elements.append(table)

        # Build the PDF
        doc.build(elements)

        # Reset buffer position
        buffer.seek(0)

        # Return PDF file to download
        return send_file(buffer, as_attachment=True, download_name=f"{customer.firstname}_{customer.lastname}_Report.pdf")
    else:
        return "Customer not found.", 404

    
if __name__ == '__main__':
    app.debug = True
    app.run()