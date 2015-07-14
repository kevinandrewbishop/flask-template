from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, BooleanField, TextField, PasswordField, validators, SelectField
from flask.ext.pagedown.fields import PageDownField
from wtforms.validators import Required



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

class PostForm(Form):
    title = TextField('Title', [validators.Length(min=4, max=25)])
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')
