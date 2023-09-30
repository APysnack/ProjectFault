from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from application.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=4, max=20)])

    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'This username is already taken. Please choose another username.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                'This email address is already connected to an account.')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20)])

    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=4, max=20)])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])

    submit = SubmitField('Update')
    image = FileField('Update Profile Picture', validators=[
                      FileAllowed(['jpg', 'png'])])

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'This username is already taken. Please choose another username.')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError(
                    'This email address is already connected to an account.')


class RequestResetForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email. You must register first.')


class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])

    submit = SubmitField('Reset Password')


class AdminForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20)])

    email = StringField('Email Address', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[
                             Optional(), Length(min=7, max=60)])

    submit = SubmitField('Update')
    image = FileField('Update Profile Picture', validators=[
                      FileAllowed(['jpg', 'png'])])

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'This username is already taken. Please choose another username.')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError(
                    'This email address is already connected to an account.')


class ArtworkForm(FlaskForm):
    artwork = FileField('Upload Artwork', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    tag = SelectField('Select Tag', choices=[
                      ('photo', 'Photography'), ('digital', 'Digital Art')], validators=[DataRequired()])
    submit = SubmitField('Add Artwork')


class WritingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    details = StringField('Details', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    tag = SelectField('Select Tag', choices=[('writing', 'General Writing'), ('poem', 'Poetry'), (
        'topical', 'Topical'), ('text-battle', 'Text Battle')], validators=[DataRequired()])
    submit = SubmitField('Add Writing')


class VideoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    url = TextAreaField('Content ', validators=[DataRequired()])
    tag = SelectField('Select Tag', choices=[('lrc-videos', 'LRC Video'), ('battle-videos', 'My Battles'),
                      ('music-videos', 'Music Videos'), ('comedy-videos', 'Stand-Up Comedy')], validators=[DataRequired()])
    submit = SubmitField('Add Video')


class ProjectForm(FlaskForm):
    title = StringField('Project Name', validators=[DataRequired()])
    details = TextAreaField('Project Details', validators=[
        DataRequired(), Length(max=1000)])
    completion_time = IntegerField(
        'Days Until Completion', validators=[DataRequired()])

    submit = SubmitField('Add Project')


class AudioForm(FlaskForm):
    title = StringField('Song Title', validators=[DataRequired()])
    image = FileField('Upload Image File (Square Img Suggested (e.g. 125 x 125)', validators=[
        FileAllowed(['jpg', 'png'])])
    audio = FileField('Upload Song', validators=[
        FileAllowed(['mp3', 'wav'])])
    tag = SelectField('Select Tag', choices=[('instrumental', 'Instrumentals'), (
        'alternative', 'Non-Rap'), ('indie-rap', 'Indie Rap'), ('hip-hop', 'Classic Rap')], validators=[DataRequired()])
    lyrics = TextAreaField('Song Lyrics', validators=[
        DataRequired()])
    submit = SubmitField('Add Song')


class UpdateUserForm(FlaskForm):
    username = StringField('User To Update', validators=[DataRequired()])
    memberType = SelectField('Member Type', choices=[('remove', 'Remove'), ('platinum member', 'Platinum'), (
        'gold member', 'Gold'), ('silver member', 'Silver'), ('member', 'Member'), ('unconfirmed', 'Unconfirmed'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Submit Changes')
