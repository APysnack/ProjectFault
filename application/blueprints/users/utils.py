import os
import secrets
import boto3
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from application import mail
from werkzeug.utils import secure_filename


def create_s3_client():
    if current_app.config['ENV'] == 'development':
        s3 = boto3.client('s3', aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
                          aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
                          aws_session_token=current_app.config.get('AWS_SESSION_TOKEN'))
    else:
        s3 = boto3.client('s3')
    return s3


def upload_to_s3(file, folder_name, file_name):
    s3 = create_s3_client()
    s3_bucket = current_app.config['S3_BUCKET_NAME']
    s3_key = f"{folder_name}/{file_name}"
    s3.upload_fileobj(file, s3_bucket, s3_key)
    return f"{current_app.config['S3_BUCKET_URL']}{s3_key}"


def get_filename(image):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(image.filename)
    new_filename = random_hex + f_ext
    return new_filename


def resize_image(image, dimensions, filename):
    image_file = Image.open(image)
    image_file.thumbnail((dimensions['width'], dimensions['height']))

    temp_image_path = os.path.join(
        current_app.root_path, 'static/images', filename)

    image_file.save(temp_image_path)
    return temp_image_path


def save_picture(form_image, dimensions=None):
    new_filename = get_filename(form_image)

    if dimensions is None:
        image_file = form_image
    else:
        temp_image_path = resize_image(form_image, dimensions, new_filename)
        image_file = open(temp_image_path, 'rb')

    picture_path = upload_to_s3(image_file, 'pf-images', new_filename)

    if dimensions is not None:
        os.remove(temp_image_path)
    return picture_path


def save_audio_file(audio_file):
    audio_filename = secure_filename(audio_file.filename)
    print(audio_filename)
    audio_url = upload_to_s3(audio_file, 'pf-audio', audio_filename)
    return audio_url


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='admin@projectfault.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be  made.
'''

    mail.send(msg)


def send_email_confirmation(user):
    token = user.get_reset_token()
    msg = Message('Email confirmation for projectfault.com',
                  sender='admin@projectfault.com', recipients=[user.email])
    msg.body = f'''Thank you for registering at project fault! Please click the link below to confirm your email address and complete the registration process. 

{url_for('users.confirm_registration', token=token, _external=True)}

If you did not make this request then simply ignore this email and this account will not be verified
'''

    mail.send(msg)
