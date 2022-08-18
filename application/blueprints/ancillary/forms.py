from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class ContactForm(FlaskForm):
    message = TextAreaField('Message', validators=[
        DataRequired()], render_kw={"placeholder": "Please enter your message"})
    name = StringField('Name', validators=[DataRequired()], render_kw={
        "placeholder": "Your name"})
    email = StringField('Email Address', validators=[
                        DataRequired(), Email()], render_kw={"placeholder": "Your email address"})
    submit = SubmitField('Submit')
