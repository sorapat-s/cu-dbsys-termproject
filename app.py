from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:p0stBLANC@localhost/termproject'
db = SQLAlchemy(app)

customer_attrb = ["customer_id", "firstname", "lastname", "national_id",
                  "passport", "date_of_birth", "gender", "email", "password"]

custtrip_attrb = ["customer_id", "trip_id", "payment_status", "payment_due"]

payment_attrb = ["customer_id", "card_number", "security_code", "expiry_date"]

program_attrb = ["tour_program_id", "tour_program_name", "max_number_of_customer", "destination_city",
                 "destination_country", "duration", "min_price", "max_price", "tour_detail", "airline"]

trip_attrb = ["trip_id", "tour_program_id", "start_date", "end_date",
              "number_of_customer", "reservation_start", "reservation_end", "price"]


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


class CustomerTrip(db.Model):
    __tablename__ = 'customer_trip'
    customer_id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, primary_key=True)
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
            'payment_status': str(self.payment_status),
            'payment_due': self.payment_due.strftime('%Y-%m-%d %H:%M:%S')
        }


class CustomerPaymentMethod(db.Model):
    __tablename__ = 'customer_payment_method'
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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


class TourProgram(db.Model):
    __tablename__ = 'tour_program'
    tour_program_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    tour_program_name = db.Column(db.String(50), nullable=False)
    max_number_of_customer = db.Column(db.Integer, nullable=False)
    destination_city = db.Column(db.String(50), nullable=False)
    destination_country = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    min_price = db.Column(db.Integer, nullable=False)
    max_price = db.Column(db.Integer, nullable=False)
    tour_detail = db.Column(db.Text, nullable=False)
    airline = db.Column(db.String(50), nullable=False)

    def __init__(self, tour_program_id, tour_program_name, max_number_of_customer, destination_city, destination_country, duration, min_price, max_price, tour_detail, airline):
        self.tour_program_id = tour_program_id
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
    tour_program_id = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    number_of_customer = db.Column(db.Integer, nullable=False)
    reservation_start = db.Column(db.DateTime, nullable=False)
    reservation_end = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, trip_id, tour_program_id, start_date, end_date, number_of_customer, reservation_start, reservation_end, price):
        self.trip_id = trip_id,
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


@app.route('/customer_trip')
def custtrip():
    return render_template('custtrip.html')


@app.route('/customer_payment_method')
def pay():
    return render_template('payment.html')


@app.route('/tour_program')
def prog():
    return render_template('program.html')


@app.route('/trip')
def trip():
    return render_template('trip.html')


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
    print("object", customer)
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


@app.route('/api/data/customer_trip')
def custtrip_data():
    query = CustomerTrip.query.order_by(CustomerTrip.payment_due)

    # search filter
    search = request.args.get('search')
    if search:
        print('search')
        query = query.filter(db.or_(
            CustomerTrip.customer_id.cast(db.String).like(f'%{search}%'),
            CustomerTrip.trip_id.cast(db.String).like(f'%{search}%'),
            CustomerTrip.payment_status.cast(db.String).like(f'%{search}%'),
            CustomerTrip.payment_due.cast(db.String).like(f'%{search}%')
        ))
    total = query.count()
    print(total)

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            if name not in custtrip_attrb:
                name = 'id'
            col = getattr(CustomerTrip, name)
            if direction == '-':
                col = col.desc()
            order.append(col)
        if order:
            query = CustomerTrip.query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    # response
    return {
        'data': [ct.to_dict() for ct in query],
        'total': total,
    }


@app.route('/api/data/customer_trip', methods=['POST'])
def custtrip_update():
    data = request.get_json()
    print(data)
    if 'id' not in data:
        abort(400)
    total = CustomerTrip.query.count()
    if (data['type'] == "add"):
        data.pop('type')
        data.pop('id')
        print("attempted to add", data)
        if data['payment_status'] == 'true':
            data['payment_status'] = True
        else:
            data['payment_status'] = False
        entry = CustomerTrip(**data)
        print("customer id askflaflsdhfjhdsjf", entry.customer_id)
        db.session.add(entry)
        db.session.commit()
    elif (data['type'] == "edit"):
        customer = CustomerTrip.query.get((data['id'], data['id2']))
        print("editting")
        for field in custtrip_attrb:
            if field in data:
                if (data[field] == "False" or data[field] == "false"):
                    data[field] = False
                if (data[field] == "True" or data[field] == "true"):
                    data[field] = True
                setattr(customer, field, data[field])
    elif (data['type'] == "delete"):
        print("deleted", data["id"])
        CustomerTrip.query.filter(CustomerTrip.customer_id == data["id"]).filter(
            CustomerTrip.trip_id == data["id2"]).delete()
    db.session.commit()
    return {
        'data': [ct.to_dict() for ct in CustomerTrip.query],
        'total': total,
    }, 200


@app.route('/api/data/customer_payment_method')
def payment_data():
    query = CustomerPaymentMethod.query.order_by(
        CustomerPaymentMethod.customer_id)

    # search filter
    search = request.args.get('search')
    if search:
        print('search')
        query = query.filter(db.or_(
            CustomerPaymentMethod.customer_id.cast(
                db.String).like(f'%{search}%'),
            CustomerPaymentMethod.card_number.like(f'%{search}%'),
            CustomerPaymentMethod.security_code.like(f'%{search}%'),
            CustomerPaymentMethod.expiry_date.like(f'%{search}%')
        ))
    total = query.count()
    print(total)

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            if name not in payment_attrb:
                name = 'id'
            col = getattr(CustomerPaymentMethod, name)
            if direction == '-':
                col = col.desc()
            order.append(col)
        if order:
            query = CustomerPaymentMethod.query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    # response
    return {
        'data': [ct.to_dict() for ct in query],
        'total': total,
    }


@app.route('/api/data/customer_payment_method', methods=['POST'])
def payment_update():
    data = request.get_json()
    print(data)
    if 'id' not in data:
        abort(400)
    total = CustomerPaymentMethod.query.count()
    if (data['type'] == "add"):
        data.pop('type')
        data.pop('id')
        print("attempted to add", data)
        entry = CustomerPaymentMethod(**data)
        print("customer id askflaflsdhfjhdsjf", entry.customer_id)
        db.session.add(entry)
        db.session.commit()
    elif (data['type'] == "edit"):
        customer = CustomerPaymentMethod.query.get((data['id'], data['id2']))
        print("editting")
        for field in payment_attrb:
            if field in data:
                setattr(customer, field, data[field])
    elif (data['type'] == "delete"):
        print("deleted", data["id"])
        print("deleted", data["id2"])
        CustomerPaymentMethod.query.filter(CustomerPaymentMethod.customer_id == data["id"]).filter(
            CustomerPaymentMethod.card_number == str(data['id2'])).delete()
    db.session.commit()
    return {
        'data': [ct.to_dict() for ct in CustomerPaymentMethod.query],
        'total': total,
    }, 200


@app.route('/api/data/tour_program')
def prog_data():
    query = TourProgram.query.order_by(TourProgram.tour_program_id)

    # search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            TourProgram.tour_program_id.cast(db.String).like(f'%{search}%'),
            TourProgram.tour_program_name.like(f'%{search}%'),
            TourProgram.destination_city.like(f'%{search}%'),
            TourProgram.destination_country.like(f'%{search}%'),
            TourProgram.duration.like(f'%{search}%'),
            TourProgram.max_number_of_customer.cast(
                db.String).like(f'%{search}%'),
            TourProgram.max_price.cast(db.String).like(f'%{search}%'),
            TourProgram.min_price.cast(db.String).like(f'%{search}%'),
            TourProgram.tour_detail.like(f'%{search}%'),
            TourProgram.airline.like(f'%{search}%')
        ))
    total = query.count()

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            if name not in program_attrb:
                name = 'tour_program_id'
            col = getattr(TourProgram, name)
            if direction == '-':
                col = col.desc()
            order.append(col)
        if order:
            query = TourProgram.query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    # response
    return {
        'data': [tp.to_dict() for tp in query],
        'total': total,
    }


@app.route('/api/data/tour_program', methods=['POST'])
def prog_update():
    data = request.get_json()
    print(data)
    if 'id' not in data:
        abort(400)
    customer = TourProgram.query.get(data['id'])
    print("object", customer)
    total = TourProgram.query.count()
    if (data['type'] == "add"):
        data.pop('type')
        data.pop('id')
        data['tour_program_id'] = total + 1
        print("attempted to add", data)
        entry = TourProgram(**data)
        print("customer id askflaflsdhfjhdsjf", entry.tour_program_id)
        db.session.add(entry)
        db.session.commit()
    elif (data['type'] == "edit"):
        for field in program_attrb:
            if field in data:
                setattr(customer, field, data[field])
    elif (data['type'] == "delete"):
        print("deleted", data["id"])
        TourProgram.query.filter(
            TourProgram.tour_program_id == data["id"]).delete()
    db.session.commit()
    return {
        'data': [tp.to_dict() for tp in TourProgram.query],
        'total': total,
    }, 200


@app.route('/api/data/trip')
def trip_data():
    query = Trip.query.order_by(Trip.trip_id)

    # search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            Trip.trip_id.cast(db.String).like(f'%{search}%'),
            Trip.tour_program_id.cast(db.String).like(f'%{search}%'),
            Trip.start_date.cast(db.String).like(f'%{search}%'),
            Trip.end_date.cast(db.String).like(f'%{search}%'),
            Trip.number_of_customer.cast(db.String).like(f'%{search}%'),
            Trip.reservation_start.cast(db.String).like(f'%{search}%'),
            Trip.reservation_end.cast(db.String).like(f'%{search}%'),
            Trip.price.cast(db.String).like(f'%{search}%')
        ))
    total = query.count()

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            if name not in trip_attrb:
                name = 'tour_program_id'
            col = getattr(Trip, name)
            if direction == '-':
                col = col.desc()
            order.append(col)
        if order:
            query = Trip.query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    # response
    return {
        'data': [tp.to_dict() for tp in query],
        'total': total,
    }


@app.route('/api/data/trip', methods=['POST'])
def trip_update():
    data = request.get_json()
    print(data)
    if 'id' not in data:
        abort(400)
    customer = Trip.query.get(data['id'])
    print("object", customer)
    total = Trip.query.count()
    if (data['type'] == "add"):
        data.pop('type')
        data.pop('id')
        data['trip_id'] = total + 1
        data['number_of_customer'] = 0
        print("attempted to add", data)
        entry = Trip(**data)
        print("customer id askflaflsdhfjhdsjf", entry.trip_id)
        db.session.add(entry)
        db.session.commit()
    elif (data['type'] == "edit"):
        for field in trip_attrb:
            if field in data:
                setattr(customer, field, data[field])
    elif (data['type'] == "delete"):
        print("deleted", data["id"])
        Trip.query.filter(
            Trip.trip_id == data["id"]).delete()
    db.session.commit()
    return {
        'data': [tp.to_dict() for tp in Trip.query],
        'total': total,
    }, 200


if __name__ == '__main__':
    app.debug = True
    app.run()
