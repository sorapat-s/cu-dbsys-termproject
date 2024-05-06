from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
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
        print("customer id ,jsdlkgldjgkdjflgjdlfgjdlkfgjldkfjglk", self.customer_id)

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


if __name__ == '__main__':
    app.debug = True
    app.run()
