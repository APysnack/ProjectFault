# ProjectFault
Flask web application developed Summer of 2021

1. MacOS pyenv installation (ensure Brew is installed)
- `brew update`
- `brew install pyenv`
- `echo 'eval "$(pyenv init --path)"' >> ~/.zshrc`
- `echo 'eval "$(pyenv init -)"' >> ~/.zshrc`
- `source ~/.zshrc`
- `pyenv --version`

2. cd into root and create a virtual environment:
- `python3 -m venv myenv `

3. Activate environment and install application dependencies:
- `source myenv/bin/activate`
- `pip3 install -r requirements.txt`

5. Create local database
- `source myenv/bin/activate`
- `python`
- `from application import create_app, db`
-  `from application.models import User` (there might be other imports I’m missing)
- `app = create_app()`

```
with app.app_context():
  db.create_all()
  hashed_pw = bcrypt.generate_password_hash("ENTER_PASSWORD_HERE").decode("utf-8")
  user = User(username='Namehere', email='email@foo.com', password=hashed_pw)
  db.session.add(user)
  db.session.commit()
```
  
Verify with User.query.all()

- exit()
- python3 run_app.py
