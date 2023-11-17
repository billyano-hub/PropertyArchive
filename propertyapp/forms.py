from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import Email, DataRequired,EqualTo,Length

class UserRegForm(FlaskForm):
    fullname = StringField("First Name",validators=[DataRequired("First Name cannot be empty")])
    email = StringField("Email Address",validators=[Email(message="enter correct email format"),DataRequired("Please enter password")])
    pwd = PasswordField("Enter Password",validators=[DataRequired()])
    confpwd = PasswordField("Confirm Password",validators=[EqualTo('pwd', message=("password must be the same"))])
    message = TextAreaField("Your Profile")
    btnsubmit = SubmitField("Create Account!")

class AgentRegForm(FlaskForm):
    fullname = StringField("First Name",validators=[DataRequired("First Name cannot be empty")])
    email = StringField("Email Address",validators=[Email(message="enter correct email format"),DataRequired("Please enter password")])
    pwd = PasswordField("Enter Password",validators=[DataRequired()])
    confpwd = PasswordField("Confirm Password",validators=[EqualTo('pwd', message=("password must be the same"))])
    message = TextAreaField("Your Profile")
    btnsubmit = SubmitField("Register!")
class ProfileForm(FlaskForm):
    fullname = StringField("First Name",validators=[DataRequired("First Name cannot be empty")])
    email = StringField("Email Address",validators=[Email(message="enter correct email format"),DataRequired("Please enter password")],render_kw={"readonly":True})
    btncancel=SubmitField("Cancel")
    btnsubmit=SubmitField("Save!")
class AgentProfileForm(FlaskForm):
    fullname = StringField("First Name",validators=[DataRequired("First Name cannot be empty")])
    email = StringField("Email Address",validators=[Email(message="enter correct email format"),DataRequired("Please enter password")],render_kw={"readonly":True})
    btncancel=SubmitField("Cancel")
    btnsubmit=SubmitField("Save!")