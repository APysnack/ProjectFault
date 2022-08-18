import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from application import mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def save_picture(form_image, type):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_image.filename)
    new_filename = random_hex + f_ext
    if type == 'audio_img':
        picture_path = os.path.join(
            current_app.root_path, 'static/audio/audio-images', new_filename)
    else:
        picture_path = os.path.join(
            current_app.root_path, 'static/images', new_filename)

    if type == 'avatar':
        output_size = (125, 125)

    elif type == 'artwork':
        i = Image.open(form_image)
        i.save(picture_path)
        return new_filename

    else:
        output_size = (150, 150)

    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(picture_path)

    return new_filename


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
