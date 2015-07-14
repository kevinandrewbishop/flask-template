import flask
from flask import request
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, BooleanField, TextField, PasswordField, validators, SelectField
from wtforms.validators import Required
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.sqlalchemy import SQLAlchemy
import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = flask.Flask(__name__)
db_string = 'mysql://root:kevinb97@127.0.0.1:3306/website'
app.debug = True
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


'''
from config import config
import pandas as pd
import sqlalchemy

class Database:
    user = config.USER
    password = config.PASSWORD
    host = config.HOST
    schema = config.SCHEMA
    def __init__(self):
        self.engine = None
        self._create_engine()
        self._generate_methods()

    def _create_url(self):
        return "mysql+mysqlconnector://%s:%s@%s/%s"%(Database.user,Database.password,Database.host,Database.schema)

    def _create_engine(self):
        url = self._create_url()
        self.engine = sqlalchemy.create_engine(url)

    def _generate_methods(self):
        # Dynamically generate a method for accessing a
        # dataframe version of each table in the schema.
        table_names = self.engine.table_names()
        for name in table_names:
            def build_method(name):
                def method():
                    return self._query(name)
                return method
            method = build_method(name)
            setattr(self,name,method)

    def _query(self,tablename):
        return pd.io.sql.read_sql(tablename,self.engine)

'''

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    first_name = TextField('First Name', [validators.Length(min=4, max=25)])
    last_name = TextField('Last Name', [validators.Length(min=4, max=25)])
    phone_number = TextField('Phone Number', [validators.Length(min=6, max=35)])
    user_type = SelectField('I am a',[validators.Required()] ,choices = [('Client','Client'),('Trainer','Trainer')])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])
    submit = SubmitField('Submit')

class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.Required()])
    user_type = SelectField('I am a', [validators.Required()],choices = [('Client','Client'),('Trainer','Trainer')])
    submit = SubmitField('Submit')

class PUser(db.Model):
    username = db.Column(db.String(30), primary_key =True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    phone_number = db.Column(db.String(10))


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


@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/about')
def about():
    return flask.render_template('about.html')



@app.route('/profile', methods = ['GET','POST'])
def profile():
    transactions = None
    user = None
    form = NameForm()
    if flask.session.get('user'):
        if flask.session.get('user_type') == 'Client':
            user = Client.query.filter_by(username = flask.session.get('user')).first()
        else:
            user = Trainer.query.filter_by(username = flask.session.get('user')).first()
        transactions = user.transactions.order_by(Transaction.transaction_date).all()
    return flask.render_template('profile.html', client = user, transactions = transactions)

@app.route('/login',  methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_type = form.user_type.data
        if user_type == 'Client':
            user = Client.query.filter_by(username = form.username.data).first()
        else:
            user = Trainer.query.filter_by(username = form.username.data).first()
        if user is None:
            return flask.render_template('login.html', form = form, error = 'Invalid Username')
        elif not check_password_hash(user.password_, form.password.data):
            return flask.render_template('login.html', form = form, error = 'Invalid Password')
        else:
            flask.session['user'] = user.username
            flask.session['user_type'] = user_type
            #flask.flash('Logged in Successfully')
            return flask.redirect(flask.url_for('profile'))
    return flask.render_template('login.html', form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    duplicate = False
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        if form.user_type.data == 'Client':
            user = Client()

        else:
            user = Trainer()
        if Client.query.filter_by(username = form.username.data).first() or Trainer.query.filter_by(username = form.username.data).first():
            return flask.render_template('register.html', form=form, duplicate = True)
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.phone_number = form.phone_number.data
        user.password_ = generate_password_hash(form.password.data)

        db.session.add(user)
        db.session.commit()
        #flask.flash('Thanks for registering')
        return flask.redirect(flask.url_for('login'))
    return flask.render_template('register.html', form=form)


@app.route('/fix_pws', methods=['GET', 'POST'])
def fix_pws():
    for client in Client.query.all():
        client.password_ = generate_password_hash('test')
        db.session.commit()
    for trainer in Trainer.query.all():
        trainer.password_ = generate_password_hash('test')
        db.session.commit()

    return 'changed!'




if __name__ == '__main__':
    manager.run()
