# ProjectFault
Flask web application developed Summer of 2021

MacOS installation instructions

- Brew should be installed
`brew update`
`brew install pyenv`
`echo 'eval "$(pyenv init --path)"' >> ~/.zshrc`
`echo 'eval "$(pyenv init -)"' >> ~/.zshrc`
`source ~/.zshrc`
`pyenv --version`

- cd into root
- Create a virtual environment: python3 -m venv myenv 
- Activate environment source myenv/bin/activate

- pip install -r requirements.txt
- pip install flask
- copy environment variables/secrets from config.py
- run python3 run_app.py and install any dependencies required  migrate database:
- activate virtual environment: source myenv/bin/activate
- type “python” followed by: from application import create_app from application import db from application.models import User (there might be other imports I’m missing)  app = create_app() with app.app_context():
         db.create_all()
         user = User.query.first()
         hashed_pw = bcrypt.generate_password_hash("supersecretpassword").decode("utf-8")
         user.password = hashed_pw
         db.session.commit()


- exit()
