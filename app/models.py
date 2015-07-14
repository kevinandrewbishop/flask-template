from . import db
#Classes here are for Object Relational Mapping




class Client(db.Model):
    __tablename__ = 'clients'
    username = db.Column(db.String(30), primary_key =True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    phone_number = db.Column(db.String(10))
    transactions = db.relationship('Transaction', backref = 'client', lazy='dynamic')
    password_ = db.Column(db.String(80))

    def __repr__(self):
        return '<Client %r>' % self.username

class Trainer(db.Model):
    __tablename__ = 'trainers'
    username = db.Column(db.String(30), primary_key =True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    phone_number = db.Column(db.String(10))
    transactions = db.relationship('Transaction', backref = 'trainer', lazy='dynamic')
    password_ = db.Column(db.String(80))

    def __repr__(self):
        return '<Trainer %r>' % self.username

class Transaction(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.Integer, primary_key=True)
    client_username = db.Column(db.String(30), db.ForeignKey('clients.username'))
    trainer_username = db.Column(db.String(30), db.ForeignKey('trainers.username'))
    transaction_date = db.Column(db.Date)
    dollar_amount = db.Column(db.Numeric)

    def __repr__(self):
        return '<Transaction %r>' % self.transaction_id

class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30))
    title = db.Column(db.String(30))
    body = db.Column(db.Text)

    def render(self, attr):
        return getattr(self, attr)
