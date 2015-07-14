import flask
from flask import render_template, session, redirect, url_for, current_app
from .forms import NameForm, LoginForm, RegistrationForm, PostForm
from ..models import Client, Trainer, Transaction, Post
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from . import main




@main.before_request
def before_request():
    pass

@main.route('/')
def index():
    return flask.render_template('index.html')


@main.route('/profile', methods = ['GET','POST'])
def profile():
    if not flask.session.get('username'):
        return flask.render_template('profile.html', form = None, client = None, transactions = None)
    username = flask.session.get('username')
    form = PostForm()
    if form.validate_on_submit():
        post = Post()
        post.username = username
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()

    if flask.session.get('user_type') == 'Client':
        user = Client.query.filter_by(username = username).first()
    else:
        user = Trainer.query.filter_by(username = username).first()
    transactions = user.transactions.order_by(Transaction.transaction_date.desc()).all()
    posts = Post.query.filter_by(username = username).order_by(Post.post_id.desc())
    return flask.render_template('profile.html', form = form, client = user, transactions = transactions, posts = posts)

@main.route('/login',  methods = ['GET','POST'])
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
            flask.session['username'] = user.username
            flask.session['user_type'] = user_type
            #flask.flash('Logged in Successfully')
            return redirect(url_for('main.profile'))
    return flask.render_template('login.html', form = form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    duplicate = False
    form = RegistrationForm(flask.request.form)
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
