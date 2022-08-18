from flask import render_template, request, Blueprint, redirect, url_for, flash
from application import bcrypt
from application.models import Post, User
from application.blueprints.main.utils import validateInput
from flask_login import login_user

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/index", methods=['GET'])
def index():
    return render_template('main/index.html')


@main.route("/art")
def art():
    return render_template('main/art.html')


@main.route("/audio")
def audio():
    return render_template('main/audio.html', title='Audio Media')


@main.route("/media", methods=['GET', 'POST'])
def media():
    if request.method == 'POST':
        userName = request.form.get("userName", "None")
        password = request.form.get("userPW", "None")
        userName, password, isValid = validateInput(userName, password)
        if isValid:
            user = User.query.filter_by(username=userName).first()
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user, remember=True)
                next_page = request.args.get('next')
                flash('Successfully logged in!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('main.media'))
            else:
                flash(
                    'Login Unsuccessful. Please check your username and password', 'danger')

    return render_template('main/media.html', title='Media Map')


@main.route("/misc")
def miscellaneous():
    return render_template('main/miscellaneous.html', title='Miscellaneous')


@ main.route("/news")
def news():
    posts = Post.query.order_by(Post.date_posted.desc()).limit(3).all()
    return render_template('main/news.html', title='News', posts=posts)


@main.route("/programming")
def programming():
    return render_template('main/programming.html', title='Programming')


@main.route("/video")
def video():
    return render_template('main/video.html', title='Video Media')


@main.route("/text")
def text():
    return render_template('main/text.html', title='Text Media')


@main.route("/board")
def board():
    page = request.args.get('page', 1, type=int)
    forum_posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('main/board.html', forum_posts=forum_posts)
