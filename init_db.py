from application import create_app, db, bcrypt
from application.models import User

app = create_app()

with app.app_context():
    db.create_all()
    hashed_pw = bcrypt.generate_password_hash("password").decode("utf-8")
    user = User(username='admin', email='email@foo.com', password=hashed_pw, rank='admin')
    db.session.add(user)
    db.session.commit()
