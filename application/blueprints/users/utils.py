import os
import secrets
import boto3
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from application import mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def save_picture(form_image, type):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_image.filename)
    new_filename = random_hex + f_ext

    if current_app.config['ENV'] == 'development':
      s3 = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
        aws_session_token=current_app.config.get('AWS_SESSION_TOKEN')
      )

    else: 
      s3 = boto3.client('s3')
    
    s3_bucket = current_app.config['S3_BUCKET_NAME']
    s3_key = 'pf-images/' + new_filename
    s3.upload_fileobj(form_image, s3_bucket, s3_key)

    picture_path = f"{current_app.config['S3_BUCKET_URL']}{s3_key}"
    return picture_path


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


def send_mass_email(title, content, members):
    with mail.connect() as conn:
        for member in members:
            message = content
            subject = title
            msg = Message(recipients=[member.email],
                          body=message,
                          sender="admin@projectfault.com",
                          subject=subject)

            conn.send(msg)
