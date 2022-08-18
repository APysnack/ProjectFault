from flask_mail import Message
from application import mail


def send_message(name, email, message):
    msg = Message(f'New Message from {email}',
                  sender='admin@projectfault.com', recipients=['admin@projectfault.com'])
    msg.body = f'''Name: {name}
    Email: {email}
    Message: {message}'''

    mail.send(msg)
